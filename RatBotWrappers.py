# client id 592850011256127518
# permissions 67584
# https://discordapp.com/api/oauth2/authorize?client_id=592850011256127518&scope=bot&permissions=8

import discord
from discord.ext import commands

commandPrefix = '!'
bot = commands.Bot(command_prefix=commandPrefix)

client = discord.Client()
token = open("token.txt", "r").read()


@client.event  # event decorator/wrapper
async def on_ready():
    print(f"we have logged in as {client.user}")


@client.event
async def on_message(message):
    guild = client.get_guild(354846043336343553)

    if message.author == client.user:
        return

    if f"{commandPrefix}rat" in message.content.lower():
        await message.channel.send(":rat: fuckin RAT :rat:")

    # print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")


@client.event
async def on_member_join(member):
    await member.channel.send("imagine being a new RAT")
    await member.edit(nick="new rat", roles="rats")


client.run(token)
