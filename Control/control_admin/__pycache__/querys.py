"El top 5 de las sesiones que mas usuarios tuvieron en cada hora entre 9:00 a.m a 6:00 p.m para un día dado."
def topsesiones(conn):
    fecha = solicitar_datos_fecha("fecha de busqueda ", 2022)
    query ="""Select se.fecha "Fecha", rep.id_sesion "Sesion", rep.Hora "Hora", rep.usuarios "Cantidad de usuarios", rep.instructores "Instructor", rep.categoria "Categoria de la Sesion"""""\
        "From Reporteria1 rep inner join sesion_ejercicio se on rep.id_sesion = se.id_sesion"\
        "Where se.fecha = '2022-10-13'"\
        "Order by usuarios desc"\
        "limit 5"
    print_tables(query, conn)

"El top 10 de los instructores que los usuarios buscan para una semana dado (de lunes a domingo)"
def topinstructores(conn):
    fecha = solicitar_datos_fecha("fecha de busqueda ", 2022)
    query = "Select extract(week from fecha) as semana, t.nombres  || ' ' || t.apellidos instructor, count(bit.instructor) conteo"\
            "From bitacora_usuario bit inner join trabajador t on bit.instructor = t.id"\
            "where extract(week from fecha) = 46"\
            "Group by semana, t.nombres, t.apellidos"\
            "order by conteo desc"\
            "limit 10"
    print_tables(query, conn)

"El top 5 de los administradores que más modificaciones realizan en las cuentas de usuario para un rango de fechas dado"
def top5admin(conn):
    fecha = solicitar_datos_fecha("fecha de busqueda ", 2022)
    query = "Select t.nombres nombres, t.apellidos apellidos, count(bit.id_admin) cambios_realizados, tipo.descripcion categoria, count(bit.id_accion)"\
            "From trabajador t inner join bitacora_admin bit on t.id = bit.id_admin inner join tipo_accion tipo on bit.id_accion = tipo.id_accion"\
            "where fecha_accion between '2022-10-15' and '2022-10-30'"\
            "Group by nombres, apellidos, categoria"\
            "order by cambios_realizados desc"\
            "limit 5"
    print_tables(query, conn)

"El top 20 de usuarios que llevan más de tres semanas sin realizar ejercicio"
def usuariosinactivos(conn):
        fecha = solicitar_datos_fecha("fecha de busqueda ", 2022)
        query = """Select usuarios "Nombre usuario", ultima_sesion "Ultima sesion agendada"""""\
        "From Reporteria4"\
        "Order by ultima_sesion desc"\
        "limit 20"
        print_tables(query, conn)
