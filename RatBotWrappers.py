# client id 592850011256127518
# permissions 67584
# https://discordapp.com/api/oauth2/authorize?client_id=592850011256127518&scope=bot&permissions=8

import discord
from discord.ext import commands
import random
import atexit
# from discord.ext.commands import Bot

Client = discord.Client()
client = commands.Bot(command_prefix=">", case_insensitive=True)
token = open("token.txt", "r").read()
theme = open("theme.txt", "r").readline()
my_guild_id = 354846043336343553
my_channel_id = 354846043336343554  # default channel the bot will send messages to and edit the name of
color = 0x00ff00


@client.event
async def on_ready():
    """ sets the bot's rich presence on start """
    activity = discord.Activity(name=theme + "-related activities", type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)
    embed = discord.Embed(title=f"{theme.capitalize()}s, we back once a-muhfuckin-gain", color=color)
    await client.get_channel(354846043336343554).send(embed=embed)
    print(f"we have logged in as {client.user}")
    print("current theme is " + theme)



@client.event
async def on_disconnect():
    """ when bot goes offline """
    embed = discord.Embed(title=f"lata {theme}s")
    await client.get_channel(354846043336343554).send(embed=embed, color=color)


@client.event
async def on_message(message):
    """ reacts to any message containing the word {theme} with the :rad: custom emoji """
    guild = client.get_guild(my_guild_id)

    if message.author == client.user:
        return

    if f"!{theme}" in message.content:
        embed = discord.Embed(title=f":rat: dumb {theme} :rat:", color=color)
        await message.channel.send(embed=embed)

    if theme in message.content.lower():
        emoji = discord.utils.get(guild.emojis, name="rad")
        if (emoji):
            await message.add_reaction(emoji)

    await client.process_commands(message)

    # print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")


@client.event
async def on_member_join(member):
    """ sets member nickname to "new rat", adds "rats" as their role, and sends a messsage """
    channel = client.get_channel(my_channel_id)
    role = client.get_guild(my_guild_id).get_role(593639732127334410)  # default role id
    embed = discord.Embed(title=f"Hey {member.name}, imagine being a new {theme.upper()}", color=color)
    await channel.send(embed=embed)
    await member.edit(nick="new " + theme)
    await member.add_roles(role)


@client.event
async def on_member_update(before, after):
    """ sets nickname to {theme} if {theme} is not in their nickname
        bot cannot change nickname of owner """
    guild = client.get_guild(my_guild_id)
    if (not before.bot) and theme not in after.nick:  # TODO: find out what "NoneType is not iterable" means
        try:
            await after.edit(nick=theme)
        except:
            print(before)


@client.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@client.command(aliases=["changetheme", "ct", "tc"])
async def themechange(ctx, new_theme: str):
    """changes the theme including nicknames, server name, role names, one text channel, and one voice channel"""
    before_theme = open("theme.txt", "r").read()
    global theme
    if new_theme == "random":  # TODO: finish this
        themes = open("all_themes.txt", "r")
        themes_list = themes.readlines()
        rand_int = random.randint(0, len(themes_list) - 1)
        theme = themes_list[rand_int]
        themes.close()
    else:
        theme = new_theme
        open("all_themes.txt", "a").write("\n" + new_theme)

    open("theme.txt", "w").write(theme)
    guild = client.get_guild(354846043336343553)
    await guild.edit(name=theme + " world")

    members = guild.members
    text_channels = guild.text_channels
    voice_channels = guild.voice_channels
    roles = guild.roles
    for member in members:
        if member.id != guild.owner_id:  # TODO: find a way to edit owner nickname
            nickname = str(member.nick).replace(before_theme, theme)
            await member.edit(nick=nickname)

    await text_channels[0].edit(name=theme)
    await voice_channels[0].edit(name=theme + " bois")
    activity = discord.Activity(name=theme + "-related activities", type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)
    for role in roles:  # TODO: if role is a bot role, skip
        try:
            await role.edit(name=role.replace(before_theme, theme))
        except:
            print(role)

    print("theme changed to " + theme)
    embed = discord.Embed(title=f"Theme changed to {theme}", color=color)
    channel = client.get_channel(my_channel_id)
    await channel.send(embed=embed)


@client.command()  # TODO: method that adds a theme to a server that has no previous theme
async def nuke(new_theme: str):
    print(f"theme nuke: {new_theme}")

client.run(token)
