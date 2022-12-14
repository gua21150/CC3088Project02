import datetime
import random

import psycopg2
from Control.validation_request import connect_db, solicitar_datos_fecha, solicitar_hora_sesion_simulacion, \
    random_usuario, random_instructor, random_hour, random_categoria
import pandas as pd
from Control.validation_request import solicitar_datos_fecha, print_tables, solicitar_credenciales




def iniciar_sesion_admin(conn, usern, passw):
    cursor = conn.cursor()
    query = "SELECT trabajador.id, rol " \
            "FROM trabajador " \
            "WHERE correo =%s AND passwordc=%s AND activo = True AND rol between 1 and 4"
    data = (usern, passw)
    cursor.execute(query, data)
    user_data = cursor.fetchone()
    if user_data is not None:
        return user_data
    else:
        return False


""" REPORTERIA """
"""El top 10 de sesiones que más usuarios tuvieron. """


def sesiones_populares(conn):
    query = """SELECT  sin.id_sesion "ID sesión", ce.ejercicio "Categoría", count(sin.id_sesion) Cantidad """ \
            """FROM sincronizacion_ejercicio sin """ \
            "INNER JOIN sesion_ejercicio se on se.id_sesion = sin.id_sesion INNER JOIN categoria_ejercicio ce on " \
            "ce.id_categoria = se.categoria GROUP BY  sin.id_sesion, ce.ejercicio ORDER BY  cantidad DESC LIMIT 10; "

    print_tables(query, conn)


"""Cantidad de sesiones y usuarios por cada categoría, para un rango de fechas dado."""


def sesiones_fecha(conn):
    fecha_inicio = str(solicitar_datos_fecha(" de inicio del rango de busqueda ", 2022))
    fecha_fin = str(solicitar_datos_fecha(" de fin del rango de busqueda ", 2022))
    print("\t\tTotal de sesiones entre %s y %s" % (fecha_inicio, fecha_fin))
    query = """Select ejercicio "Categoría", count(id_sesion) "Total de sesiones" """ \
            "from categoria_ejercicio ce, sesion_ejercicio se " \
            "where ce.id_categoria = se.categoria and fecha between '%s' and '%s' " \
            "group by ejercicio;" % (fecha_inicio, fecha_fin)
    print_tables(query, conn)

    print("\t\tTotal de usuarios en las categorias de fechas entre %s y %s" % (fecha_inicio, fecha_fin))
    query = """select ejercicio "Categoría", count(sinc.id_usuario) "Total de usuarios" """ \
            "from categoria_ejercicio cat inner join sesion_ejercicio ses on cat.id_categoria = ses.categoria " \
            "inner join sincronizacion_ejercicio sinc on ses.id_sesion = sinc.id_sesion " \
            "where ses.fecha between '%s' and '%s' " \
            "group by ejercicio;" % (fecha_inicio, fecha_fin)
    print_tables(query, conn)


""" top 5 entrenadores """


def top_entrenadores(conn):
    query = """SELECT t.nombres||' '||t.apellidos "Entrenador", count(id) "Sesiones dadas" """ \
            "FROM trabajador t INNER JOIN sesion_ejercicio ses ON t.id = ses.instructor " \
            "WHERE id_sesion IN ( " \
            "SELECT sinc.id_sesion " \
            "FROM   sincronizacion_ejercicio sinc INNER JOIN sesion_ejercicio ses ON sinc.id_sesion = ses.id_sesion )" \
            """GROUP BY nombres, apellidos ORDER BY "Sesiones dadas" DESC LIMIT 5;"""

    print_tables(query, conn)


""" La cantidad de cuentas diamante que se han creado en los últimos 6 meses.  """


def cuentas_diamante(conn):
    query = """SELECT COUNT(id_suscripcion) "Usuarios diamante" """ \
            "FROM usuario_suscripcion " \
            "WHERE fecha_inicio > current_date -'6 months'::INTERVAL " \
            "AND fecha_inicio IS NOT NULL AND id_suscripcion = 1;"

    print_tables(query, conn)


