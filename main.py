import discord
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

    if message.content.startswith(prefix):
        if message.content.lower() == '=proxclase':
            curso = meets.getCursoByID(message.channel.id)[0]
            if curso is not None:
                clase = meets.getClaseSiguiente(curso)
                if clase is not None:
                    content = f'La proxima clase es {clase[2]}, a las {clase[1]}, link: {clase[3]}'
                    await message.channel.send(content, delete_after=7200)
                else:
                    content = 'No hay mas clases por hoy ;)'
                    await message.channel.send(content, delete_after=7200)


@tasks.loop(seconds=60)
async def links():
    clasesAhora = meets.getClasesAhora()
    if clasesAhora is not None:
        for clase in clasesAhora:
            content = f'Clase de {clase[2]}, link: {clase[3]}'
            canales = meets.getCanalesCurso(clase[4])
            for canal in canales:
                message_channel = client.get_channel(int(canal[0]))
                await message_channel.send(content, delete_after=7200)


client.run(TOKEN)
