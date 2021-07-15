from datetime import datetime
import sqlite3

conn = sqlite3.connect('data.db')
curs = conn.cursor()


def getClasesHoy():
    hoy = datetime.now().weekday()
    with conn:
        curs.execute("SELECT * FROM clases WHERE dia=:dia", {'dia': hoy})
        return curs.fetchall()


def getClasesAhora():
    ahora = datetime.now().strftime("%H:%M")
    hoy = datetime.now().weekday()
    with conn:
        curs.execute("SELECT * FROM clases WHERE dia=:dia AND hora=:hora", {'dia': hoy, 'hora': ahora})
        return curs.fetchall()


def getCanalesCurso(curso):
    with conn:
        curs.execute("SELECT canal FROM canales WHERE curso=:curso", {'curso': curso})
        return curs.fetchall()


def getClaseSiguiente(curso):
    ahora = datetime.now().strftime("%H:%M")
    hoy = datetime.now().weekday()
    with conn:
        curs.execute("SELECT * FROM clases WHERE dia=:dia AND hora>=:hora AND curso=:curso", {'dia': hoy, 'hora': ahora, 'curso': curso})
        return curs.fetchone()


def getCursoByID(canal):
    canal = str(canal)
    with conn:
        curs.execute("SELECT curso FROM canales WHERE canal=:canal", {'canal': canal})
        return curs.fetchone()


def getTareasCurso(curso):
    hoy = datetime.now().strftime("%m/%d/%y")
    with conn:
        curs.execute("SELECT * FROM tareas WHERE fecha>=:fecha AND curso=:curso", {'fecha': hoy, 'curso': curso})
        return curs.fetchall()


getTareasCurso('info')
