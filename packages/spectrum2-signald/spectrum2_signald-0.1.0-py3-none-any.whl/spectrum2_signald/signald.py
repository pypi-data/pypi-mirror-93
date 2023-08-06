from dataclasses import dataclass
from enum import Enum
import asyncio
import time
import typing
import logging

from pysignald_async.api import SignaldAPI, Profile
from pysignald_async import generated
from pysignald_async.error import SignaldException
from spectrum2.protocol_pb2 import WrapperMessage as wm
import spectrum2.protocol_pb2 as spb2


class MessageState(Enum):
    """
    A message is marked sent once signald responds with a send_results.
    """

    PENDING = 0
    SENT = 1


@dataclass
class Message:
    """
    Represents a message sent via this module.
    """

    state: MessageState
    payload: dict
    id: str

    def set_sent(self):
        self.state = MessageState.SENT


class PendingMessages:
    """
    Store messages that have been sent, awaiting their receipts.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.messages: typing.List[Message] = []

    def pop_message_by_timestamp(self, timestamp: int):
        """
        Remove and return a message from this storage using a timestamp in
        nanoseconds to identify it.
        """
        for message in self.messages:
            if message.payload["timestamp"] == timestamp:
                result = message
                self.messages.remove(result)
                if result.state == MessageState.PENDING:
                    self.logger.warning("Popping message with PENDING state")
                return message

    def append(self, message: Message):
        """
        Add a message to this storage.
        """
        self.messages.append(message)


class SpectrumClient(SignaldAPI):
    def __init__(self, spectrum2: "spectrum2_signald.SignalBackend", *a, **kw):
        super().__init__(*a, **kw)
        self.spectrum2 = spectrum2
        self.sessions = spectrum2.sessions
        self.pending_messages = PendingMessages()

    def handle_version(self, payload: dict):
        self.logger.info(f"Signald version: {payload['data']['version']}")

    def handle_message(self, payload):
        envelope = generated.JsonMessageEnvelopev1(**payload.get("data", dict()))
        loop = asyncio.get_running_loop()
        # if envelope.groupV2 is not None:
        source_number = envelope.source.number
        username = envelope.username

        if envelope.typing is not None:
            action = envelope.typing.action
            if envelope.typing.groupId is not None:
                return  # No typing notif for groups
            if action == "STARTED":
                self.on_buddy_starts_typing(username, source_number)
            elif action == "STOPPED":
                self.on_buddy_stopped_typing(username, source_number)
        if envelope.dataMessage is not None:
            group = envelope.dataMessage.groupV2
            if group is None:
                if envelope.dataMessage.body is not None:
                    self.on_message(username, source_number, envelope.dataMessage.body)
                if envelope.dataMessage.attachments is not None:
                    for attachment in envelope.dataMessage.attachments:
                        self.on_attachment(username, source_number, attachment)
            else:
                fut = asyncio.create_task(self.get_profile(username, envelope.source))
                # profile: Profile =
                if envelope.dataMessage.body is not None:
                    fut.add_done_callback(
                        lambda fut_profile: self.on_group_message(
                            username,
                            fut_profile.result().name,
                            group.id,
                            envelope.dataMessage.body,
                        )
                    )
                if envelope.dataMessage.attachments is not None:
                    for attachment in envelope.dataMessage.attachments:
                        fut.add_done_callback(
                            lambda fut_profile: self.on_group_attachment(
                                username,
                                fut_profile.result().name,
                                group.id,
                                attachment,
                            )
                        )
        if envelope.syncMessage is not None:
            sent = envelope.syncMessage.sent
            if sent is not None:
                if sent.message is not None:
                    if sent.message.body is not None:
                        group = sent.message.groupV2
                        if group is None:
                            self.on_message_sent_from_other_device(
                                username,
                                sent.destination.number,
                                sent.message.body,
                                envelope.timestampISO,
                            )
                        else:
                            self.on_group_message_sent_from_other_device(
                                username,
                                group.id,
                                sent.message.body,
                                envelope.timestampISO,
                            )
        if envelope.type == "RECEIPT":
            message = self.pending_messages.pop_message_by_timestamp(envelope.timestamp)
            self.on_receipt(username, message)
        if envelope.receipt is not None:
            for timestamp in envelope.receipt.timestamps:
                message = self.pending_messages.pop_message_by_timestamp(timestamp)
                self.on_receipt(username, message)

    def on_buddy_starts_typing(self, account, source_number):
        session = self.sessions.get_session(phone=account)
        self.spectrum2.handle_buddy_typing(user=session.jid, buddy_name=source_number)

    def on_buddy_stopped_typing(self, account, source_number):
        session = self.sessions.get_session(phone=account)
        self.spectrum2.handle_buddy_stopped_typing(
            user=session.jid, buddy_name=source_number
        )

    def on_message(self, account, source_number, body):
        session = self.sessions.get_session(phone=account)
        self.spectrum2.handle_message(
            user=session.jid, legacy_name=source_number, message=body, nickname=""
        )

    def on_group_message(self, account, source_name, group_id, body):
        session = self.sessions.get_session(phone=account)
        self.spectrum2.handle_message(
            user=session.jid,
            legacy_name=group_id.lower(),
            nickname=source_name,
            message=body,
        )

    def on_attachment(self, account, source_number, attachment):
        url = self.spectrum2.copy_file(attachment)
        self.on_message(
            account=account,
            source_number=source_number,
            body=url,
        )

    def on_receipt(self, account, message):
        session = self.sessions.get_session(phone=account)
        self.logger.debug(f"Receipt for {message}")
        if message is None or "recipientGroupId" in message.payload:
            return
        self.spectrum2.handle_message_ack(
            user=session.jid,
            legacy_name=message.payload["recipientAddress"]["number"],
            mid=message.id,
        )

    def on_group_attachment(self, account, source_name, group_id, attachment):
        url = self.spectrum2.copy_file(attachment)
        self.on_group_message(
            account=account, source_name=source_name, group_id=group_id, body=url
        )

    def on_message_sent_from_other_device(self, account, buddy_number, body, timestamp):
        session = self.sessions.get_session(phone=account)
        m = spb2.ConversationMessage()
        m.userName = session.jid
        m.buddyName = buddy_number
        m.message = body
        m.timestamp = ""  # str(timestamp // 1_000)

        m.nickname = ""
        m.xhtml = ""
        m.carbon = True
        self.logger.debug(f"Carbon: {m}")
        self.spectrum2.send_wrapped(m.SerializeToString(), wm.TYPE_CONV_MESSAGE)

    def on_group_message_sent_from_other_device(
        self, account, group_id, body, timestamp
    ):
        session = self.sessions.get_session(phone=account)
        self.spectrum2.handle_message(
            user=session.jid,
            legacy_name=group_id.lower(),
            message=body,
            nickname=session.name,
        )

    def on_attachment_sent_from_other_device(
        self,
        account,
        buddy_number,
        attachment,
        timestamp,
    ):
        url = self.spectrum2.copy_file(attachment)
        self.on_message_sent_from_other_device(account, buddy_number, url, timestamp)

    def on_group_attachment_sent_from_other_device(
        self,
        account,
        group_id,
        attachment,
        timestamp,
    ):
        url = self.spectrum2.copy_file(attachment)
        self.on_group_message_sent_from_other_device(account, group_id, url, timestamp)

    async def send_message(self, from_, to, text, group, mid=None):
        # TODO: use SignaldGeneratedAPI.send instead of manually building the payload
        timestamp = time.time_ns() // 1_000_000
        payload = {
            "type": "send",
            "username": from_,
            "messageBody": text,
            "timestamp": timestamp,
        }
        if group is None:
            payload["recipientAddress"] = {"number": to}
        else:
            payload["recipientGroupId"] = group
        message = Message(state=MessageState.PENDING, payload=payload, id=mid)
        self.pending_messages.append(message)
        try:
            payload = await self.get_response(payload)
        except SignaldException:
            self.pending_messages.messages.remove(message)
            raise
        else:
            message.set_sent()
