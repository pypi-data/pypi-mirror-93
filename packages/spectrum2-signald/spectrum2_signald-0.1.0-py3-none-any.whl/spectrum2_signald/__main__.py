from argparse import ArgumentParser
import asyncio
import logging
import logging.handlers
import socket
import json
import pprint
import random
import sys
import subprocess
import shutil
import re

from spectrum2 import Config

from spectrum2_signald.spectrum2 import SignalBackend


def get_logging_handler():
    """This doesn't properly implement log4j config file, but it's a start"""
    # I did not find a better way to handle the dot in the command line arguments
    backend_id = vars(args)["service.backend_id"]

    filename = (
        config["log4j.appender.R.File"]
        .replace("${jid}", args.jid)
        .replace("${id}", str(backend_id))
    )

    maxbytes_string = config["log4j.appender.R.MaxFileSize"]
    maxbytes_number = re.findall(r"\d+", maxbytes_string)[0]
    maxbytes_unit = maxbytes_string.replace(maxbytes_number, "")

    maxbytes = int(maxbytes_number) * HUMAN_SIZES[maxbytes_unit]

    handler = logging.handlers.RotatingFileHandler(
        filename,
        maxBytes=maxbytes,
        backupCount=int(config["log4j.appender.R.MaxBackupIndex"]),
    )

    # TODO: convert log4j format
    formatter = logging.Formatter(
        "%(asctime)s:[%(process)d]:%(levelname)s:%(name)s:%(message)s", "%b %d %H:%M:%S"
    )

    handler.setFormatter(formatter)

    return handler


def configure_logger(logger):
    logging_handler = get_logging_handler()
    logger.addHandler(logging_handler)
    logger.setLevel(LOGGING_LEVEL)


async def main():
    logger = logging.getLogger()
    configure_logger(logger)
    logger.info("Starting spectrum2-signald…")
    loop = asyncio.get_running_loop()

    _, spectrum2 = await loop.create_connection(
        lambda: SignalBackend(SIGNALD_SOCKET_PATH, args.jid, args.CONFIG),
        host=args.host,
        port=args.port,
    )

    await spectrum2.on_con_lost
    logger.info("One of the connections was lost or exit was requested.")
    sys.exit(0)


HUMAN_SIZES = {"": 1, "KB": 1024, "MB": 1024 ** 2, "GB": 1024 ** 3}

parser = ArgumentParser()
parser.add_argument("--host")
parser.add_argument("--port", type=int)
parser.add_argument("--service.backend_id", type=int)
parser.add_argument("--jid", "-j")
parser.add_argument("CONFIG")
args = parser.parse_args()

config = Config(args.CONFIG)
LOGGING_LEVEL = getattr(logging, config["log4j.rootLogger"].split(",")[0].upper())
DEVICE_NAME = config["signal.device_name"]
SIGNALD_SOCKET_PATH = config["signal.socket"]
SPECTRUM2_USERNAME = config["signal.buddy"]
SEND_ROOM_LIST_TO_USER = config["signal.send_room_list_to_user"]

asyncio.run(main())
