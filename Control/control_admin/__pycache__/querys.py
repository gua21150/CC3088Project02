"El top 5 de las sesiones que mas usuarios tuvieron en cada hora entre 9:00 a.m a 6:00 p.m para un día dado."
def topsesiones(conn):
    fecha = solicitar_datos_fecha("fecha de busqueda ", 2022)
    query = """Select (extract(hour from s.hora_inicio)::VARCHAR) || ":00:00 -" ||(extract(hour from s.hora_inicio)+1)::VARCHAR||
            ":00:00" "HORA", s.id_sesion, count(extract(hour from sinc.hora_inicio)) usuarios, t.nombres ||""|| t.apellidos instructros, cat.ejercicio categoria"""\
            "From sesion_ejercicio s inner join trabajador t on s.instructor = t.id inner join sincronizacion_ejercicio sinc on s.id_sesion = sinc.id_sesion inner join categoria_ejercicio cat on cat.id_categoria = s.categoria" \
            "where s.fecha = '%s' and extract(hour from sinc.hora_inicio) between 9 and 18"\
            "Group by s.id_sesion, t.nombres, t.apellidos, s.hora_inicio, cat.ejercicio"\
            "order by usuarios desc"\
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
        query = "Select u.nombres || ' '|| u.apellidos usuario, ses.fecha ultima_sesion"\
                "From sesion_ejercicio ses inner join sincronizacion_ejercicio sinc on ses.id_sesion = sinc.id_sesion inner join usuario u on sinc.id_usuario = u.id_usuario"\
                "Where not exists (Select usuario.id_usuario"\
                        "From usuario inner join sincronizacion_ejercicio on usuario.id_usuario = sincronizacion_ejercicio.id_usuario inner join sesion_ejercicio on sincronizacion_ejercicio.id_sesion = sesion_ejercicio.id_sesion"\
                        "Where sesion_ejercicio.fecha <  current_date - interval '3 weeks')"\
                "Group by nombres, apellidos, ultima_sesion"\
                "order by ultima_sesion asc"\
                "limit 20"
        print_tables(query, conn)
