from Control.validation_request import connect_db, solicitar_datos_fecha, print_tables


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

    conn = connect_db()
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


def crear_admin():
    print("Creacion del admin")
