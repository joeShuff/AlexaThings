import asyncio
import discord
import random
import os
cwd = os.getcwd()

client = discord.Client()
# client = commands.Bot(command_prefix="!")

gifs = ['https://cdn.discordapp.com/attachments/380862354407292930/402406738965430282/giphy.gif',
        'https://cdn.discordapp.com/attachments/380862354407292930/402407182777450497/giphy.gif',
        'https://cdn.discordapp.com/attachments/380862354407292930/402407630380728320/giphy.gif',
        'https://cdn.discordapp.com/attachments/380862354407292930/402408270897217536/giphy.gif']

name_map = {"lick":"6.gif"}

@client.event
async def on_ready():
    print("on READY")
    await client.change_presence(game=discord.Game(name='I WANT TO DIE'))

async def send_message(channel, message):
    await client.send_message(channel, message)

@client.event
async def on_message(message):
    if (message.content.lower().startswith("gimme joe")):

        comm = message.content.lower()

        if (comm.replace("gimme joe", "").strip() == ""):
            await client.send_file(message.channel, cwd + "/" + str(random.randint(1, 7)) + ".gif")
        else:
            extra = comm.replace("gimme joe", "").strip()

            if extra in name_map:
                await client.send_file(message.channel, cwd + "/" + name_map[extra])
            else:
                await client.send_message(message.channel, "That is not a gif I have you autist. Have a random one")
                await client.send_file(message.channel, cwd + "/" + str(random.randint(1, 7)) + ".gif")
    elif (message.content.lower().startswith("gimme a way to die")):
        await send_message(message.channel, "cheeky twat")
    elif (message.content.lower().startswith("show me da wae")):
        await send_message(message.channel, "fuck off with your old memes")
    elif ("cunt" in message.content):
        await send_message(message.channel, "who are you calling a CUNT ya saggy granny tit")

client.run("")