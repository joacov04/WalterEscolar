import discord
import os
import dbQueries
import dbManagement
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
        if message.content.lower() == '=help':
            emb = discord.Embed(title='Help Page', description='WalterEscolar va a mandar los links de cada clase 2 minutos antes.\nComandos:', color=0x961111)
            emb.set_footer(text='by samurai#1995')
            emb.add_field(name="=proxclase", value="Responde con la hora y el link de la clase en el mismo dia. Este comando solo puede ser usado en canales donde manda links.", inline=False)
            emb.add_field(name="=clases", value="Responde con el dia, hora y link de cada clase. Solo se puede usar en canales donde manda links.", inline=False)
            emb.add_field(name="=nuevatarea una tarea, fecha", value="Guarda una tarea que se elimina luego de la fecha solicitada. Solo se puede usar en canales done manda links. Hay que separar la tarea y fecha con la coma y la decha debe tener el sig formato: 07/15/21 (15 de julio del 2021)", inline=False)
            emb.add_field(name="=tareas", value="Responde con todas las tareas del curso. Solo se puede usar en canales donde manda links.", inline=False)
            await message.channel.send(embed=emb)

        if message.content.lower() == '=clases':
            curso = dbQueries.getCursoByID(message.channel.id)[0]
            if curso is not None:
                emb = discord.Embed(title=f'Clases de {curso}', color=0x961111)
                emb.set_footer(text='by samurai#1995')
                clases = dbQueries.getClasesCurso(curso)
                for clase in clases:
                    if clase[0] == 0:
                        weekday = 'lunes'
                    elif clase[0] == 1:
                        weekday = 'martes'
                    elif clase[0] == 2:
                        weekday = 'miercoles'
                    elif clase[0] == 3:
                        weekday = 'jueves'
                    elif clase[0] == 4:
                        weekday = 'viernes'
                    elif clase[0] == 5:
                        weekday = 'sabado'
                    else:
                        weekday = 'domingo'
                    emb.add_field(name=f'{clase[2]}', value=f'{weekday.capitalize()} a las {clase[1]}, link: {clase[3]}')
                await message.channel.send(embed=emb)

        if message.content.lower() == '=proxclase':
            curso = dbQueries.getCursoByID(message.channel.id)[0]
            emb = discord.Embed(color=0x961111)
            emb.set_footer(text='by samurai#1995')
            if curso is not None:
                clase = dbQueries.getClaseSiguiente(curso)
                if clase is not None:
                    emb.add_field(name=f'{clase[2]}', value=f'A las {clase[1]}, link: {clase[3]}')
                    await message.channel.send(embed=emb, delete_after=7200)
                else:
                    content = 'No hay mas clases por hoy ;)'
                    await message.channel.send(content, delete_after=7200) 

        if message.content.lower().startswith('=nuevatarea'):
            msg = message.content.split(',')
            fecha = msg[1].strip(' ')
            tarea = msg[0].lower().split('=nuevatarea')[1].lstrip(' ').capitalize()
            curso = dbQueries.getCursoByID(message.channel.id)[0]
            dbManagement.insertarTarea(tarea, fecha, curso)

        if message.content.lower() == '=tareas':
            curso = dbQueries.getCursoByID(message.channel.id)[0]
            tareas = dbQueries.getTareasCurso(curso)
            msg = ''
            for tarea in tareas:
                content = f'{tarea[0]}  Fecha: {tarea[1]}\n'
                msg += content
            await message.channel.send(msg, delete_after=7200)


@tasks.loop(seconds=60)
async def links():
    clasesAhora = dbQueries.getClasesAhora()
    if clasesAhora is not None:
        for clase in clasesAhora:
            emb = discord.Embed(color=0x961111)
            emb.set_footer(text='by samurai#1995')
            emb.add_field(name=f'Clase de {clase[2]}', value=f'Link: {clase[3]}')
            canales = dbQueries.getCanalesCurso(clase[4])
            for canal in canales:
                message_channel = client.get_channel(int(canal[0]))
                await message_channel.send(embed=emb, delete_after=7200)


client.run(TOKEN)
