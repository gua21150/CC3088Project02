from Control.validation_request import create_pandas_table, connect_db, solicitar_datos_fecha

def iniciar_sesion_admin(conn, usern, passw):
    cursor = conn.cursor()
    query = "SELECT trabajador.id "\
            "FROM trabajador "\
            "WHERE correo =%s AND passwordc=%s AND activo = True AND rol='IDR_AD'"
    # cambiar idr_ad
    data = (usern, passw)
    cursor.execute(query, data)
    user_data = cursor.fetchone()
    if user_data != 'None':
        return True
    else:
        return False


""" REPORTERIA """
"""El top 10 de sesiones que más usuarios tuvieron. """
def sesiones_populares(conn):
    query = "SELECT  sin.id_sesion, ce.ejercicio, count(sin.id_sesion) cantidad FROM sincronizacion_ejercicio sin " \
            "INNER JOIN sesion_ejercicio se on se.id_sesion = sin.id_sesion INNER JOIN categoria_ejercicio ce on " \
            "ce.id_categoria = se.categoria GROUP BY  sin.id_sesion, ce.ejercicio ORDER BY  cantidad DESC LIMIT 10; "

    result = create_pandas_table(query, conn)
    print(result)


"""Cantidad de sesiones y usuarios por cada categoría, para un rango de fechas dado."""
def sesiones_fecha(conn):
    fecha_inicio = str(solicitar_datos_fecha(" de inicio del rango de busqueda ", 2022))
    fecha_fin = str(solicitar_datos_fecha(" de fin del rango de busqueda ", 2022))
    print("\t\tTotal de sesiones entre %s y %s" % (fecha_inicio, fecha_fin))
    query = "Select ejercicio, count(id_sesion) "\
            "from categoria_ejercicio ce, sesion_ejercicio se "\
            "where ce.id_categoria = se.categoria and fecha between '%s' and '%s' "\
            "group by ejercicio;" % (fecha_inicio, fecha_fin)

    result = create_pandas_table(query, conn)
    print(result)
    conn = connect_db()
    print("\t\tTotal de usuarios en las categorias de fechas entre %s y %s" % (fecha_inicio, fecha_fin))
    query = "select ejercicio, count(sinc.id_usuario) " \
            "from categoria_ejercicio cat inner join sesion_ejercicio ses on cat.id_categoria = ses.categoria " \
            "inner join sincronizacion_ejercicio sinc on ses.id_sesion = sinc.id_sesion "\
            "where ses.fecha between '%s' and '%s' " \
            "group by ejercicio;" % (fecha_inicio, fecha_fin)
    result = create_pandas_table(query, conn)
    print(result)

""" top 5 entrenadores """
def top_entrenadores(conn):
    query = "SELECT nombres, apellidos, count(id) sesiones_dadas " \
            "FROM trabajador t INNER JOIN sesion_ejercicio ses ON t.id = ses.instructor " \
            "WHERE id_sesion IN ( " \
            "SELECT sinc.id_sesion " \
            "FROM   sincronizacion_ejercicio sinc INNER JOIN sesion_ejercicio ses ON sinc.id_sesion = ses.id_sesion )" \
            "GROUP BY nombres, apellidos ORDER BY sesiones_dadas DESC LIMIT 5;"

    result = create_pandas_table(query, conn)
    print(result)


""" La cantidad de cuentas diamante que se han creado en los últimos 6 meses.  """
def cuentas_diamante(conn):
    query = "SELECT COUNT(id_suscripcion) usuarios_diamante "\
            "FROM usuario_suscripcion "\
            "WHERE fecha_inicio > current_date -'6 months'::INTERVAL "\
            "AND fecha_inicio IS NOT NULL AND id_suscripcion = 'IDS_D';"

    result = create_pandas_table(query, conn)
    print(result)


""" Para una fecha específica, ¿cuál es la hora pico donde el servicio es más utilizado? """
def hora_pico(conn):
    fecha = solicitar_datos_fecha("fecha de busqueda ", 2022)
    query = "SELECT se.hora_inicio, COUNT(sin.id_usuario) total_personas, se.hora_fin, COUNT(sin.id_usuario) total_personas "\
            "FROM sincronizacion_ejercicio sin INNER JOIN sesion_ejercicio se ON se.id_sesion = sin.id_sesion "\
            "WHERE se.fecha = '%s' "\
            "GROUP BY se.hora_inicio, se.hora_fin "\
            "ORDER BY total_personas DESC LIMIT 3;" %fecha

    result = create_pandas_table(query, conn)
    print(result)
