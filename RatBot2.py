# client id 592850011256127518
# permissions 67584
# https://discordapp.com/api/oauth2/authorize?client_id=592850011256127518&scope=bot&permissions=67584

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='>')

client = discord.Client()
token = open("token.txt", "r").read()

@client.event # event decorator/wrapper
async def on_ready():
    print(f"we have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "rat" in message.content.lower():
        await message.channel.send("fuckin RAT")

    # print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
client.run(token)
