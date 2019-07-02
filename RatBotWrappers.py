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
theme = "bonobo"


# sets the bots rich presence
@client.event
async def on_ready():
    activity = discord.Activity(name=theme + "-related activities", type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)
    print(f"we have logged in as {client.user}")


# reacts to any message containing the word "rat" with the :rad: custom emoji
@client.event
async def on_message(message):
    guild = client.get_guild(354846043336343553)

    if message.author == client.user:
        return

    if "!theme_change" in message.content:
        parameters = message.content.split()
        before_theme = parameters[1]
        after_theme = parameters[2]
        guild = client.get_guild(354846043336343553)
        await guild.edit(name=after_theme + " world")

        members = guild.members
        text_channels = guild.text_channels
        voice_channels = guild.voice_channels
        roles = guild.roles
        for member in members:
            if member.id != 348315506417336321:
                nickname = str(member.nick).replace(before_theme, after_theme)
                await member.edit(nick=nickname)

        await text_channels[0].edit(name=after_theme)
        await voice_channels[0].edit(name=after_theme + "bois")
        for role in roles:
            await role.edit(name=role.name.replace(before_theme, after_theme))

    if theme in message.content.lower():
        emoji = discord.utils.get(guild.emojis, name="rad")
        if (emoji):
            await message.add_reaction(emoji)

    await client.process_commands(message)

    # print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")


# sets member nickname to "new rat", adds "rats" as their role, and sends a messsage
@client.event
async def on_member_join(member):
    channel = client.get_channel(354846043336343554)
    role = client.get_role(593639732127334410)
    await channel.send("imagine being a new " + theme)
    await member.edit(nick="new " + theme)
    await member.add_roles(role)


# sets nickname to "rat" if "rat" is not in their nickname
@client.event
async def on_member_update(before, after):
    if theme not in after.nick:
        await after.edit(nick=theme)


# ping pong method
@client.command()
async def rat(ctx):
    await ctx.send(f":rat: dumb {theme} :rat:")


# creates a group call with all users in the given voice channel
@client.command()
async def groupcall(ctx, channel: discord.VoiceChannel, client_user: discord.ClientUser):

    print(channel)
    members = channel.members
    user_list = []
    print("Members")
    for member in members:
        user_list.append(client.get_user(member.id))
        print(member)
    print("Users")
    for user in user_list:
        print(user)

    await client_user.create_group(user_list)

    # guild = client.get_guild(354846043336343553)
    #
    # if channel in client.get_all_channels():
    #     members = guild.get_channel()


@client.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


# changes the theme including nick names, server name, role names, one text channel, and one voice channel
@client.command()
async def themechange(ctx, before_theme: str, after_theme: str):
    guild = client.get_guild(354846043336343553)
    members = guild.members
    text_channels = guild.text_channels
    voice_channels = guild.voice_channels
    roles = guild.roles
    for member in members:
        nickname = member.nick.replace(before_theme, after_theme)
        await member.edit(nick=nickname)

    await text_channels[0].edit(name=after_theme)
    await voice_channels[0].edit(name=after_theme + "bois")
    for role in roles:
        await role.edit(name=role.name.replace(before_theme, after_theme))

    await guild.edit(name=after_theme + " world")


client.run(token)