""" Para una fecha específica, ¿cuál es la hora pico donde el servicio es más utilizado? """


def hora_pico(conn):
    fecha = solicitar_datos_fecha("fecha de busqueda ", 2022)
    query = """SELECT se.hora_inicio "Hora de inicio", COUNT(sin.id_usuario) "Total de usuarios al principio", """ \
            """se.hora_fin "Hora de finalización", COUNT(sin.id_usuario) "Total de usuarios al finalizar" """ \
            "FROM sincronizacion_ejercicio sin INNER JOIN sesion_ejercicio se ON se.id_sesion = sin.id_sesion " \
            "WHERE se.fecha = '%s' " \
            "GROUP BY se.hora_inicio, se.hora_fin " \
            """ORDER BY "Total de usuarios al principio" DESC LIMIT 3;""" % fecha
    print_tables(query, conn)



"""SIMULACION"""


def simulacion(conn):
        
    print("\t\t Bienvenido al menú de simulación del programa iHealth+, para generar la simulación de un día de actividad deberá:  ")
    print("\t\t Ingresar la fecha y cantidad de usuarios para la actividad:  ")
    
    simFecha = int(input("Ingrese la fecha (YYYY/M/D)"))
    cantidad = int(input("Ingrese la cantidad de usuarios que desea ingresar: " ))
    
    fecha = datetime.strptime(simFecha.get(), '%Y-%m-%d')
    
    cursor = conn.cursor()

    cursor.execute('''SELECT nombres FROM trabajador WHERE rol = 6''')

    listaInstructor = [item for t in cursor.fetchall() for item in t]

    cursor = conn.cursor()

    cursor.execute('''SELECT id_usuario FROM usuario %s''', cantidad)

    prevListaCat = ['Aerobicos', 'Zumba', 'Salsa', 'Pesas' , 'Cardio', 'Yoga', 'Fortalecimiento', 'Resistencia']
    listaUsuario = [item for t in cursor.fetchall() for item in t]
    listaInicio = []
    listaFin = []
    listaCat = []
    listaCal = []
    listaRitmo = []

    for n in range(cantidad):
            print(1)
            inicio = fecha.replace(hour=random.randint(6,22), minute=random.randint(0,59))
            fin = inicio + datetime.timedelta(minutes=random.randint(30,60))
            cat = random.choice(prevListaCat)
            cal = random.randint(150,300)
            ritmo = random.randint(110,180)

            listaInicio.append(inicio)
            listaFin.append(fin)
            listaCat.append(cat)
            listaCal.append(cal)
            listaRitmo.append(ritmo)
        
    data = list(zip(listaUsuario,listaInicio,listaFin,listaCat,listaInstructor,listaCal,listaRitmo))



"""Reporteria Proyecto 3""" 
"""El top 5 de las sesiones que mas usuarios tuvieron en cada hora entre 9:00 a.m a 6:00
p.m para un día dado."""


def bitacora_admin(conn):
    print("Las acciones de los administradores han sido")
    query = """SELECT t.nombres||' '||t.apellidos "Nombre Admin", fecha_accion "Fecha", hora "Hora", """ \
            """ta.descripcion "Accion", bitacora_admin.descripcion "Descripcion" """ \
            "FROM bitacora_admin INNER JOIN trabajador t on bitacora_admin.id_admin = t.id " \
            "INNER JOIN tipo_accion ta on bitacora_admin.id_accion = ta.id_accion " \
            "ORDER BY fecha_accion DESC;"
    print_tables(query, conn)


def bitacora_usuario(conn):
    print("Las acciones de los usuarios han sido")
    query = """SELECT usuario.nickname "Nickname", fecha_accion "Fecha", hora "Hora", """ \
            """ta.descripcion "Accion", bitacora_admin_usuarios.descripcion "Descripcion" """ \
            "FROM bitacora_admin_usuarios INNER JOIN usuario ON " \
            "bitacora_admin_usuarios.id_usuario = usuario.id_usuario " \
            "INNER JOIN tipo_accion ta on bitacora_admin_usuarios.id_accion = ta.id_accion " \
            "ORDER BY fecha_accion DESC;"
    print_tables(query, conn)


