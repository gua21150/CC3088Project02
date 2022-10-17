from Control.control_usuario import *
from Control.validation_request import create_pandas_table

def acciones_usuario_suscrito_oro():
    print("\t¿Qué deseas hacer hoy?")
    print("\t\t[1] Buscar sesión y agendarme")
    print("\t\t[2] Unirme a sesion de ejercicio")
    print("\t\t[3] Consultar sesiones semanales")
    print("\t\t[4] Consultar sesiones pasadas")
    print("\t\t[5] Cambiar plan de ejercicio y cancelar")
    print("\t\t[6] Consultar mi progreso en sesiones")
    print("\t\t[7] Registro y consulta de mi peso semanal")
    print("\t\t[8] Cerrar sesion")


def acciones_usuario_suscrito_diamante():
    print("\t¿Qué deseas hacer hoy?")
    print("\t\t[1] Buscar sesión y agendarme")
    print("\t\t[2] Unirme a sesion de ejercicio")
    print("\t\t[3] Unirme a sesion de nutricionista")
    print("\t\t[4] Consultar sesiones semanales")
    print("\t\t[5] Consultar sesiones pasadas")
    print("\t\t[6] Cambiar plan de ejercicio y cancelar")
    print("\t\t[7] Consultar mi progreso en sesiones")
    print("\t\t[8] Registro y consulta de mi peso semanal")
    print("\t\t[9] Cerrar sesion")


def acciones_usuario_no_suscrito():
    print("\t¿Qué deseas hacer hoy?")
    print("\t\t[1] Registrar metodo de pago")
    print("\t\t[2] Elegir plan de ejercicio y cancelar")
    print("\t\t[3] Salir")


def accion_usuario_no_suscrito(conn, id):
    se_suscribio = False
    acciones_usuario_no_suscrito()  # llamada del menu
    option = int(input("Ingrese su opción: "))

    while option != 0:
        if option == 1:  # registrar metodo de pago
            registro_metodo_pago(conn, id)
        elif option == 2:  # elegir plan de ejercicio y cancelar
            print("\tEstos son los planes que te ofrecemos ")
            query = "SELECT tipo, precio FROM suscripcion;"
            planes_info = create_pandas_table(query, conn)
            print("En diamante tendrás un IHealthWatch+ de regalo y una sesión mensual con nutricionista")
            print("En oro tendrás un IHealthWatch+ de alquiler")
            print("\t¿Te gustaría obtener un plan de ejercicio?")
            try:
                respuesta = int(input("\t\t[1]Sí\n\t\t[2]No"))
                if respuesta == 1:
                    plan = int(input("\t\t¿Cuál te gustaría obtener?\n\t\t[1]Diamante\n\t\t[2]Oro"))

            except ValueError:
                print("Su respuesta no es valida, se le mostrara el menu")



            acciones_usuario_no_suscrito()
            option = int(input("Ingrese su opción: "))

            print("Feliz día")



