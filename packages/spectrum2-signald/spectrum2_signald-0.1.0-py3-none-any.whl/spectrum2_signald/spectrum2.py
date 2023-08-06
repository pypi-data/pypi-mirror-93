from dataclasses import dataclass, field
from pathlib import Path
import subprocess
import sys
import logging
import asyncio
import random
import shutil
import time

from pysignald_async.error import SignaldException
from pysignald_async import generated
from spectrum2_signald.signald import SpectrumClient

from spectrum2 import Backend, Config
from spectrum2.protocol_pb2 import WrapperMessage as wm
import spectrum2.protocol_pb2 as spb2


@dataclass
class Session:
    phone: str
    jid: str
    name: str
    real_room_names: dict = field(default_factory=dict)


class Sessions:
    def __init__(self):
        self.sessions = []
        self.logger = logging.getLogger(self.__class__.__name__)

    def add(self, phone, jid):
        session = Session(phone=phone, jid=jid, real_room_names={})
        self.sessions.append(session)
        return session

    def get_session(self, phone=None, jid=None) -> Session:
        for s in self.sessions:
            if s.phone == phone:
                return s
            if s.jid == jid:
                return s
        else:
            self.logger.warning(
                f"Couldn't find session with phone '{phone}' or JID '{jid}'"
            )

    def remove(self, phone=None, jid=None):
        self.sessions.remove(self.get_session(phone=phone, jid=jid))