"""" Muestra los administradores dentro de la base de datos"""


def mostrar_administradores(conn):
    query = """SELECT id "ID", nombres||' '||apellidos "Nombre Admin", correo "Correo", """ \
            """activo "Estado de actividad", tr.rol "Tipo de rol" """ \
            """FROM trabajador INNER JOIN tipo_rol tr on trabajador.rol = tr.cod_rol WHERE trabajador.rol BETWEEN 2 AND 4"""
    print_tables(query, conn)


""" creacion de cuentas de administrador """


def crear_admin(conn, id_admin, rol):
    data = solicitar_credenciales(conn, "del administrador", 2)

    if data is not False:
        cursor = conn.cursor()  # se conecta a la base de datos
        # realizar nuevo codigo de usuario
        selection = "SELECT nextval('entrenador_sequence')"
        cursor.execute(selection)  # ultimo id de trabajador
        id_trab = cursor.fetchone()
        id_t = id_trab[0]
        # insercion de dato
        insert_script = "INSERT INTO trabajador(id, nombres, apellidos, correo, passwordc, activo, rol) " \
                        "VALUES(%s,%s,%s,%s,%s,%s,%s)"
        insert_values = (id_t, data[0], data[1], data[2], data[3], data[4], data[5])
        cursor.execute(insert_script, insert_values)
        conn.commit()

        cursor.execute("SELECT obtener_nombre(%s,%s)" % (id_admin, rol))
        admin = cursor.fetchone()[0]
        querry_bitacora = "CALL bitacora_admin(%s, %s, %s, %s);"
        descripcion = "El administrador %s creo la cuenta del nuevo administrador %s" % (
            admin, data[0] + ' ' + data[1])
        data_bitacora = (id_admin, rol, descripcion, 1)
        cursor.execute(querry_bitacora, data_bitacora)
        conn.commit()
        print("Registro realizado\nSe mostraran los administradores")
        mostrar_administradores(conn)
    else:
        print("Tus datos no son validos")


"""" dar de baja a un administrador """
def dar_baja_administrador(conn, id_trabajador, id_admin, rol_admin):
    cursor = conn.cursor()
    cursor.execute("SELECT rol FROM trabajador WHERE id = %s AND activo = True AND rol!=1" % id_trabajador)
    validation = cursor.fetchone()
    if validation is not None:
        query = "UPDATE trabajador set activo = False where id = %s" % id_trabajador
        cursor.execute(query)
        conn.commit()

        # registro en bitacora
        rol_trabajador = validation[0]
        cursor.execute("SELECT obtener_nombre(%s,%s)", (id_admin, rol_admin))
        admin_name = cursor.fetchone()[0]
        cursor.execute("SELECT obtener_nombre(%s,%s)", (id_trabajador, rol_trabajador))
        trab_name = cursor.fetchone()[0]
        querry_bitacora = "CALL bitacora_admin(%s, %s, %s, %s);"
        descripcion = "El administrador %s modifico el estado de actividad del entrenador %s a INACTIVO" % (
        admin_name, trab_name)
        data_bitacora = (id_admin, rol_admin, descripcion, 2)
        cursor.execute(querry_bitacora, data_bitacora)
        conn.commit()
        print("Se ha desactivado al administrador\nA continuación puede ver el cambio")
        mostrar_administradores(conn)
    else:
        print("Este administrador ya se encuentra INACTIVO o no puede desactivar este admin")


