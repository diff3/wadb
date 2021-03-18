#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Bot for connecting Discord and Alpha-core emulator

Written by Entropy 2021

TODO: Make database independen from Alpha Core
"""

from emulators.alpha_core import Alpha
import asyncio
import discord
from dotenv import load_dotenv
import os


INTERVAL = 60

load_dotenv()
client = discord.Client()

TOKEN = os.getenv('DISCORD_TOKEN')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # if not message.is_private:
    #   return

    if message.guild:
        return

    if '!account' in message.content:
        response = Alpha.account_create(message)
        await message.author.send(response)

    elif '!delete' in message.content:
        response = Alpha.account_delete(message)
        await message.author.send(response)

    elif message.content == '!help':
        response = Alpha.help_text()
        await message.author.send(response)

    elif '!list' in message.content:
        response = Alpha.account_list(message)
        await message.author.send(response)

    elif message.content == '!online':
        response = Alpha.who_is_online()
        await message.author.send(response)

    elif '!password' in message.content:
        response = Alpha.account_password(message)
        await message.author.send(response)

    elif message.content == '!weather':
        response = Alpha.curent_weather()
        await message.author.send(response)

    else:
        response = Alpha.help_text()
        await message.author.send(response)


async def send_interval_message():
    print('Interval loop active')
    await client.wait_until_ready()

    while True:
        await asyncio.sleep(INTERVAL)

        msg = Alpha.num_player_online()
        if '0' not in msg:
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=msg)) # noqa
        else:
            await client.change_presence(activity=None, status=None, afk=False)


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    await client.change_presence(activity=None, status=None, afk=False)
    client.loop.create_task(send_interval_message())


client.run(TOKEN)
