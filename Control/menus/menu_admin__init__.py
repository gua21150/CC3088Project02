def menu_principal():
    print("\t¿Qué deseas hacer hoy?")
    print("\t\t[1] Agregar, modificar o dar de baja a instructores")
    print("\t\t[2] Agregar, modificar, dar de baja a sesiones")
    print("\t\t[3] Modificar a usuario")
    print("\t\t[4] Reportería de iHealth+")
    print("\t\t[5] Realizar Simulación")
    print("\t\t[6] Perfil de administradores")
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

def menu_entrenadores():
    print("\t\t[1] Agregar instructor")
    print("\t\t[2] Dar de baja instructor (Esto solo lo desactivará)")
    print("\t\t[3] Activar instructor")
    print("\t\t[4] Modificar nombre al instructor")
    print("\t\t[5] Modificar apellido al instructor")
    print("\t\t[6] Modificar nombre y apellido al instructor")
    print("\t\t[7] Modificar password al instructor")
    print("\t\t[8] Retornar ")

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
    print("\t\t[2] Modificar nombre al usuario")
    print("\t\t[3] Modificar apellido al usuario")
    print("\t\t[4] Modificar nombre y apellido al usuario")
    print("\t\t[5] Modificar password al usuario")
    print("\t\t[6] Retornar ")

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


def menu_reporteria():
    print("\t\t[1] Top 10 sesiones ")
    print("\t\t[2] Buscar popularidad de categorías por fecha ")
    print("\t\t[3] Top 5 entrenadores")
    print("\t\t[4] Cantidad cuentas diamante")
    print("\t\t[5] Conocer la hora pico en iHealth+ de una fecha ")
    print("\t\t[6] Bitacora actividad de usuarios ")
    print("\t\t[7] Bitacora actividad de administradores ")
    print("\t\t[8] Top 5 sesiones con más usuarios en horas registradas")
    print("\t\t[9] Top 10 entrenadores más solicitados ")
    print("\t\t[10] Top 5 administradores que modifican cuentas de usuario")
    print("\t\t[11] Top 20 de usuarios sin realizar ejercicio")
    print("\t\t[12] Retornar ")

    try:
        select = int(input("¿Cuál es tu selección?"))
        if 1 <= select <= 12:
            return select
        else:
            print("Opción no válida, se cerrará sesión")
            return False
    except ValueError:
        print("Opción no válida, se cerrará sesión")
        return False
    
def menu_simulacion():
    print("\t\t[1] Iniciar simulación ")
    print("\t\t[2] Iniciar simulación a nivel de base de datos")
    try:
        select = int(input("¿Cuál es tu selección?"))
        if 1 <= select <= 2:
            return select
        else:
            print("Opción no válida, se cerrará sesión")
            return False
    except ValueError:
        print("Opción no válida, se cerrará sesión")
        return False
    
def menu_perfil_admin():
    print("\t\t[1] Crear nuevo administrador")
    print("\t\t[2] Activar permisos de administrador")
    print("\t\t[3] Desactivar permisos de administrador")
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
