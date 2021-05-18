import discord
import pipe
import os
import meets
from dotenv import load_dotenv
from datetime import datetime
from discord.ext import tasks

load_dotenv()
TOKEN = os.getenv('discord_secret')
client = discord.Client()

prefix = '='

now = datetime.now()
current_time = now.strftime("%H:%M:%S")


@client.event
async def on_ready():
    print('Estoy vivo como {0.user}'.format(client))
    links.start()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await pipe.findPrice(message)

    if message.content.startswith(prefix):
        if 'crypto' in message.content:
            await pipe.crypto(message)


@tasks.loop(seconds=60)
async def links():
    if meets.mandar() is not None:
        dicc = meets.mandar()
        link = dicc.get("link")
        nom = dicc.get("nombre")
        content = f"Clase de {nom}, link: {link}"
        message_channel = client.get_channel(838783941355896884)
        message_channel2 = client.get_channel(842742270155685898)
        message_channel3 = client.get_channel(838812861437313055)
        await message_channel.send(content)
        await message_channel2.send(content)
        await message_channel3.send(content)


@tasks.loop(hours=8)
async def prices(message):
    await pipe.crypto(message)

client.run(TOKEN)
