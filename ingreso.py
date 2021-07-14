import dbManagement

print("Nombre del curso: ")
curso = input()

print("Cantidad de materias (si hay una 2 dias distintos cuenta como 2): ")
cant = int(input())

print("Cantidad de canales de discord donde mandar los links: ")
cantLinks = int(input())


for i in range(cantLinks):
    print(f"Ingrese el ID del canal {i}: ")
    dbManagement.ingresarCanal(curso, str(input()))

dicc = {
    'nombre': '',
    'dia': 0,
    'link': '',
    'hora': '',
    'curso': ''
}

lista = []


def ingresar(i):
    dic = {}
    print(f'Nombre de la materia {i+1}: ')
    dic['nombre'] = input()
    print(f'Dia de {dicc["nombre"]} (lunes 0, martes 1...):')
    dic['dia'] = int(input())
    print(f'Link de {dicc["nombre"]}:')
    dic['link'] = input()
    print('Hora (2min antes de la clase, formato:07:58):')
    dic['hora'] = input()
    dic['curso'] = curso
    return dic


for i in range(cant):
    lista.append(ingresar(i))

dbManagement.insertarCurso(lista)
