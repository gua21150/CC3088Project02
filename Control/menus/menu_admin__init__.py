def menu_principal():
    print("\t¿Qué deseas hacer hoy?")
    print("\t\t[1] Agregar o dar de baja a instructores")
    print("\t\t[2] Agregar, modificar, dar de baja a sesiones")
    print("\t\t[3] Dar de baja a usuario")
    print("\t\t[4] Reportería de iHealth+")
    print("\t\t[5] Cerrar sesión")

    try:
        select = int(input("¿Cuál es tu selección?"))
        if 1 <= select <= 5:
            return select
        else:
            print("Opción no válida, se cerrará sesión")
            return False
    except ValueError:
        print("Opción no válida, se cerrará sesión")
        return False

def menu_entrenadores():
    print("\t\t[1] Agregar instructor")
    print("\t\t[2] Dar de baja instructor (Esto solo lo desactivará)\n\t\tEsta acción es irreversible")
    print("\t\t[3] Retornar ")

    try:
        select = int(input("¿Cuál es tu selección?"))
        if 1 <= select <= 3:
            return select
        else:
            print("Opción no válida, se cerrará sesión")
            return False
    except ValueError:
        print("Opción no válida, se cerrará sesión")
        return False


def menu_sesiones():
    print("\t\t[1] Agregar sesión")
    print("\t\t[2] Modificar sesión\n\t\t\tSolo se podrá modificar la categoría de la sesión siempre y cuando la sesión no ha ocurrido")
    print("\t\t[3] Dar de baja sesión\n\t\t\tEsta sesión será eliminada")
    print("\t\t[4] Retornar ")

    try:
        select = int(input("¿Cuál es tu selección?"))
        if 1 <= select <= 4:
            return select
        else:
            print("Opción no válida, se cerrará sesión")
            return False
    except ValueError:
        print("Opción no válida, se cerrará sesión")
        return False


def menu_usuario_admin():
    print("\t\t[1] Dar de baja a usuario \n\t\t\tEsto desactivará el acceso a la aplicación al usuario")
    print("\t\t[2] Activar a usuario \n\t\t\tEsta acción le permitirá el acceso a la aplicación")
    print("\t\t[3] Retornar ")

    try:
        select = int(input("¿Cuál es tu selección?"))
        if 1 <= select <= 3:
            return select
        else:
            print("Opción no válida, se cerrará sesión")
            return False
    except ValueError:
        print("Opción no válida, se cerrará sesión")
        return False


def menu_reporteria():
    print("\t\t[1] Top 10 sesiones ")
    print("\t\t[2] Buscar popularidad de categorías por fecha ")
    print("\t\t[3] Top 5 entrenadores")
    print("\t\t[4] Cantidad cuentas diamante")
    print("\t\t[5] Conocer la hora pico en iHealth+ de una fecha ")
    print("\t\t[6] Regresar ")

    try:
        select = int(input("¿Cuál es tu selección?"))
        if 1 <= select <= 6:
            return select
        else:
            print("Opción no válida, se cerrará sesión")
            return False
    except ValueError:
        print("Opción no válida, se cerrará sesión")
        return False