def activar_administrador(conn, id_trabajador, id_admin, rol_admin):
    cursor = conn.cursor()
    cursor.execute("SELECT rol FROM trabajador WHERE id = %s AND activo = False" % id_trabajador)
    validation = cursor.fetchone()
    if validation is not None:
        query = "UPDATE trabajador set activo = True WHERE id = %s" % id_trabajador
        cursor.execute(query)
        conn.commit()

        # registro en bitacora
        rol_trabajador = validation[0]
        cursor.execute("SELECT obtener_nombre(%s,%s)", (id_admin, rol_admin))
        admin_name = cursor.fetchone()[0]
        cursor.execute("SELECT obtener_nombre(%s,%s)", (id_trabajador, rol_trabajador))
        trab_name = cursor.fetchone()[0]
        querry_bitacora = "CALL bitacora_admin(%s, %s, %s, %s);"
        descripcion = "El administrador %s modifico el estado de actividad del administrador %s a ACTIVO" % (
        admin_name, trab_name)
        data_bitacora = (id_admin, rol_admin, descripcion, 2)
        cursor.execute(querry_bitacora, data_bitacora)
        conn.commit()
        print("Se ha desactivado al entrenador\nA continuación puede ver el cambio")
        mostrar_administradores(conn)
    else:
        print("Este administrador ya se encuentra ACTIVO o no puede activar este admin")

"El top 5 de las sesiones que mas usuarios tuvieron en cada hora entre 9:00 a.m a 6:00 p.m para un día dado."
def topsesiones(conn):
    fecha = solicitar_datos_fecha("fecha de busqueda ", 2022)
    query = """Select se.fecha "Fecha", rep.id_sesion "Sesion", rep.Hora "Hora", rep.usuarios "Cantidad de usuarios", rep.instructores "Instructor", rep.categoria "Categoría de la sesión" """\
        "From Reporteria1 rep inner join sesion_ejercicio se on rep.id_sesion = se.id_sesion " \
        "Where se.fecha = '%s' "\
        "Order by usuarios desc "\
        "limit 5" % fecha
    print_tables(query, conn)

"El top 10 de los instructores que los usuarios buscan para una semana dado (de lunes a domingo)"
def topinstructores(conn):
    fecha = solicitar_datos_fecha("fecha de busqueda ", 2022)
    query = """Select semana "Semana consultada", instructor "Instructor", conteo "Cantidad de busquedas" """\
        "From reporteria2 "\
        "Where semana = extract(week from '%s'::DATE) "\
        "order by conteo desc "\
        "limit 10" % fecha
    print_tables(query, conn)

"El top 5 de los administradores que más modificaciones realizan en las cuentas de usuario para un rango de fechas dado"
def top5admin(conn):
    fechainicio = solicitar_datos_fecha("fecha de busqueda ", 2022)
    fechafinal = solicitar_datos_fecha("fecha de busqueda ", 2022)
    query = "Create or replace view Reporteria3 as "\
            """Select t.nombres||' '||t.apellidos "Administrador", tipo.descripcion "Tipo de cambio", count(bit.id_admin) "Total de cambios realizados" """ \
            "From trabajador t inner join bitacora_admin bit on t.id = bit.id_admin inner join tipo_accion tipo on bit.id_accion = tipo.id_accion " \
            "where fecha_accion between %s and %s " \
            """Group by "Administrador", "Tipo de cambio" """ \
            """order by "Total de cambios realizados" desc limit 5;"""
    cursor = conn.cursor()
    cursor.execute(query, (fechainicio, fechafinal))
    conn.commmit()
    query = "SELECT * FROM reporteria3"
    print_tables(query, conn)


"El top 20 de usuarios que llevan más de tres semanas sin realizar ejercicio"
def usuariosinactivos(conn): 
        query = """Select usuarios "Nombre usuario", ultima_sesion "Ultima sesion agendada" """\
        "From Reporteria4 "\
        "Order by ultima_sesion desc "\
        "limit 20"
        print_tables(query, conn)


