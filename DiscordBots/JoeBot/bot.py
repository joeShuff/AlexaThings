import asyncio
import discord
import random
import os
import urllib
from urllib import request
import json
import time
cwd = os.getcwd()

client = discord.Client()
# client = commands.Bot(command_prefix="!")

gifs = ['https://cdn.discordapp.com/attachments/380862354407292930/402406738965430282/giphy.gif',
        'https://cdn.discordapp.com/attachments/380862354407292930/402407182777450497/giphy.gif',
        'https://cdn.discordapp.com/attachments/380862354407292930/402407630380728320/giphy.gif',
        'https://cdn.discordapp.com/attachments/380862354407292930/402408270897217536/giphy.gif']

name_map = {"lick":"6.gif"}

current_milli_time = lambda: int(round(time.time() * 1000))

@client.event
async def on_ready():
    print("on READY")
    await client.change_presence(game=discord.Game(name='I WANT TO DIE'))

async def send_message(channel, message):
    await client.send_message(channel, message)

async def on_command(command, args):
    pass

async def get_kewt_kitty(channel):

    try:
        filename = str(current_milli_time()) + ".jpg"

        urllib.request.urlretrieve("http://thecatapi.com/api/images/get?format=src", cwd + "/cattos/" + filename)

        messages = ['the best catto', 'omg so kewt', 'this is :ok_hand:', '*meow*',
                    'omg I want this catto']

        await send_message(channel, random.choice(messages))
        await client.send_file(channel, cwd + "/cattos/" + filename)
    except:
        get_kewt_kitty(channel)

async def get_good_boi(channel):
    request = urllib.request.Request("https://dog.ceo/api/breeds/image/random")
    response = urllib.request.urlopen(request)

    tojson = str(response.read()).replace("\\", "").replace("'", "")[1:]
    print(tojson)

    jsonresponse = json.loads(tojson)

    url = jsonresponse['message']

    filename = url.split("/")
    filename = filename[len(filename) - 1]

    print(filename)

    urllib.request.urlretrieve(url, cwd + "/doggos/" + filename)

    messages = ['This one is a good boi', 'omg so kewt', 'this is a :ok_hand: doggo', '*woof bork*', 'omg I want a doggo']

    await send_message(channel, random.choice(messages))
    await client.send_file(channel, cwd + "/doggos/" + filename)

@client.event
async def on_message(message):

    print(message.content)

    # Respond to mentions
    mentionReplies = ['lets fite',"don't make me come over there and fuk u up","I will fuckin kick you m9","You are doing my tits in","Let's take this beef outside",'Hey, fuck you',"Mention me again, and i'll shank ya"]
    if ('<@402394931836092434>' in message.content):
        await send_message(message.channel, random.choice(mentionReplies))
        return

    if (message.content.lower().startswith("gimme joe")):
        comm = message.content.lower()

        if (comm.replace("gimme joe", "").strip() == ""):
            await client.send_file(message.channel, cwd + "/" + str(random.randint(1, 6)) + ".gif")
        else:
            extra = comm.replace("gimme joe", "").strip()

            if extra in name_map:
                await client.send_file(message.channel, cwd + "/" + name_map[extra])
            else:
                await client.send_message(message.channel, "That is not a gif I have you autist. Have a random one")
                await client.send_file(message.channel, cwd + "/" + str(random.randint(1, 6)) + ".gif")

    elif (message.content.lower().startswith("gimme goodboi")):
        await send_message(message.channel, "choosing the perfect goodboi")
        await get_good_boi(message.channel)

    elif (message.content.lower().startswith("gimme catto")):
        await send_message(message.channel, "trying to find kewtest catto")
        await get_kewt_kitty(message.channel)
    elif (message.content.lower().startswith("gimme")):
        messages = ['make ya fuckin mind up', 'you undecisive silly cunt', 'ran out of that', "my god, I wish you'd die"]
        await send_message(message.channel, random.choice(messages))

client.run("NDAyMzk0OTMxODM2MDkyNDM0.DUChew.OqybbqhxvpHazN8COYmbQdGm4rg")