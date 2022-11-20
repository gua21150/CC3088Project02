def acciones_usuario_suscrito_oro():
    print("\t¿Qué deseas hacer hoy?")
    print("\t\t[1] Buscar sesión y agendarme")
    print("\t\t[2] Unirme a sesión de ejercicio")
    print("\t\t[3] Consultar sesiones semanales y pasadas")
    print("\t\t[4] Cambiar plan de suscripción y cancelar")
    print("\t\t[5] Consultar mi progreso en sesiones")
    print("\t\t[6] Registro y consulta de mi peso semanal")
    print("\t\t[7] Cerrar sesión")

    try:
        select = int(input("¿Cuál es tu selección?"))
        if 1 <= select <= 7:
            return select
        else:
            print("Opción no válida, se cerrará sesión")
            return False
    except ValueError:
        print("Opción no válida, se cerrará sesión")
        return False

def acciones_usuario_suscrito_diamante():
    print("\t¿Qué deseas hacer hoy?")
    print("\t\t[1] Buscar sesión y agendarme")
    print("\t\t[2] Unirme a sesión de ejercicio")
    print("\t\t[3] Unirme a sesión de nutricionista")
    print("\t\t[4] Consultar sesiones semanales y pasadas")
    print("\t\t[5] Cambiar plan de suscripción y cancelar")
    print("\t\t[6] Consultar mi progreso en sesiones")
    print("\t\t[7] Registro y consulta de mi peso semanal")
    print("\t\t[8] Cerrar sesión")

    try:
        select = int(input("¿Cuál es tu selección?"))
        if 1 <= select <= 8:
            return select
        else:
            print("Opción no válida, se cerrará sesión")
            return False
    except ValueError:
        print("Opción no válida, se cerrará sesión")
        return False


def acciones_busqueda_sesiones():
    print("\t¿Cuál sesión te llama la atención?")
    print("\t\t[1] Las sesiones de esta semana")
    print("\t\t[2] Por el día de la sesión")
    print("\t\t[3] Por el horario de la sesión")
    print("\t\t[4] Por duración de la sesión")
    print("\t\t[5] Por el instructor")
    print("\t\t[6] Por la categoría")
    print("\t\t[7] Regresar")

    try:
        select = int(input("¿Cuál es tu selección?"))
        if 1 <= select <= 7:
            return select
        else:
            print("Opción no válida, se cerrará sesión")
            return False
    except ValueError:
        print("Opción no válida, se cerrará sesión")
        return False