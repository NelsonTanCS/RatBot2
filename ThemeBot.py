# client id 592850011256127518
# permissions 67584
# https://discordapp.com/api/oauth2/authorize?client_id=592850011256127518&scope=bot&permissions=8

import discord
from discord.ext import commands
import random
import os
import json

# get config file
current_dir = os.path.dirname(__file__)
with open(os.path.join(current_dir, 'config.json')) as config_file:
    config = json.load(config_file)

# define bot
dev_mode = False  # sets default text channel to a private one so it doesn't spam the main one
client = commands.Bot(command_prefix=config['prefix'], case_insensitive=True)
theme = config['theme']
my_guild_id = config['guild_id']
admin_role_id = config['admin_role_id']
default_role_id = config['default_role_id']
if dev_mode:
    my_channel_id = 594000152025366534  # private bot channel
else:
    my_channel_id = config['channel_id']  # default channel the bot will send messages to and edit the name of
color = 0x00ff00  # color for embedded message border


@client.event
async def on_ready():
    """ sets the bot's rich presence on start """
    print(my_channel_id)
    activity = discord.Activity(name=theme + "-related activities", type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)
    embed = discord.Embed(title=f"{theme.capitalize()}s, we back once a-muhfuggin-gain", color=color)
    await client.get_channel(my_channel_id).send(embed=embed)
    print(f"we have logged in as {client.user}")
    print("current theme is " + theme)


# TODO: bot doesn't disconnect immediately so this message doesn't send
@client.event
async def on_disconnect():
    """ when bot goes offline """
    embed = discord.Embed(title=f"lata {theme}s", color=color)
    await client.get_channel(my_channel_id).send(embed=embed)


@client.event
async def on_message(message):
    """ reacts to any message containing the word {theme} with the :rad: custom emoji
        bot responds when message stars with !{theme}"""
    guild = client.get_guild(my_guild_id)

    if message.author == client.user:
        return

    if message.content.startswith(f"!{theme}"):
        embed = discord.Embed(title=f":rat: rat {theme} :rat:", color=color)
        await message.channel.send(embed=embed)

    if theme in message.content.lower():
        emoji = discord.utils.get(guild.emojis, name="rad")
        if (emoji):
            await message.add_reaction(emoji)

    await client.process_commands(message)


@client.event
async def on_member_join(member):
    """ sets member nickname to "new {theme}", adds {theme}s as their role, and sends a message """
    channel = client.get_channel(my_channel_id)
    role = client.get_guild(my_guild_id).get_role(default_role_id)  # default role id
    embed = discord.Embed(title=f"Hey {member.name}, imagine being a new {theme.upper()}", color=color)
    await channel.send(embed=embed)
    await member.edit(nick="new " + theme)
    await member.add_roles(role)


@client.event
async def on_member_update(before, after):
    """ sets nickname to {theme} if {theme} is not in their nickname.
        bot cannot change nickname of owner """
    guild = client.get_guild(my_guild_id)
    if theme not in after.nick.lower():
        try:
            await after.edit(nick=f"{after.nick} {theme}")
        except:
            print(before.name + " didn't want to edit nickname")


@client.command(aliases=["changetheme", "ct", "tc"])
async def themechange(ctx, new_theme: str):
    """changes the theme including nicknames, server name, role names, one text channel, and one voice channel"""
    # channel = client.get_channel(my_channel_id)
    embed = discord.Embed(title=f"Changing theme to {new_theme}. Don't change theme again until I'm done >:(", color=color)
    working_message = await ctx.send(embed=embed)
    before_theme = config['theme']
    global theme
    if new_theme == "random":
        themes = config['all_themes']
        rand_int = random.randint(0, len(themes) - 1)
        theme = themes[rand_int]
    else:
        theme = new_theme
        config['all_themes'].append(theme)
        with open('config.json', 'w') as f:
            json.dump(config, f)

    config['theme'] = theme
    with open('config.json', 'w') as f:
        json.dump(config, f)

    guild = client.get_guild(my_guild_id)
    await guild.edit(name=theme + " world")

    members = guild.members
    text_channels = guild.text_channels
    voice_channels = guild.voice_channels

    for member in members:
        if member.id != guild.owner_id:
            nickname = str(member.nick).replace(before_theme, theme)
            await member.edit(nick=nickname)

    await text_channels[0].edit(name=theme)
    await voice_channels[0].edit(name=theme + " bois")

    activity = discord.Activity(name=theme + "-related activities", type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)

    await guild.get_role(admin_role_id).edit(name=f"not {theme}")  # admin role
    await guild.get_role(default_role_id).edit(name=f"{theme}s")  # default role

    print("theme changed to " + theme)
    await working_message.delete()
    embed = discord.Embed(title=f"Theme changed to {theme}", color=color)
    await ctx.send(embed=embed)


@client.command()
async def printtheme(ctx):
    """Prints the current theme"""
    await ctx.send(theme)

client.run(config['token'])
