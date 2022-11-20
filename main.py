# importacion de librerías
from Control.validation_request import *
from Control.menus import *
from Control.menus.menu_usuario__init___ import *
from Control.control_admin.admin_eleccion__init__ import *
from Control.control_admin import iniciar_sesion_admin


conn = connect_db()  # se conecta a la base de datos
print("---------------")
print("Bienvenido a iHealth+")
try:
    menu_login()
    option = int(input("Ingrese su opción: "))

    while option != 0:
        if option == 1:  # iniciar sesion
            menu_iniciar_sesion()  # llamada al menu
            option2 = int(input("Ingrese su selección: "))

            if option2 == 1:  # iniciar sesion como usuario
                nick, passw = credencial_login("¿Cuál es tu nombre de usuario?")
                validacion = iniciar_sesion_usuario(conn, nick, passw)

                if validacion is not False:

                    id, suscrip, dias = validacion
                    id_usuario = int(id)
                    print("Faltan %s para tu próxima renovación de servicio" % dias)
                    # presentar menu de acciones
                    if suscrip == 2:  # cuenta oro
                        resp = 1
                        while resp != 7:
                            resp = acciones_usuario_suscrito_oro()

                            if resp == 1:  # sesiones y agendar
                                conn = connect_db()
                                cursor = conn.cursor()
                                op_sesion = acciones_busqueda_sesiones()
                                id_sesion = 0
                                if op_sesion == 1: # sesiones de la semana
                                    print("Presentar las sesiones de esta semana")
                                    id_sesion = mostrar_sesiones_semanales(conn)
                                elif op_sesion == 2: # buscar por fecha
                                    id_sesion = mostrar_sesiones_fecha(conn)
                                elif op_sesion == 3: # buscar por horario
                                    id_sesion = mostrar_sesiones_horario(conn)
                                elif op_sesion == 4: # duracion de la sesion
                                    id_sesion = mostrar_sesiones_duracion(conn)
                                elif op_sesion == 5: # por el instructor
                                    id_sesion = mostrar_sesiones_entrenador(conn, id_usuario)
                                elif op_sesion == 6: # por la categoria
                                    id_sesion = mostrar_sesiones_categoria(conn)
                                else:
                                    id_sesion = False

                                if id_sesion is not False:
                                    try:
                                        conn = connect_db()
                                        agendar_sesion(conn, id_usuario, id_sesion)
                                    except:
                                        print("parece que has ingresado incorrectamente el id de la sesion")

                            elif resp == 2:  # unirse a la sesion
                                print("Estas son las sesiones de esta semana") # sesiones generales
                                conn = connect_db()
                                mis_sesiones_semanales(conn, id_usuario)
                                print("El dia de hoy puedes unirte a estas sesiones") # sesion que tiene agendada
                                mis_sesiones_diarias(conn, id_usuario)
                            elif resp == 3:  # sesiones semanales
                                conn = connect_db()
                                print("Estas han sido las sesiones pasadas en iHealth+")
                                mostrar_sesiones(conn)
                                print("Estas son las sesiones de esta semana en iHealth+")
                                mostrar_sesiones_semanales(conn)
                            elif resp == 4:  # cambiar de plan
                                conn = connect_db()
                                tipo = presentar_tipos_planes(conn)  # se presentan tipos de planes
                                conn = connect_db()
                                registrar_suscripcion(conn, id_usuario, tipo)
                                conn = connect_db()
                                realizar_pago_suscripcion(conn, id_usuario)
                                print("Transaccion realizada con exito, por favor vuelva a iniciar sesion")
                                resp = 7
                            elif resp == 5:  # tiempo del usuario en sesiones
                                print("Esta es tu estadistica")
                                estadisticas_sesiones(conn, id_usuario)
                            elif resp == 6:
                                registrar_peso(conn, id_usuario)
                            else:
                                resp = 7  # para el while
                                option = 0  # retorna 0 porque desea cerrar sesion
                    else:
                        # suscripcion de diamante
                        resp = 1
                        while resp != 8:
                            resp = acciones_usuario_suscrito_diamante()

                            if resp == 1:  # sesiones y agendar
                                conn = connect_db()
                                cursor = conn.cursor()
                                op_sesion = acciones_busqueda_sesiones()
                                id_sesion = 0
                                if op_sesion == 1:  # sesiones de la semana
                                    print("Presentar las sesiones de esta semana")
                                    id_sesion = mostrar_sesiones_semanales(conn)
                                elif op_sesion == 2:  # buscar por fecha
                                    id_sesion = mostrar_sesiones_fecha(conn)
                                elif op_sesion == 3:  # buscar por horario
                                    id_sesion = mostrar_sesiones_horario(conn)
                                elif op_sesion == 4:  # duracion de la sesion
                                    id_sesion = mostrar_sesiones_duracion(conn)
                                elif op_sesion == 5:  # por el instructor
                                    id_sesion = mostrar_sesiones_entrenador(conn, id_usuario)
                                elif op_sesion == 6:  # por la categoria
                                    id_sesion = mostrar_sesiones_categoria(conn)
                                else:
                                    id_sesion = False

                                if id_sesion is not False:
                                    try:
                                        conn = connect_db()
                                        agendar_sesion(conn, id_usuario, id_sesion)
                                        print("Ha sido agregado a esta sesion")
                                    except:
                                        print("parece que has ingresado incorrectamente el id de la sesion")

                            elif resp == 2:  # unirse a la sesion
                                print("Estas son las sesiones de esta semana") # sesiones generales
                                conn = connect_db()
                                mis_sesiones_semanales(conn, id_usuario)
                                print("El dia de hoy puedes unirte a estas sesiones") # sesion que tiene agendada
                                mis_sesiones_diarias(conn, id_usuario)
                            elif resp == 3:
                                print("Se ha unido a la sesion con la nutricionista")
                            elif resp == 4:  # sesiones semanales
                                conn = connect_db()
                                print("Estas han sido las sesiones pasadas en iHealth+")
                                mostrar_sesiones(conn)
                                print("Estas son las sesiones de esta semana en iHealth+")
                                mostrar_sesiones_semanales(conn)
                            elif resp == 5:  # cambiar de plan
                                conn = connect_db()
                                tipo = presentar_tipos_planes(conn)  # se presentan tipos de planes
                                conn = connect_db()
                                registrar_suscripcion(conn, id_usuario, tipo)
                                conn = connect_db()
                                realizar_pago_suscripcion(conn, id_usuario)
                                print("Transaccion realizada con exito, por favor vuelva a iniciar sesion")
                                resp = 8
                            elif resp == 6:  # tiempo del usuario en sesiones
                                print("Esta es tu estadistica")
                                conn = connect_db()
                                estadisticas_sesiones(conn, id_usuario)
                            elif resp == 7:
                                registrar_peso(conn, id_usuario)
                            else:
                                resp = 8  # para el while
                                option = 0  # retorna 0 porque desea cerrar sesion
                else:
                    print("Este usuario no esta registrado. Valide su nickname y contraseña")
            elif option2 == 2:  # iniciar sesion como trabajador
                correo, passw = credencial_login("¿Cuál es tu correo?")
                conn = connect_db()
                id_admin = iniciar_sesion_admin(conn, correo, passw)
                if id_admin is not False:
                    resp = 1  # menu principal de los admin
                    cod_admin = id_admin[0]  # para el registro en bitacora
                    rol_admin = id_admin[1]  # el rol del admin le da permisos en ciertas funciones
                    while resp != 6:
                        resp = menu.menu_principal()
                        if resp == 1:  # entrenadores
                            resp1 = menu.menu_entrenadores()
                            if resp1 == 1:  # agregar entrenador
                                conn = connect_db()
                                registrar_entrenador(conn, cod_admin, rol_admin)
                            elif resp1 == 2:  # dar de baja a entrenador
                                conn = connect_db()
                                mostrar_entrenadores(conn)  # se muestran los entrenadores
                                id_entrenador = int(input("De los anteriores entrenadores, escriba el id del entrenador "))
                                conn = connect_db()
                                dar_baja_entrenador(conn, id_entrenador, cod_admin, rol_admin)
                            elif resp1 == 3:  # Activar instructor
                                conn = connect_db()
                                mostrar_entrenadores(conn)  # se muestran los entrenadores
                                id_entrenador = int(input("De los anteriores entrenadores, escriba el id del entrenador "))
                                conn = connect_db()
                                activar_entrenador(conn, id_entrenador, cod_admin, rol_admin)
                            elif resp1 == 4:  # modificar nombre
                                conn = connect_db()
                                mostrar_entrenadores(conn)  # se muestran los entrenadores
                                id_entrenador = int(input("De los anteriores entrenadores, escriba el id del entrenador para cambiarle nombre "))
                                modificar_nombre(conn, id_entrenador, cod_admin, rol_admin, 1)
                            elif resp1 == 5:  # modificar apellido
                                conn = connect_db()
                                mostrar_entrenadores(conn)  # se muestran los entrenadores
                                id_entrenador = int(input("De los anteriores entrenadores, escriba el id del entrenador para cambiarle apellido "))
                                modificar_nombre(conn, id_entrenador, cod_admin, rol_admin, 2)
                            elif resp1 == 6: # modificar nombre y apellido
                                conn = connect_db()
                                mostrar_entrenadores(conn)  # se muestran los entrenadores
                                id_entrenador = int(input("De los anteriores entrenadores, escriba el id del entrenador para cambiarle nombre y apellido "))
                                modificar_nombre(conn, id_entrenador, cod_admin, rol_admin, 3)
                            elif resp1 == 7: # modificar password
                                conn = connect_db()
                                mostrar_entrenadores(conn)  # se muestran los entrenadores
                                id_entrenador = int(input("De los anteriores entrenadores, escriba el id del entrenador para cambiarle password "))
                                modificar_password_entre(conn, id_entrenador, cod_admin, rol_admin)
                            elif resp1 is False:  # retornar
                                resp = 5  # termina el while
                                option = 0  # se cierra sesion automaticamente

                        elif resp == 2:  # sesiones
                            resp1 = 0
                            resp1 = menu.menu_sesiones()
                            if resp1 == 1:  # agregar sesion
                                conn = connect_db()
                                registrar_sesion(conn, cod_admin, rol_admin)
                            elif resp1 == 2:  # modificar sesion
                                conn = connect_db()
                                mostrar_sesiones_modificar(conn)  # se muestran las sesiones que se pueden modificar
                                id_sesion = int(input("De las anteriores sesiones, escriba el id de la sesion que desea modificar "))
                                conn = connect_db()
                                mostrar_categorias_ejercicio(conn)
                                id_categoria = int(input("De las anteriores CATEGORIAS, escriba el id de la categoria que desea modificar "))
                                conn = connect_db()
                                modificar_sesion(conn, id_sesion, id_categoria, cod_admin, rol_admin)
                            elif resp1 == 3:  # dar baja sesion
                                conn = connect_db()
                                mostrar_sesiones(conn)  # se muestran las sesiones
                                id_sesion = int(input("De las anteriores sesiones, escriba el id de la sesion que desea eliminar "))
                                conn = connect_db()
                                dar_baja_sesion(conn, id_sesion, cod_admin, rol_admin)
                            elif resp1 is False:  # retornar
                                resp = 5  # termina el while
                                option = 0  # se cierra sesion automaticamente
                        elif resp == 3:  # usuario
                            resp1 = 0
                            resp1 = menu.menu_usuario_admin()
                            if resp1 == 1:
                                print("Se le mostraran los usuarios cuyas cuentas estan activas")
                                conn = connect_db()
                                mostrar_usuarios(conn)
                                res = int(input("Escriba el id del usuario que desea desactivar. Esta accion es irreversible, ademas se eliminara el metodo de pago del usuario "))
                                conn = connect_db()
                                desactivar_usuario(conn, res, cod_admin, rol_admin)
                            elif resp1 == 2:  # modificar nombre
                                conn = connect_db()
                                mostrar_usuarios(conn)  # se muestran los usuarios
                                id_usuario = int(input(
                                    "De los anteriores usuarios, escriba el id del usuario para cambiarle nombre "))
                                modificar_nombre_usuario(conn, id_usuario, cod_admin, rol_admin, 1)
                            elif resp1 == 3:  # modificar apellido
                                conn = connect_db()
                                mostrar_usuarios(conn)  # se muestran los usuarios
                                id_usuario = int(input(
                                    "De los anteriores usuarios, escriba el id del usuario para cambiarle apellido "))
                                modificar_nombre_usuario(conn, id_usuario, cod_admin, rol_admin, 2)
                            elif resp1 == 4:  # modificar nombre y apellido
                                conn = connect_db()
                                mostrar_usuarios(conn)  # se muestran los usuarios
                                id_usuario = int(input(
                                    "De los anteriores usuarios, escriba el id del usuario para cambiarle nombre y apellido "))
                                modificar_nombre_usuario(conn, id_usuario, cod_admin, rol_admin, 3)
                            elif resp1 == 5:  # modificar password
                                conn = connect_db()
                                mostrar_usuarios(conn)  # se muestran los usuarios
                                id_usuario = int(input(
                                    "De los anteriores usuarios, escriba el id del usuario para cambiarle nombre "))
                                modificar_password_usuario(conn, id_usuario, cod_admin, rol_admin)
                            elif resp1 is False:  # retornar
                                resp = 5  # termina el while
                                option = 0  # se cierra sesion automaticamente
                        elif resp == 4:  # reporteria
                            resp1 = menu.menu_reporteria()
                            if resp1 == 1:  # top sesiones
                                conn = connect_db()
                                sesiones_populares(conn)
                            elif resp1 == 2:  # cantidad sesiones
                                conn = connect_db()
                                sesiones_fecha(conn)
                            elif resp1 == 3:  # entrenadores
                                conn = connect_db()
                                top_entrenadores(conn)
                            elif resp1 == 4:  # cuentas diamantes
                                conn = connect_db()
                                cuentas_diamante(conn)
                            elif resp1 == 5:  # hora pico
                                conn = connect_db()
                                hora_pico(conn)
                            elif resp1 == 6:  # bitacora usuarios
                                conn = connect_db()
                                bitacora_usuario(conn)
                            elif resp1 == 7:  # bitacora admin
                                conn = connect_db()
                                bitacora_admin(conn)
                            elif resp1 is False:  # retornar
                                resp = 5  # termina el while
                                option = 0
                        elif resp == 5:  # siomulacion
                            menu.menu_simulacion()
                        else:
                            resp = 6  # para el while
                            option = 0  # retorna 0 porque desea cerrar sesion

        elif option == 2:  # registrar usuario
            conn = connect_db()
            id = registrar_usuario(conn)  # se obtiene su usuario
            conn = connect_db()
            registro_metodo_pago(conn, id)   # se registra su metodo de pago
            conn = connect_db()
            tipo = presentar_tipos_planes(conn)  # se presentan tipos de planes
            conn = connect_db()
            registrar_suscripcion(conn, id, tipo)
            conn = connect_db()
            realizar_pago_suscripcion(conn, id)
            print("Por favor inicie sesion")

        menu_login()
        option = int(input("Ingrese su opción: "))

    print("Feliz día, ha cerrado sesion ")
except Exception as e:
    print("Su entrada no es válida, feliz día. \nERROR: %s" % e)
finally:
    conn.rollback()
    conn.close()

