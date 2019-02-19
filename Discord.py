#!/usr/bin/env python3
import discord
import asyncio
import socket
import json

# ----   Configuration   ---- # 
token = "discordTokenNeeded"


# ---- Documentation Links -- #
# http://discordpy.readthedocs.io/en/latest/api.html#client

# -- End Documentation Links -#

client = discord.Client()
@client.event
async def on_ready():
	"""When the client firsts connects to discord."""
	print(client.get_all_members())
	members = client.get_all_members()
	for m in members:
		print("on ready " + m.display_name)
	pass
@client.event
async def on_message(message):
	"""What happens when a message is recieved on IRC."""
	print("<{}> [{}]: {}".format(message.channel, message.author.display_name, message.content))
	nick = message.author.display_name.replace(" ", "_") + "[D]"
client.run(token)