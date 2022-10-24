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
                    id_usuario, suscrip, dias = validacion
                    print("Faltan %s para tu próxima renovación de servicio" % dias)
                    # presentar menu de acciones
                    if suscrip == 'IDS_O':
                        resp = 1
                        while resp != 7:
                            resp = acciones_usuario_suscrito_oro()

                            if resp == 1:  # sesiones y agendar
                                conn = connect_db()
                                cursor = conn.cursor()
                                print("Presentar las sesiones de esta semana")
                                query = "select id_sesion, ejercicio, fecha, hora_inicio, hora_fin, nombres "\
                                        "From sesion_ejercicio ses inner join categoria_ejercicio cat on ses.categoria = cat.id_categoria "\
                                        "                         inner join trabajador t on ses.instructor=t.id "\
                                        "WHERE fecha between current_date and current_date+'1 week'::interval; "
                                print(create_pandas_table(query, conn))
                                eleccion = str(input("Ingrese el id de la sesion a la que desea conectarse "))

                                try:
                                    query = "INSERT INTO sincronizacion_ejercicio (id_usuario, id_sesion) VALUES('%s','%s')" % (id_usuario, eleccion)  # lo registra
                                    conn = connect_db()
                                    cursor = conn.cursor()
                                    cursor.execute(query)
                                    conn.commit()
                                    print("Ha sido agregado a esta sesion")
                                except:
                                    print("parece que has ingresado correctamente el id de la sesion")
                            elif resp == 2: # unirse a la sesion
                                print("Estas son las sesiones de esta semana")
                                query = "select sinc.id_sesion, nombres, apellidos, fecha, sinc.hora_inicio, sinc.hora_fin "\
                                        "from sincronizacion_ejercicio sinc inner join usuario us on sinc.id_usuario = us.id_usuario "\
                                        "inner join sesion_ejercicio ses on sinc.id_sesion = ses.id_sesion "\
                                        "where fecha > current_date + interval '-1 week' and sinc.id_usuario='%s'" %id_usuario
                                conn = connect_db()
                                cursor = conn.cursor()
                                print(create_pandas_table(query, conn))
                                print("El dia de hoy puedes unirte a estas sesiones")
                                query = "select sinc.id_sesion, nombres, apellidos, fecha, sinc.hora_inicio, sinc.hora_fin " \
                                        "from sincronizacion_ejercicio sinc inner join usuario us on sinc.id_usuario = us.id_usuario " \
                                        "inner join sesion_ejercicio ses on sinc.id_sesion = ses.id_sesion " \
                                        "where fecha = current_date and sinc.id_usuario='%s'" %id_usuario
                                conn = connect_db()
                                print(create_pandas_table(query, conn))
                                # unirse = str(input("Ingresa el id de la sesion de hoy para poder unirte"))
                            elif resp == 3:  # sesiones semanales
                                conn = connect_db()
                                cursor = conn.cursor()
                                print("Sesiones pasadas y presentes en iHealth+")
                                query = "select id_sesion, ejercicio, fecha, hora_inicio, hora_fin, nombres "\
                                        "From sesion_ejercicio ses inner join categoria_ejercicio cat on ses.categoria = cat.id_categoria "\
                                        "inner join trabajador t on ses.instructor=t.id"
                                print(create_pandas_table(query,conn))
                            elif resp == 4:  # cambiar de plan
                                conn = connect_db()
                                tipo = presentar_tipos_planes(conn)  # se presentan tipos de planes
                                conn = connect_db()
                                registrar_suscripcion(conn, id_usuario, tipo)
                                conn = connect_db()
                                realizar_pago_suscripcion(conn, id)
                                print("Transaccion realizada con exito, por favor vuelva a iniciar sesion")
                                resp = 7
                            elif resp == 5:  # tiempo del usuario en sesiones
                                print("Esta es tu estadistica")
                                query = "select nombres, apellidos, sinc.id_usuario, id_sesion,hora_inicio, hora_fin "\
                                        "from sincronizacion_ejercicio sinc inner join usuario u on sinc.id_usuario = u.id_usuario "\
                                        "where sinc.id_usuario='%s'" %id_usuario
                                conn = connect_db()
                                cursor = conn.cursor()
                                print(create_pandas_table(query, conn))
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
                                print("Presentar las sesiones de esta semana")
                                query = "select id_sesion, ejercicio, fecha, hora_inicio, hora_fin, nombres " \
                                        "From sesion_ejercicio ses inner join categoria_ejercicio cat on ses.categoria = cat.id_categoria " \
                                        "                         inner join trabajador t on ses.instructor=t.id " \
                                        "WHERE fecha between current_date and current_date+'1 week'::interval; "
                                print(create_pandas_table(query, conn))
                                eleccion = str(input("Ingrese el id de la sesion a la que desea conectarse "))

                                try:
                                    query = "INSERT INTO sincronizacion_ejercicio (id_usuario, id_sesion) VALUES('%s','%s')" % (id_usuario, eleccion)  # lo registra
                                    conn = connect_db()
                                    cursor = conn.cursor()
                                    cursor.execute(query)
                                    conn.commit()
                                    print("Ha sido agregado a esta sesion")
                                except:
                                    print("parece que has ingresado correctamente el id de la sesion")
                                print("Ha sido agregado a esta sesion")
                            elif resp == 2:  # unirse a la sesion
                                print("Estas son las sesiones de esta semana")
                                query = "select sinc.id_sesion, nombres, apellidos, fecha, sinc.hora_inicio, sinc.hora_fin " \
                                        "from sincronizacion_ejercicio sinc inner join usuario us on sinc.id_usuario = us.id_usuario " \
                                        "inner join sesion_ejercicio ses on sinc.id_sesion = ses.id_sesion " \
                                        "where fecha > current_date + interval '-1 week' and sinc.id_usuario='%s'" % id_usuario
                                conn = connect_db()
                                cursor = conn.cursor()
                                print(create_pandas_table(query, conn))
                                print("El dia de hoy puedes unirte a estas sesiones")
                                query = "select sinc.id_sesion, nombres, apellidos, fecha, sinc.hora_inicio, sinc.hora_fin " \
                                        "from sincronizacion_ejercicio sinc inner join usuario us on sinc.id_usuario = us.id_usuario " \
                                        "inner join sesion_ejercicio ses on sinc.id_sesion = ses.id_sesion " \
                                        "where fecha = current_date and sinc.id_usuario='%s'" % id_usuario
                                conn = connect_db()
                                cursor = conn.cursor()
                                print(create_pandas_table(query, conn))
                                # unirse = str(input("Ingresa el id de la sesion de hoy para poder unirte"))
                            elif resp == 4:  # sesiones semanales
                                conn = connect_db()
                                cursor = conn.cursor()
                                print("Sesiones pasadas y presentes en iHealth+")
                                query = "select id_sesion, ejercicio, fecha, hora_inicio, hora_fin, nombres " \
                                        "From sesion_ejercicio ses inner join categoria_ejercicio cat on ses.categoria = cat.id_categoria " \
                                        "inner join trabajador t on ses.instructor=t.id"
                                print(create_pandas_table(query, conn))
                            elif resp == 5:  # cambiar de plan
                                conn = connect_db()
                                tipo = presentar_tipos_planes(conn)  # se presentan tipos de planes
                                conn = connect_db()
                                registrar_suscripcion(conn, id_usuario, tipo)
                                conn = connect_db()
                                realizar_pago_suscripcion(conn, id)
                                print("Transaccion realizada con exito, por favor vuelva a iniciar sesion")
                                resp = 7
                            elif resp == 6:  # tiempo del usuario en sesiones
                                print("Esta es tu estadistica")
                                query = "select nombres, apellidos, sinc.id_usuario, id_sesion,hora_inicio, hora_fin " \
                                        "from sincronizacion_ejercicio sinc inner join usuario u on sinc.id_usuario = u.id_usuario " \
                                        "where sinc.id_usuario='%s'" % id_usuario
                                conn = connect_db()
                                cursor = conn.cursor()
                                print(create_pandas_table(query, conn))
                            elif resp == 7:
                                registrar_peso(conn, id_usuario)
                            elif resp == 3:
                                print("Se ha unido a la sesion con la nutricionista")
                            else:
                                resp = 8  # para el while
                                option = 0  # retorna 0 porque desea cerrar sesion
                else:
                    print("Este usuario no esta registrado. Valide su nickname y contraseña")
            elif option2 == 2: # iniciar sesion como trabajador
                correo, passw = credencial_login("¿Cuál es tu correo?")
                if iniciar_sesion_admin(conn, correo, passw):
                    resp = 1
                    while resp != 5:
                        resp = menu.menu_principal()

                        if resp == 1:  # entrenadores
                            resp1 = menu.menu_entrenadores()
                            if resp1 == 1:  # agregar entrenador
                                conn = connect_db()
                                registrar_entrenador(conn)
                            elif resp1 == 2:  # dar de baja a entrenador
                                conn = connect_db()
                                mostrar_entrenadores(conn)  # se muestran los entrenadores
                                id_entrenador = str(input("De los anteriores entrenadores, escriba el id del entrenador"))
                                conn = connect_db()
                                dar_baja_entrenador(conn, id_entrenador)
                            elif resp1 is False:  # retornar
                                resp = 5  # termina el while
                                option = 0  # se cierra sesion automaticamente

                        elif resp == 2:  # sesiones
                            resp1 = 0
                            resp1 = menu.menu_sesiones()
                            if resp1 == 1:  # agregar sesion
                                conn = connect_db()
                                registrar_sesion(conn)
                            elif resp1 == 2:  # modificar sesion
                                conn = connect_db()
                                mostrar_sesiones_modificar(conn)  # se muestran las sesiones que se pueden modificar
                                id_sesion = str(input("De las anteriores sesiones, escriba el id de la sesion que desea modificar "))
                                conn = connect_db()
                                mostrar_categorias_ejercicio(conn)
                                id_categoria = str(input("De las anteriores CATEGORIAS, escriba el id de la categoria que desea modificar" ))
                                conn = connect_db()
                                modificar_sesion(conn, id_sesion, id_categoria)
                            elif resp1 == 3:  # dar baja sesion
                                conn = connect_db()
                                mostrar_sesiones(conn)  # se muestran las sesiones
                                id_sesion = input(
                                    "De las anteriores sesiones, escriba el id de la sesion que desea eliminar")
                                conn = connect_db()
                                dar_baja_sesion(conn, id_sesion)
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
                                res = input("Escriba el id del usuario que desea desactivar. Esta accion es irreversible, ademas se eliminara el metodo de pago del usuario ")
                                conn = connect_db()
                                desactivar_usuario(conn, res)
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
                            elif resp1 is False:  # retornar
                                resp = 5  # termina el while
                                option = 0
                        else:
                            resp = 5  # para el while
                            option = 0  # retorna 0 porque desea cerrar sesion

        elif option == 2:  # registrar usuario
            conn = connect_db()
            id = registrar_usuario(conn)  # se obtiene su usuario
            conn = connect_db()
            registro_metodo_pago(conn)   # se registra su metodo de pago
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
    print("Su entrada no es válida, feliz día %s" %e)
finally:
    conn.close()
