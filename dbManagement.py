import sqlite3

conn = sqlite3.connect('data.db')

curs = conn.cursor()


def insertarClase(clase):
    with conn:
        curs.execute("INSERT INTO clases VALUES (:dia, :hora, :nombre, :link, :curso)", {'dia': clase['dia'], 'hora': clase['hora'], 'nombre': clase['nombre'], 'link': clase['link'], 'curso': clase['curso']})


def insertarCurso(curso):
    for elemento in curso:
        insertarClase(elemento)


def insertarCanal(nomCurso, canal):
    with conn:
        curs.execute("INSERT INTO canales VALUES (:curso, :canal)", {'curso': nomCurso, 'canal': canal})


def insertarTarea(tarea, fecha, curso):
    # LA FECHA DEBE SER STRING Y TENER FORMATO 07/14/21
    with conn:
        curs.execute("INSERT INTO tareas VALUES (:tarea, :fecha, :curso)", {'tarea': tarea, 'fecha': fecha, 'curso': curso})


def borrarTarea(tarea):
    pass
