import re

from .chat_functions import send_text_to_room


class Command(object):
    def __init__(self, client, store, config, command, room, event):
        """A command made by a user

        Args:
            client (nio.AsyncClient): The client to communicate to matrix with

            store (Storage): Bot storage

            config (Config): Bot configuration parameters

            command (str): The command and arguments

            room (nio.rooms.MatrixRoom): The room the command was sent in

            event (nio.events.room_events.RoomMessageText): The event describing the command
        """
        self.client = client
        self.store = store
        self.config = config
        self.command = command
        self.room = room
        self.event = event
        self.args = self.command.split()[1:]

    async def process(self):
        """Process the command"""
        pattern = re.compile(r'\b[a]+lter\b', re.IGNORECASE)
        matches = pattern.findall(self.command)
        for match in matches:
            await self._alter(match)

    async def _alter(self, txt):
        await send_text_to_room(
            self.client,
            self.room.room_id,
            f"{''.join([x*2 for x in txt if x in ['a','A']])}{txt[-4:]}{(txt.lower().count('a'))*'!'}",
        )
