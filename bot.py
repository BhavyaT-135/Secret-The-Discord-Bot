import discord
import random
import os
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle
from datetime import datetime
import time
import json
import re
from discord.ext import commands
import pkg_resources
import asyncio

client = commands.Bot(command_prefix='*')
status = cycle(['Scrabble', 'Chess'])
players = {}


@client.event
async def on_ready():
    # activity=discord.Game('Scrabble'))
    await client.change_presence(status=discord.Status.idle)
    change_status.start()
    print("Bot is ready!")


@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')


@client.event
async def on_member_remove(member):
    print(f'{member} has left a server.')


@client.command()
async def ping(ctx):
    '''
    - Returns the Bot's response time.
    '''
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


# general error handler
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
        # await ctx.send('Invalid command used.')


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    '''
    - Delete specified number of messages.
    '''
    await ctx.channel.purge(limit=amount)


# specific error handler
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify an amount of messages to delete.')


@client.command()
# @commands.check(is_it_me)
async def user(ctx):
    '''
    - Returns the username.
    '''
    await ctx.send(f'Hi! I am {ctx.author}')


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    '''
    - Kick members from the server.
    '''
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention}')


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    '''
    - Ban members from the server.
    '''
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')


@client.command()
async def unban(ctx, *, member):
    '''
    - Unban banned members from the server.
    '''
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)

            await ctx.send(f'Unbanned {user.name}#{user.discriminator}')
            # same as ctx.send(f'Banned {user.mention}')
            return


@tasks.loop(seconds=200)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

# Insert Your Token Here (Discord Developer Portal: https://discord.com/developers/applications)
client.run("")
