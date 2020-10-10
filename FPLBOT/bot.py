from discord.ext import commands
import discord
from discord.ext.commands import CommandNotFound
from dotenv import load_dotenv
import os 
import sys
import aiohttp
import asyncio
load_dotenv()
client=commands.Bot(command_prefix='pl!')

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name="$help"))


client.load_extension('cogs.fpl')

client.run(os.getenv("discord_token"))