def asignar_usario_simulacion(conn, asignacion, usuarios, sesiones, id_admin, rol):
    i = 0
    while i != asignacion:
        cantidad_usuarios = len(usuarios) - 1
        posible_usuario = random.randint(0, cantidad_usuarios)
        id_usuario = usuarios[posible_usuario]
        id_sesion = sesiones[random.randint(0, len(sesiones)-1)]  # sesion a la que es asignado el usuario

        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM sincronizacion_ejercicio WHERE id_usuario=%s and id_sesion=%s", (id_usuario, id_sesion))
        validation = cursor.fetchone()
        if validation is None:
            query = "SELECT hora_inicio, hora_fin FROM sesion_ejercicio WHERE id_sesion=%s"
            cursor.execute(query, (id_sesion, ))
            hora = cursor.fetchone()
            hi = hora[0]
            hf = hora[1]

            query = "INSERT INTO sincronizacion_ejercicio (id_usuario, id_sesion, hora_inicio, hora_fin, calorias_quemadas, ritmo_cardiaco) VALUES (%s,%s,%s,%s,%s,%s)"
            pul = round(random.uniform(80.00, 160.00), 2)
            cal = round(random.uniform(200.00, 1000.00), 2)
            cursor.execute(query, (id_usuario, id_sesion, hi, hf, cal, pul))
            conn.commit()

            cursor.execute("SELECT obtener_nombre(%s, %s)" % (id_admin, rol))
            querry_bitacora = "CALL bitacora_admin(%s, %s, %s, %s);"
            descripcion = "El administrador %s creó un nuevo registro de sesión en %s en sincronizacion_ejercicio como parte de simulación" % (
                cursor.fetchone()[0], id_sesion)
            data_bitacora = (id_admin, rol, descripcion, 1)
            cursor.execute(querry_bitacora, data_bitacora)
            conn.commit()

        i = i + 1

def simulacion_mariel(conn, id_admin, rol):
    fecha = solicitar_datos_fecha("del día de simulación", 2022)
    cantidad_usuarios = int(input("Ingresa la cantidad de usuarios "))
    #cantidad_sesiones = int(input("Ingresa la cantidad de sesiones "))
    cantidad_sesiones = 5
    if (fecha is not False) and cantidad_sesiones>0 and cantidad_usuarios>0:
        i = 0
        id_sesiones = []

        while i != cantidad_sesiones:
            hora_inicio, hora_final = random_hour()
            entrenador = random_instructor(conn, hora_inicio, hora_final, fecha)
            categoria = random_categoria()

            if entrenador is not False:
                cursor = conn.cursor()  # se conecta a la base de datos
                # realizar nuevo codigo de usuario
                selection = "SELECT nextval('sesion_sequence')"
                cursor.execute(selection)  # ultimo usuario
                id_sesion = cursor.fetchone()
                id_u = id_sesion[0]
                id_sesiones.append(id_u)  # se guardan las sesiones agregadas
                # insercion de dato
                insert_script = "INSERT INTO sesion_ejercicio(id_sesion, fecha, hora_inicio, hora_fin, duracion, instructor, " \
                                "categoria) VALUES(%s,%s,%s,%s,%s,%s,%s)"
                insert_values = (id_u, fecha, hora_inicio, hora_final, 60, entrenador, categoria)
                cursor.execute(insert_script, insert_values)
                conn.commit()
                # registro en bitacora
                cursor.execute("SELECT obtener_nombre(%s,%s)" % (id_admin, rol))
                admin_name = cursor.fetchone()[0]
                querry_bitacora = "CALL bitacora_admin(%s, %s, %s, %s);"
                descripcion = "El administrador %s creó la sesión %s durante simulación" % (admin_name, id_u)
                data_bitacora = (id_admin, rol, descripcion, 1)
                cursor.execute(querry_bitacora, data_bitacora)
                conn.commit()
                i = i+1
            else:
                break

        usuarios_disponibles = random_usuario(conn)
        if usuarios_disponibles is not False:
            cantidad_u_dis = len(usuarios_disponibles)
            if cantidad_u_dis < cantidad_usuarios:
                print("Hay menos usuarios disponibles que los ingresados, se hara la simulacion con %s usuarios" % cantidad_u_dis)

            asignar_usario_simulacion(conn, cantidad_usuarios, usuarios_disponibles, id_sesiones, id_admin, rol)
            query = "SELECT * from "
        else:
            print("No hay usuarios disponibles para esta simulacion")
    else:
        print("El dato de fecha no es correcto")