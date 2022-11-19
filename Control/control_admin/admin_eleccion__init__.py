from Control.menus import menu_admin__init__ as menu
from Control.control_admin import *
from Control.control_entrenador_nutricionista import *
from Control.control_sesion import *
from Control.control_usuario import *

def menu_principal_response(conn):
    resp = 1
    while resp != 6:
        resp = menu.menu_principal()

        if resp == 1:  # entrenadores
            resp1 = menu.menu_entrenadores()
            if resp1 == 1:  # agregar entrenador
                registrar_entrenador(conn)
            elif resp1 == 2:  # dar de baja a entrenador
                mostrar_entrenadores(conn)  # se muestran los entrenadores
                id_entrenador = int(input("De los anteriores entrenadores, escriba el id del entrenador"))
                dar_baja_entrenador(conn, id_entrenador)
            elif resp1 is False:  # retornar
                resp = 5  # termina el while
                return 0    # se cierra sesion automaticamente

        elif resp == 2:  # sesiones
            resp1 = 0
            resp1 = menu.menu_sesiones()
            if resp1 == 1:  # agregar sesion
                registrar_sesion(conn)
            elif resp1 == 2:  # modificar sesion
                mostrar_sesiones_modificar(conn)  # se muestran las sesiones que se pueden modificar
                id_sesion = int(input("De las anteriores sesiones, escriba el id de la sesion que desea modificar"))
                mostrar_categorias_ejercicio(conn)
                id_categoria = int(input("De las anteriores CATEGORIAS, escriba el id de la categoria que desea modificar"))
                modificar_sesion(conn, id_sesion, id_categoria)
            elif resp1 == 3:  # dar baja sesion
                mostrar_sesiones(conn)  # se muestran las sesiones
                id_sesion = int(input("De las anteriores sesiones, escriba el id de la sesion que desea eliminar"))
                dar_baja_sesion(conn, id_sesion)
            elif resp1 is False:  # retornar
                resp = 5    # termina el while
                return 0    # se cierra sesion automaticamente
        elif resp == 3:  # usuario
            resp1 = 0
            resp1 = menu.menu_usuario_admin()
            if resp1 == 1:
                print("Se le mostraran los usuarios cuyas cuentas estan activas")
                mostrar_usuarios(conn)
                res = int(input("Escriba el id del usuario que desea desactivar. Esta accion es irreversible, ademas se eliminara el metodo de pago del usuario"))
                desactivar_usuario(conn, res)
            elif resp1 is False:  # retornar
                resp = 5  # termina el while
                return 0  # se cierra sesion automaticamente
        elif resp == 4:  # reporteria
            resp1 = menu.menu_reporteria()
            if resp1 == 1:  # top sesiones
                sesiones_populares(conn)
            elif resp1 == 2:  # cantidad sesiones
                sesiones_fecha(conn)
            elif resp1 == 3:  # entrenadores
                top_entrenadores(conn)
            elif resp1 == 4:  # cuentas diamantes
                cuentas_diamante(conn)
            elif resp1 == 5:  # hora pico
                hora_pico(conn)
            elif resp1 is False:  # retornar
                resp = 6  # termina el while
                return 0
        elif resp == 5:  # simulación
            resp1 = menu.menu_simulacion()
        else:
            resp = 6  # para el while
            return 0  # retorna 0 porque desea cerrar sesion

