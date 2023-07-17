import discord
from discord.ext import commands
import asyncio
import os
from webserver import keep_alive

TOKEN = os.environ['TOKEN']
my_secret = os.environ['TOKEN']
bot_prefix = '.'

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=bot_prefix, intents=intents)

raid_threshold = 10  # threshold is like...people joining together make it as threads like how many accs join together like 10 in 60 seconds. easy bro.
join_time_limit = 60  # join time limit (in seconds) for raid detection. mind you its seconds not minutes so ye.

join_times = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@bot.event
async def on_member_join(member):
    guild = member.guild
    num_members = len(guild.members)

    if num_members > raid_threshold:
        join_times[member.id] = member.joined_at.timestamp()
        await asyncio.sleep(join_time_limit)

        if member.id in join_times:
            del join_times[member.id]
        else:
            await member.kick(reason='Server raid protection')

@bot.event
async def on_member_remove(member):
    if member.id in join_times:
        del join_times[member.id]

keep_alive()
bot.run(TOKEN)