class SignalBackend(Backend):
    def __init__(self, socket_path, *a, **kwa):
        # because pylint does not get it
        self.config = dict()
        super().__init__(*a, **kwa)
        self.sessions = Sessions()
        self.on_con_lost = asyncio.get_running_loop().create_future()
        self.futures = {}

        self.signald = SpectrumClient(self)
        task = asyncio.create_task(self.connect_signald(socket_path))
        while not task.done:
            time.sleep(1)

    def connection_made(self, transport):
        self.transport = transport
        self.logger.debug("Connection established")
        config = spb2.BackendConfig()
        config.config = "[registration]\nneedPassword=0\n[features]\nreceipts=1"
        self.send_wrapped(config.SerializeToString(), wm.TYPE_BACKEND_CONFIG)

    async def connect_signald(self, socket_path):
        loop = asyncio.get_running_loop()
        while True:
            try:
                _, self.signald = await loop.create_unix_connection(
                    lambda: self.signald, path=socket_path
                )
            except (FileNotFoundError, ConnectionRefusedError):
                self.logger.warning(
                    "Cannot connect to signald socket, waiting 5 seconds"
                )
                await asyncio.sleep(5)
            else:
                break

        self.signald.on_con_lost.add_done_callback(
            lambda res: self.on_con_lost.set_result(True)
        )

    def connection_lost(self, exc):
        self.logger.debug(f"Connection lost: {exc}")
        self.transport = None
        try:
            self.on_con_lost.set_result(True)
        except asyncio.InvalidStateError:
            pass

    def handle_login_request(self, user, legacy_name, password, extra):
        self.logger.info("Login")
        asyncio.create_task(self.login(user, legacy_name))

    async def login(self, jid, phone):
        while True:
            try:
                await self.signald.subscribe(phone)
            except SignaldException:
                await self.link_or_register(jid, phone)
            else:
                break
        signald: SpectrumClient = self.signald
        my_profile = await signald.get_profile(
            username=phone, recipientAddress=generated.JsonAddressv1(number=phone)
        )
        session = Session(phone=phone, jid=jid, name=my_profile.name)
        self.sessions.sessions.append(session)
        self.handle_connected(user=jid)
        asyncio.gather(
            self.get_roster(session),
            self.get_rooms(
                session, inform_user=self.config["signal.send_room_list_to_user"]
            ),
        )

    async def link_or_register(self, jid, phone):
        while True:
            res = await self.prompt_user(
                jid,
                "Do you want to [link] this transport as "
                "a new device or [register] your phone number?",
            )
            if res == "link":
                self.logger.debug(f"User '{jid}' requested to link '{phone}'")
                uri, linking_successful = await self.signald.link(
                    phone, device_name=self.config["signal.device_name"]
                )
                filename = (
                    "".join(
                        random.choice("abcdefghijklmnopqrstuvwxyz0123456789")
                        for _ in range(20)
                    )
                    + ".png"
                )
                self.logger.debug("Generating QR code")
                img_path = self.config["service.web_directory"] + filename
                qr_encode(uri, img_path)
                img_url = self.config["service.web_url"] + filename
                self.inform_user(jid, "Scan this with signal:")
                self.inform_user(jid, img_url)
                await linking_successful
                break
            elif res == "register":
                self.logger.debug(f"User '{jid}' requested to register '{phone}'")
                await self.signald.register(phone)
                code = await self.prompt_user(jid, "Enter SMS verification code")
                # TODO: handle wrong code input…
                await self.signald.verify(phone, code)
                name = await self.prompt_user(
                    jid, "Enter a name for your profile, that other users will see"
                )
                await self.signald.set_profile(phone, name)
                break
            else:
                self.inform_user(jid, "I don't understand")
                await asyncio.sleep(1)

    async def prompt_user(self, jid, message):
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        self.futures[jid] = future
        self.inform_user(jid, message)
        return await future

    def inform_user(self, jid, message):
        self.handle_message(
            user=jid,
            legacy_name=self.config["signal.buddy"],
            message=message,
            nickname="",
        )

    def handle_user_to_spectrum_message(self, user, message):
        self.logger.debug(f"User to spectrum: {message}")
        future = self.futures.pop(user, None)
        self.logger.debug(f"Future: {future}")
        if future is not None:
            future.set_result(message)
        else:
            if message == "groups":
                asyncio.create_task(
                    self.get_rooms(
                        session=self.sessions.get_session(jid=user), inform_user=True
                    )
                )
            else:
                self.inform_user(user, "I do not understand you, my friend.")

    async def get_roster(self, session: Session):
        contacts = await self.signald.list_contacts(username=session.phone)
        for contact in contacts:
            if contact.name is None:
                profile = await self.signald.get_profile(
                    username=session.phone, recipientAddress=contact.address
                )
                self.handle_buddy_changed(
                    user=session.jid,
                    buddy_name=profile.address.number,
                    alias=profile.name,
                    groups=["Signal"],
                    status=spb2.StatusType.STATUS_ONLINE,
                )
            else:
                self.handle_buddy_changed(
                    user=session.jid,
                    buddy_name=contact.address.number,
                    alias=contact.name,
                    groups=["Signal"],
                    status=spb2.StatusType.STATUS_ONLINE,
                )

    async def get_rooms(self, session, inform_user):
        groups = await self.signald.list_groups(session.phone)

        room_list = spb2.RoomList()
        for group in groups:
            room_list.room.append(group.id)
            room_list.name.append(group.title)
            session.real_room_names[group.id.lower()] = group.id

        room_list.user = session.jid
        self.logger.debug(f"Room list:\n{room_list}")
        self.send_wrapped(room_list.SerializeToString(), wm.TYPE_ROOM_LIST)

        if inform_user:
            self.logger.debug("Sending XMPP URIs for groups…")
            for group in groups:
                # escaped = room[0]  # .lower()
                escaped = group.id.lower()
                self.inform_user(
                    jid=session.jid,
                    message=f"You can join the group '{group.title}' at {escaped}, xmpp:{escaped}@{self.jid}?join",
                )

    def handle_logout_request(self, user, legacy_name):
        self.logger.info("Logout")
        self.sessions.remove(phone=legacy_name, jid=user)
        task = asyncio.create_task(self.signald.unsubscribe(phone=legacy_name))
        # FIXME: account data should be removed from signald at this point
        # task.add_done_callback(
        #     lambda: subprocess.call([self.config["signal.remove_account", legacy_name]])
        # )

    def handle_conv_message_payload(self, data):
        payload = spb2.ConversationMessage()
        payload.ParseFromString(data)
        self.logger.debug(f"conv message:{payload}")
        self.handle_message_send_request(
            payload.userName,
            payload.buddyName,
            payload.message,
            payload.xhtml,
            payload.id,
        )

    def handle_message_send_request(self, user, legacy_name, message, xhtml="", mid=0):
        if legacy_name == self.config["signal.buddy"]:
            self.handle_user_to_spectrum_message(user, message)
            return

        self.logger.debug(f"Send message")
        session = self.sessions.get_session(jid=user)
        if session is None:
            self.logger.warning(f"Session not found, not sending message")
            return

        asyncio.create_task(
            self.handle_message_send_request_async(
                session, legacy_name, message, xhtml, mid
            )
        )

    async def handle_message_send_request_async(
        self, session, legacy_name, message, xhtml, mid
    ):
        group = session.real_room_names.get(legacy_name)
        try:
            await self.signald.send_message(
                from_=session.phone,
                to=legacy_name,
                text=message,
                mid=mid,
                group=group,
            )
        except SignaldException as e:
            self.handle_message(
                user=session.jid,
                legacy_name=legacy_name,
                message=f"{e.type} '{e.msg}'",
            )
        else:
            # Self echo of group message.
            if group is not None:
                self.handle_message(
                    user=session.jid,
                    legacy_name=legacy_name,
                    message=message,
                    nickname=session.name,
                )

    def handle_exit_request(self):
        self.logger.info("Exit request")
        self.on_con_lost.set_result(True)

    def handle_vcard_request(self, user, legacy_name, mid):
        asyncio.create_task(
            self.get_vcard(self.sessions.get_session(jid=user), legacy_name, mid)
        )

    async def get_vcard(self, session, legacy_name, mid):
        profile = await self.signald.get_profile(
            phone=session.phone, buddy_phone=legacy_name
        )
        self.handle_vcard(
            user=session.jid,
            mid=mid,
            legacy_name=profile.address.number,
            full_name="",
            nickname=profile.name,
            photo=bytes("", "ascii"),
        )

    def handle_join_room_request(self, user, room, nickname, password):
        asyncio.create_task(self.join_group(user, room, nickname, password))

    async def join_group(self, user, room, nickname, password):
        session = self.sessions.get_session(jid=user)
        try:
            group_id = session.real_room_names[room]
        except KeyError:
            await self.get_rooms(session, inform_user=False)
            group_id = session.real_room_names[room]

        group = await self.signald.get_group(account=session.phone, groupID=group_id)

        for address in group.members:
            if address.number == session.phone:
                # my_address = address
                continue

            profile = await self.signald.get_profile(
                username=session.phone, recipientAddress=address
            )

            self.handle_participant_changed(
                user=session.jid,
                room=room,
                flags=spb2.ParticipantFlag.PARTICIPANT_FLAG_NONE,
                status=spb2.StatusType.STATUS_ONLINE,
                nickname=profile.name,
                alias="",
            )

        self.handle_room_nickname_changed(user=session.jid, r=room, nickname=nickname)
        self.handle_participant_changed(
            user=session.jid,
            nickname=nickname,
            room=room,
            flags=spb2.ParticipantFlag.PARTICIPANT_FLAG_ME,
            status=spb2.StatusType.STATUS_ONLINE,
            alias="",
        )
        self.handle_subject(user=session.jid, legacy_name=room, message=group.title)

    def handle_participant_changed(
        self,
        user,
        nickname,
        room,
        flags,
        status,
        alias,
        status_message="",
        newname="",
        icon_hash="",
    ):
        d = spb2.Participant()
        d.userName = user
        d.nickname = nickname
        d.room = room
        d.flag = flags
        d.newname = newname
        d.iconHash = icon_hash
        d.status = status
        d.statusMessage = status_message
        d.alias = alias
        self.logger.debug(f"Participant changed\n{d}")
        self.send_wrapped(d.SerializeToString(), wm.TYPE_PARTICIPANT_CHANGED)

    def handle_room_nickname_changed(self, user, r, nickname):
        room = spb2.Room()
        room.userName = user
        room.nickname = nickname
        room.room = r
        room.password = ""
        self.logger.debug(f"Nickname changed\n{room}")
        self.send_wrapped(room.SerializeToString(), wm.TYPE_ROOM_NICKNAME_CHANGED)

    def handle_leave_room_request(self, user, room):
        self.logger.info(f"Leave room '{room}' request for user '{user}'")

    def copy_file(self, attachment):
        self.logger.debug(f"Handling attachemnt {attachment}")
        path = Path(attachment["storedFilename"])
        id_ = attachment["id"]

        web_dir = Path(self.config["service.web_directory"])
        new_dir = web_dir / id_
        new_dir.mkdir()

        new_path = new_dir / id_

        content_type = attachment.get("contentType").lower()
        if "jpeg" in content_type:
            new_path = new_path.with_suffix(".jpg")
        elif "gif" in content_type:
            new_path = new_path.with_suffix(".gif")
        elif "png" in content_type:
            new_path = new_path.with_suffix(".png")

        shutil.copy(path, new_path)

        url = self.config["service.web_url"] + id_ + "/" + new_path.parts[-1]
        return url


def qr_encode(text, filename):
    subprocess.call(["qrencode", text, "-o", filename])
