# client id 592850011256127518
# permissions 67584
# https://discordapp.com/api/oauth2/authorize?client_id=592850011256127518&scope=bot&permissions=8

import discord
from discord.ext import commands
# from discord.ext.commands import Bot

commandPrefix = '!'
Client = discord.Client()
client = commands.Bot(command_prefix=commandPrefix)
token = open("token.txt", "r").read()
theme = open("theme.txt", "r").read()
my_guild_id = 354846043336343553
#TODO: Add new themes to all_themes.txt and let "random" be an argument to themechange

# sets the bot's rich presence
@client.event
async def on_ready():
    activity = discord.Activity(name=theme + "-related activities", type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)
    print(f"we have logged in as {client.user}")
    print("current theme is " + theme)


# reacts to any message containing the word "rat" with the :rad: custom emoji
@client.event
async def on_message(message):
    guild = client.get_guild(my_guild_id)

    if message.author == client.user:
        return

    if f"!{theme}" in message.content:
        await message.channel.send(f":rat: dumb {theme} :rat:")

    if theme in message.content.lower():
        emoji = discord.utils.get(guild.emojis, name="rad")
        if (emoji):
            await message.add_reaction(emoji)

    await client.process_commands(message)

    # print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")


# sets member nickname to "new rat", adds "rats" as their role, and sends a messsage
@client.event
async def on_member_join(member):
    channel = client.get_channel(354846043336343554) # default channel id
    role = client.get_role(593639732127334410) # default role id
    await channel.send("imagine being a new " + theme)
    await member.edit(nick="new " + theme)
    await member.add_roles(role)


# sets nickname to "rat" if "rat" is not in their nickname
# bot cannot change nickname of owner
@client.event
async def on_member_update(before, after):
    guild = client.get_guild(my_guild_id)
    if before.id != guild.owner_id and theme not in after.nick:
        try:
            await after.edit(nick=theme)
        except:
            print(before)


@client.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


# changes the theme including nick names, server name, role names, one text channel, and one voice channel
@client.command()
async def themechange(ctx, after_theme: str):
    before_theme = open("theme.txt", "r").read()
    open("theme.txt", "w").write(after_theme)
    global theme
    theme = after_theme
    guild = client.get_guild(354846043336343553)
    await guild.edit(name=after_theme + " world")

    members = guild.members
    text_channels = guild.text_channels
    voice_channels = guild.voice_channels
    roles = guild.roles
    for member in members:
        if member.id != guild.owner_id:  # TODO: find a way to edit owner nickname
            nickname = str(member.nick).replace(before_theme, after_theme)
            await member.edit(nick=nickname)

    await text_channels[0].edit(name=after_theme)
    await voice_channels[0].edit(name=after_theme + " bois")
    activity = discord.Activity(name=theme + "-related activities", type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)
    for role in roles:  # TODO: if role is a bot role, skip
        try:
            await role.edit(name=role.name.replace(before_theme, after_theme))
        except:
            print(role)

    print("theme changed to " + theme)


client.run(token)
