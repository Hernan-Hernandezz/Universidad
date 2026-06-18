from icecream import ic

# definicion de los datos a usar en tres grupos estudiantes,matriculas,clases, asignatura
estudiantes = [
    {"id_user": 0, "user": "hernan", "correo": "h@gmail.com", "password": "123"},
    {"id_user": 1, "user": "luis", "correo": "l@gmail.com", "password": "123"},
    {"id_user": 2, "user": "karol", "correo": "k@gmail.com", "password": "123"},
    {"id_user": 3, "user": "jose|", "correo": "j@gmail.com", "password": "123"},
    {"id_user": 4, "user": "anderson", "correo": "a@gmail.com", "password": "123"},
    {"id_user": 5, "user": "jhonatan", "correo": "jh@gmail.com", "password": "123"},
]

matriculas = [
    {
        "id_matricula": 1,
        "id_user": 1,
        "id_room": 1,
        "note": 3.5,
        "state": "en proceso",
    },
    {
        "id_matricula": 3,
        "id_user": 2,
        "id_room": 1,
        "note": 3.5,
        "state": "en proceso",
    },
    {
        "id_matricula": 5,
        "id_user": 3,
        "id_room": 1,
        "note": 3.5,
        "state": "en proceso",
    },
    {
        "id_matricula": 7,
        "id_user": 3,
        "id_room": 2,
        "note": 3.5,
        "state": "en proceso",
    },
    {
        "id_matricula": 4,
        "id_user": 4,
        "id_room": 2,
        "note": 3.5,
        "state": "en proceso",
    },
    {
        "id_matricula": 2,
        "id_user": 5,
        "id_room": 1,
        "note": 3.5,
        "state": "en proceso",
    },
    {
        "id_matricula": 3,
        "id_user": 5,
        "id_room": 2,
        "note": 3.5,
        "state": "en proceso",
    },
    {
        "id_matricula": 8,
        "id_user": 5,
        "id_room": 1,
        "note": 3.5,
        "state": "en proceso",
    },
]

clases = [
    {"id_room": 1, "id_subject": 1},
    {"id_room": 2, "id_subject": 3},
]


asignaturas = [
    {
        "id_subject": 1,
        "name": "programacion",
    },
    {
        "id_subject": 2,
        "name": "excel",
    },
    {
        "id_subject": 3,
        "name": "bases de datos",
    },
    {
        "id_subject": 4,
        "name": "induccion educativa",
    },
]


# busca la asignatura por su id
def buscar_asigantura(id_subject):
    for i in asignaturas:
        if i["id_subject"] == id_subject:
            return i["name"]


# busca estudiantes por su id
def buscar_estudiante(id_user):
    estudiante = ""
    for i in estudiantes:
        if i["id_user"] == id_user:
            estudiante = i["user"]
    if estudiante != "":
        return estudiante
    else:
        return "estudiante no encontrado"


# buscar estudiantes en una clase
def buscar_estudiantes_clases():
    print("clases")
    lista_clases = []

    # busca todas las clase y las va listando
    for i in clases:
        lista_clases.append(i["id_room"])
        print(f"{i["id_room"]}. {buscar_asigantura(i["id_subject"])}")

    clase = int(input("ingresa el numero para seleccionar una clase\n"))

    # busca si la clase si existe en la lista
    if clase in lista_clases:
        print("estudiantes de la clase")

        # busca que estudiantes estan en la clase
        for estudiante in matriculas:
            if estudiante["id_room"] == clase:
                nombre_estudiante = buscar_estudiante(estudiante["id_user"])
                print(nombre_estudiante)
    else:
        print("clase no encontrada")


# print(buscar_estudiante(2))
# print(buscar_estudiante(7))

buscar_estudiantes_clases()

# busqueda = buscar_asigantura(2)
# print(busqueda)
