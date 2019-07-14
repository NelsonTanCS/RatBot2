# ThemeBot
Discord bot originally made for Discord Hack Week 2019 for the "Something Silly" category. 
This bot converts an entire Discord server to conform to a single "theme" word.

## Running ThemeBot
1. Clone this repository.
2. Fill out `config_template.json` with your token, command prefix, and guild IDs.
3. `pip install discord.py`
4. `python Themebot.py`

## Commands
* `themechange/changetheme/tc/ct [theme]` Changes the theme. This includes changing the server name, first text channel name, first voice channel name, admin role name, default role name, and all nicknames of users. If there is a previous theme, only replaces the previous theme word from nicknames with the new theme word.
* `themechange random` Changes the theme to a random theme that has been changed to before.
* `[theme]` This command changes with the theme. The bot will respond with a message.

## Features
* New members will automatically be named the theme and moved to the default role.
* Members who attempt to change their nickname to something that does not contain the theme will be changed back to the theme.
* Reacts to messages containing the theme with a custom emoji.
