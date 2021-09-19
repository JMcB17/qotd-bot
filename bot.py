#!/usr/bin/env python3


import json
import discord
from discord.ext import commands


__version__ = '0.1.0b'


CONFIG_PATH = 'config.json'
PIN_LIMIT = 50


class QotdBot(commands.Bot):
    def __init__(self, options: dict, *args, **kwargs):
        self.options = options
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'Started as {self.user.name}.')

    async def on_message(self, message: discord.Message):
        if (
            message.channel.id == self.options['channel_id']
            and self.options['role_id'] in [role.id for role in message.author.roles]
        ):
            pins = await message.channel.pins()
            if len(pins) >= PIN_LIMIT:
                await pins[-1].unpin(reason='Auto unpinned by Qotd Bot when pin limit reached.')

            await message.pin(reason='Auto pinned by Qotd Bot.')

            if self.options['ping_id']:
                ping_role: discord.Role = message.guild.get_role(self.options['ping_id'])
                if ping_role is not None:
                    await message.reply(content=ping_role.mention, mention_author=False)

        await super().on_message(message)


def main():
    with open(CONFIG_PATH) as config_file:
        config = json.load(config_file)

    qotd_bot = QotdBot(options=config['options'], command_prefix='!')
    qotd_bot.run(config['token'])


if __name__ == '__main__':
    main()
