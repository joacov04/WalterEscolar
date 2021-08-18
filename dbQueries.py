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
        fetch = curs.fetchall()
        if fetch == []:
            return None
        hora = fetch[1].split(':')[0] + ':' + str(int(fetch[1].split(':')[1])+2) if fetch[1].split(':')[1] != '58' else str(int(fetch[1].split(':')[0])+1) + ':' + '00'
        tupla = (fetch[0], hora, fetch[2], fetch[3], fetch[4])
        return tupla


def getClasesCurso(curso):
    with conn:
        curs.execute("SELECT * FROM clases WHERE curso=:curso", {'curso': curso})
        fetch = curs.fetchall()
        lista = []
        for clase in fetch:
            hora = clase[1].split(':')[0] + ':' + str(int(clase[1].split(':')[1])+2) if clase[1].split(':')[1] != '58' else str(int(clase[1].split(':')[0])+1) + ':' + '00'
            tupla = (clase[0], hora, clase[2], clase[3], clase[4])
            lista.append(tupla)
        return lista


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
