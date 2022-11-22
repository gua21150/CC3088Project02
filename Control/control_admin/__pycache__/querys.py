"El top 5 de las sesiones que mas usuarios tuvieron en cada hora entre 9:00 a.m a 6:00 p.m para un día dado."
def topsesiones(conn):
    fecha = solicitar_datos_fecha("fecha de busqueda ", 2022)
    query = """Select se.fecha "Fecha", rep.id_sesion "Sesion", rep.Hora "Hora", rep.usuarios "Cantidad de usuarios", rep.instructores "Instructor", rep.categoria "Categoria de la Sesion" """\
        "From Reporteria1 rep inner join sesion_ejercicio se on rep.id_sesion = se.id_sesion"\
        "Where se.fecha = '%s'"\
        "Order by usuarios desc"\
        "limit 5" %fecha
    print_tables(query, conn)

"El top 10 de los instructores que los usuarios buscan para una semana dado (de lunes a domingo)"
def topinstructores(conn):
    fecha = solicitar_datos_fecha("fecha de busqueda ", 2022)
    query = """Select semana "Semana consultada", instructor "Instructor", conteo "Cantidad de busquedas" """\
        "From reporteria2"\
        "Where semana = extract(week from '%s'::DATE)"\
        "order by conteo desc"\
        "limit 10" %fecha
    print_tables(query, conn)

"El top 5 de los administradores que más modificaciones realizan en las cuentas de usuario para un rango de fechas dado"
def top5admin(conn):
    fechainicio = solicitar_datos_fecha("fecha de busqueda ", 2022)
    fechafinal = solicitar_datos_fecha("fecha de busqueda ", 2022)
    query = "Create view Reporteria3 as"\
        """Select t.nombres||' '||t.apellidos "Administrador", tipo.descripcion "Tipo de cambio", count(bit.id_admin) "Total de cambios realizados" """\
        "From trabajador t inner join bitacora_admin bit on t.id = bit.id_admin inner join tipo_accion tipo on bit.id_accion = tipo.id_accion"\
        "where fecha_accion between '%s' and '%s' "\
        """Group by "Administrador", "Tipo de cambio"""""\
        """order by "Total de cambios realizados" desc """\
        "limit 5" %(fechainicio, fechafinal)

    print_tables(query, conn)


"El top 20 de usuarios que llevan más de tres semanas sin realizar ejercicio"
def usuariosinactivos(conn): 
        query = """Select usuarios "Nombre usuario", ultima_sesion "Ultima sesion agendada" """\
        "From Reporteria4"\
        "Order by ultima_sesion desc"\
        "limit 20"
        print_tables(query, conn)
