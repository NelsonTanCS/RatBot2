# client id 592850011256127518
# permissions 67584
# https://discordapp.com/api/oauth2/authorize?client_id=592850011256127518&scope=bot&permissions=8

import discord
from discord.ext import commands

commandPrefix = '!'
bot = commands.Bot(command_prefix=commandPrefix)


class RatClient(discord.Client):

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    #
    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if f"{commandPrefix}rat" in message.content.lower():
            await message.channel.send(":rat: fuckin RAT :rat:")

    async def on_member_join(self, member):
        await member.channel.send("imagine being a new RAT")
        await member.edit(nick="new rat", roles="rats")


client = RatClient()
guild = client.get_guild(354846043336343553)
token = open("token.txt", "r").read()
client.run(token)