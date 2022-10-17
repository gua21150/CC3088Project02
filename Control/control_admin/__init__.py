from Control.function_validation import solicitar_fecha, create_pandas_table

""" REPORTERIA """
"""El top 10 de sesiones que más usuarios tuvieron. """


def sesiones_populares(conn):
    query = "SELECT  sin.id_sesion, ce.ejercicio, count(sin.id_sesion) cantidad FROM sincronizacion_ejercicio sin " \
            "INNER JOIN sesion_ejercicio se on se.id_sesion = sin.id_sesion INNER JOIN categoria_ejercicio ce on " \
            "ce.id_categoria = se.categoria GROUP BY  sin.id_sesion, ce.ejercicio ORDER BY  cantidad DESC LIMIT 10; "

    result = create_pandas_table(query, conn)
    conn.close()
    return result


"""Cantidad de sesiones y usuarios por cada categoría, para un rango de fechas dado."""
def sesiones_fecha(conn):
    fecha_inicio = str(solicitar_fecha(" de inicio del rango de busqueda "))
    fecha_fin = str(solicitar_fecha(" de fin del rango de busqueda "))

    query = "Select ejercicio, count(id_sesion) "\
            "from categoria_ejercicio ce, sesion_ejercicio se "\
            "where ce.id_categoria = se.categoria and fecha between '%s' and '%s' "\
            "group by ejercicio;" % (fecha_inicio, fecha_fin)

    result = create_pandas_table(query, conn)
    conn.close()
    return result


""" top 5 entrenadores """
def top_entrenadores(conn):
    query = "SELECT nombres, apellidos, count(id) sesiones_dadas " \
            "FROM trabajador t INNER JOIN sesion_ejercicio ses ON t.id = ses.instructor " \
            "WHERE id_sesion IN ( " \
            "SELECT sinc.id_sesion " \
            "FROM   sincronizacion_ejercicio sinc INNER JOIN sesion_ejercicio ses ON sinc.id_sesion = ses.id_sesion )" \
            "GROUP BY nombres, apellidos ORDER BY sesiones_dadas DESC LIMIT 5;"

    result = create_pandas_table(query, conn)
    conn.close()
    return result


""" La cantidad de cuentas diamante que se han creado en los últimos 6 meses.  """
def cuentas_diamante(conn):
    query = "SELECT COUNT(id_suscripcion) usuarios_diamante "\
            "FROM usuario_suscripcion "\
            "WHERE fecha_inicio > current_date -'6 months'::INTERVAL "\
            "AND fecha_inicio IS NOT NULL AND id_suscripcion = 'IDS_D';"

    result = create_pandas_table(query, conn)
    conn.close()
    return result


""" Para una fecha específica, ¿cuál es la hora pico donde el servicio es más utilizado? """
def hora_pico(conn):
    query = "SELECT COUNT(id_suscripcion) usuarios_diamante " \
            "FROM usuario_suscripcion " \
            "WHERE fecha_inicio > current_date -'6 months'::INTERVAL " \
            "AND fecha_inicio IS NOT NULL AND id_suscripcion = 'IDS_D';"

    result = create_pandas_table(query, conn)
    conn.close()
    return result