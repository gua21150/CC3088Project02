"El top 5 de las sesiones que mas usuarios tuvieron en cada hora entre 9:00 a.m a 6:00 p.m para un día dado."
def topsesiones(conn):
    fecha = solicitar_datos_fecha("fecha de busqueda ", 2022)
    query = "Create view Reporteria1 as" \
            """Select (extract(hour from s.hora_inicio)::VARCHAR) || ":00:00 -" ||(extract(hour from s.hora_inicio)+1)::VARCHAR||
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
    query = "Create view Reporteria2 as"\
            "Select extract(week from fecha) as semana, t.nombres  || ' ' || t.apellidos instructor, count(bit.instructor) conteo"\
            "From bitacora_usuario bit inner join trabajador t on bit.instructor = t.id"\
            "where extract(week from fecha) = 46"\
            "Group by semana, t.nombres, t.apellidos"\
            "order by conteo desc"\
            "limit 10"
    print_tables(query, conn)


