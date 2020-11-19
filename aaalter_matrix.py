#!/usr/bin/env python3
import asyncio
import logging
import re

from nio import InviteEvent, RoomMessageText, AsyncClient

from hopfenmatrix.callbacks import auto_join, Callback
from hopfenmatrix.client import new_async_client
from hopfenmatrix import run
from hopfenmatrix.config import Config

logger = logging.getLogger(__name__)


def receive_message(client: AsyncClient) -> Callback:

    async def callback(room, event) -> None:
        msg = event.body

        if event.sender == client.user:
            return

        logger.debug(
            f"Bot message received for room {room.display_name} | "
            f"{room.user_name(event.sender)}: {msg}"
        )
        await process(client, room, msg)

    return callback


async def process(client, room, msg):
    """Process the command"""
    pattern_alter = re.compile(r'\b[a]+lter\b', re.IGNORECASE)
    matches_alter = pattern_alter.findall(msg)
    for match_alter in matches_alter:
        await _alter(client, room, match_alter)
    pattern_porsche = re.compile(r'\b((j[a]+wo(h?)[l]+)|porsche|cayman)\b', re.IGNORECASE)
    matches_porsche = pattern_porsche.findall(msg)
    if len(matches_porsche) > 0:
        await _porsche(client, room)


async def _alter(client, room, txt):
    await client.room_send(
        room.room_id,
        "m.room.message",
        {
            "msgtype": "m.text",
            "body": f"{''.join([x * 2 for x in txt if x in ['a', 'A']])}{txt[-4:]}{(txt.lower().count('a')) * '!'}"
        },
        ignore_unverified_devices=True
    )


async def _porsche(client, room):
    await client.room_send(
        room.room_id,
        "m.room.message",
        {
            "msgtype": "m.text",
            "body": f"PORSCHE CAYMAN S JUNGS\nJAWOLL JAAAAA!"
        },
        ignore_unverified_devices=True
    )


async def main():
    config = Config().from_json("config.json")

    client = new_async_client(config)
    client.add_event_callback(auto_join(client), InviteEvent)
    client.add_event_callback(receive_message(client), RoomMessageText)

    await run.run(client, config)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
