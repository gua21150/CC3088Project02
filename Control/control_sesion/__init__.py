from ..validation_request import solicitar_datos_fecha, solicitar_hora, solicitar_duracion, solicitar_categoria, \
    solicitar_entrenador, solicitar_hora_busqueda, solicitar_hora_sincronizacion, solicitar_ritmo_cardiaco_calorias
from Control.control_entrenador_nutricionista import mostrar_entrenadores_activos
import pandas as pd

""" categorias disponibles"""


def mostrar_categorias_ejercicio(conn):
    query = "SELECT  id_categoria, ejercicio FROM categoria_ejercicio"
    result = pd.read_sql(query, conn)
    print(result)


""" solicitar datos para registrar un nuevo entrenador """


def solicitar_datos_sesion(conn):
    try:
        print("\tA continuación se te solicitará información para crear la sesión")
        print("\tSI ALGUNO DE LOS DATOS ES INCORRECTO SE TE NOTIFICARÁ")
        fecha = solicitar_datos_fecha(" para la sesión ", 2022)
        data = solicitar_hora(" de la sesión ")
        if data is not False:
            hora_inicio, hora_final, tiempo = data
            mostrar_entrenadores_activos(conn, hora_inicio, hora_final, fecha)
            entrenador = int(input("¿A quién le asignarás esta sesión? Ingresa su id\n*Si no se mostraron "
                                   "entrenadores, quiere decir que no hay datos disponibles*?"))
            mostrar_categorias_ejercicio(conn)
            categoria = int(input("¿De qué será la sesión? Ingresa el código"))

            return fecha, hora_inicio, hora_final, tiempo, entrenador, categoria
    except:
        print("Los datos ingresados no son válidos, tendrá que regresar a esta parte del menú")
        return False


"""" registro de la sesion dentro de la base de datos """


def registrar_sesion(conn):
    data = solicitar_datos_sesion(conn)  # solicitar informacion de la sesion

    if data is not False:
        cursor = conn.cursor()  # se conecta a la base de datos
        # realizar nuevo codigo de usuario
        selection = "SELECT nextval('sesion_sequence')"
        cursor.execute(selection)  # ultimo usuario
        id_sesion = cursor.fetchone()
        id_u = id_sesion[0]
        # insercion de dato
        insert_script = "INSERT INTO sesion_ejercicio(id_sesion, fecha, hora_inicio, hora_fin, duracion, instructor, " \
                        "categoria) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        insert_values = (id_u, data[0], data[1], data[2], data[3], data[4], data[5])
        cursor.execute(insert_script, insert_values)
        conn.commit()
        print("Registro realizado\nSe mostraran las sesiones ")
        mostrar_sesiones(conn)
    else:
        print("La sesion no se pudo registrar debido a error en los datos ingresados, puede ser por falta de "
              "entrenadores")


""" Desactiva la sesion indicada """


def modificar_sesion(conn, id_sesion, id_categoria):
    cursor = conn.cursor()
    query = "UPDATE sesion_ejercicio SET categoria = %s WHERE id_sesion = %s" % (id_categoria, id_sesion)
    cursor.execute(query)
    conn.commit()
    print("Se ha modificado la categoría de la sesión %s\nA continuación puede ver el cambio" % id_sesion)
    mostrar_sesiones(conn)


""" Desactiva la sesion indicada """


def dar_baja_sesion(conn, id_sesion):
    cursor = conn.cursor()
    query = "DELETE FROM sesion_ejercicio WHERE id_sesion = %s" % id_sesion
    cursor.execute(query)
    conn.commit()
    print("Se ha eliminado la sesión\nA continuacion puede ver el cambio")
    mostrar_sesiones(conn)


""" mostrar sesiones que pueden ser modificadas """


def mostrar_sesiones_modificar(conn):
    query = "SELECT ses.id_sesion, ses.fecha, ses.hora_inicio,ses.hora_fin, ce.ejercicio, t.nombres, t.apellidos " \
            "FROM  sesion_ejercicio ses INNER JOIN categoria_ejercicio ce on ce.id_categoria = ses.categoria " \
            "INNER JOIN trabajador t on t.id = ses.instructor " \
            "WHERE ses.fecha > current_date"
    result = pd.read_sql(query, conn)
    print(result)


""" mostrar las sesiones dentro de la base de datos """


def mostrar_sesiones(conn):
    query = """SELECT ses.id_sesion, ses.fecha, ses.hora_inicio,ses.hora_fin, ce.ejercicio, t.nombres||' '||t.apellidos "Entrenador" """ \
            "FROM  sesion_ejercicio ses INNER JOIN categoria_ejercicio ce on ce.id_categoria = ses.categoria " \
            "INNER JOIN trabajador t on t.id = ses.instructor ORDER BY fecha DESC"
    result = pd.read_sql(query, conn)
    print(result)


""" mostrar las sesiones disponibles en la base de datos de la presente semana a los usuarios """


def mostrar_sesiones_semanales(conn):
    query = """SELECT ses.id_sesion, cat.ejercicio, ses.fecha, ses.hora_inicio, ses.hora_fin, t.nombres||' '||t.apellidos "Instructor" """ \
            "from sesion_ejercicio ses inner join categoria_ejercicio cat on ses.categoria = cat.id_categoria " \
            "                         inner join trabajador t on ses.instructor=t.id " \
            "WHERE fecha between current_date and current_date+'1 week'::interval; "
    print(pd.read_sql(query, conn))

    try:
        inscribir = int(input("¿Deseas agendarte a alguna sesión?\n[1] Sí\n[2]No"))
        if inscribir == 1:
            eleccion = int(input("Ingrese el id de la sesion a la que desea conectarse \n\t"))
            return eleccion
        else:
            return False
    except ValueError:
        print("Tu entrada no es válida")
        return False


""" mostrar sesiones por la fecha """


def mostrar_sesiones_fecha(conn):
    fecha = solicitar_datos_fecha('de la sesión', 2022)

    query = """SELECT ses.id_sesion, cat.ejercicio, ses.fecha, ses.hora_inicio, ses.hora_fin, t.nombres||' '||t.apellidos "Instructor" """ \
            "from sesion_ejercicio ses inner join categoria_ejercicio cat on ses.categoria = cat.id_categoria " \
            "                         inner join trabajador t on ses.instructor=t.id " \
            "WHERE fecha='%s' and fecha>=current_date;" % fecha
    print(pd.read_sql(query, conn))

    try:
        inscribir = int(input("¿Deseas agendarte a alguna sesión?\n[1] Sí\n[2]No"))
        if inscribir == 1:
            eleccion = int(input("Ingrese el id de la sesion a la que desea conectarse \n\t"))
            return eleccion
        else:
            return False
    except ValueError:
        print("Tu entrada no es válida")
        return False


""" mostrar sesiones por el horario """


def mostrar_sesiones_horario(conn):
    data = solicitar_hora_busqueda('de la sesión')
    if data is not False:
        hi = data[0]
        hf = data[1]
        query = """SELECT ses.id_sesion, cat.ejercicio, ses.fecha, ses.hora_inicio, ses.hora_fin, t.nombres||' '||t.apellidos "Instructor" """ \
                "from sesion_ejercicio ses inner join categoria_ejercicio cat on ses.categoria = cat.id_categoria " \
                "inner join trabajador t on ses.instructor=t.id " \
                "WHERE ses.fecha>=current_date and ((EXTRACT(HOUR FROM ses.hora_inicio))" \
                "BETWEEN EXTRACT(HOUR FROM time'%s') AND EXTRACT(HOUR FROM time'%s')) AND " \
                "((EXTRACT(HOUR FROM ses.hora_fin)) " \
                "BETWEEN EXTRACT(HOUR FROM time'%s') AND EXTRACT(HOUR FROM time'%s'))" % (hi, hf, hi, hf)

        print(pd.read_sql(query, conn))
        try:
            inscribir = int(input("¿Deseas agendarte a alguna sesión?\n[1] Sí\n[2]No"))
            if inscribir == 1:
                eleccion = int(input("Ingrese el id de la sesion a la que desea conectarse \n\t"))
                return eleccion
            else:
                return False
        except ValueError:
            print("Tu entrada no es válida")
            return False
    else:
        return False


""" mostrar sesiones por la duracion """


def mostrar_sesiones_duracion(conn):
    duracion = solicitar_duracion()
    query = """SELECT ses.id_sesion, cat.ejercicio, ses.fecha, ses.hora_inicio, ses.duracion, t.nombres||' '||t.apellidos "Instructor" """ \
            "from sesion_ejercicio ses inner join categoria_ejercicio cat on ses.categoria = cat.id_categoria " \
            "                         inner join trabajador t on ses.instructor=t.id " \
            "WHERE ses.duracion=%s and ses.fecha>=current_date" % duracion

    print(pd.read_sql(query, conn))
    try:
        inscribir = int(input("¿Deseas agendarte a alguna sesión?\n[1] Sí\n[2]No"))
        if inscribir == 1:
            eleccion = int(input("Ingrese el id de la sesion a la que desea conectarse \n\t"))
            return eleccion
        else:
            return False
    except ValueError:
        print("Tu entrada no es válida")
        return False


""" mostrar sesiones por categoria """


def mostrar_sesiones_categoria(conn):
    categoria = solicitar_categoria(conn)
    query = """SELECT ses.id_sesion, cat.ejercicio, ses.fecha, ses.hora_inicio, ses.hora_fin, t.nombres||' '||t.apellidos "Instructor" """ \
            "from sesion_ejercicio ses inner join categoria_ejercicio cat on ses.categoria = cat.id_categoria " \
            "                         inner join trabajador t on ses.instructor=t.id " \
            "WHERE cat.id_categoria=%s and ses.fecha>=current_date" % categoria
    print(pd.read_sql(query, conn))
    try:
        inscribir = int(input("¿Deseas agendarte a alguna sesión?\n[1] Sí\n[2]No"))
        if inscribir == 1:
            eleccion = int(input("Ingrese el id de la sesión a la que desea conectarse \n\t"))
            return eleccion
        else:
            return False
    except ValueError:
        print("Tu entrada no es válida")
        return False


""" mostrar sesiones por categoria """


def mostrar_sesiones_entrenador(conn, id_usuario):
    entrenador = solicitar_entrenador(conn)
    query = """SELECT ses.id_sesion, cat.ejercicio, ses.fecha, ses.hora_inicio, ses.hora_fin, t.nombres||' '||t.apellidos "Instructor" """ \
            "from sesion_ejercicio ses inner join categoria_ejercicio cat on ses.categoria = cat.id_categoria " \
            "                         inner join trabajador t on ses.instructor=t.id " \
            "WHERE t.id=%s and ses.fecha>=current_date" % entrenador
    print(pd.read_sql(query, conn))
    cursor = conn.cursor()
    cursor.execute("CALL bitacora_busqueda_usuario(%s, %s)", (id_usuario, entrenador))
    conn.commit()
    try:
        inscribir = int(input("¿Deseas agendarte a alguna sesión?\n[1] Sí\n[2]No"))
        if inscribir == 1:
            eleccion = int(input("Ingrese el id de la sesión a la que desea conectarse \n\t"))
            return eleccion
        else:
            return False
    except ValueError:
        print("Tu entrada no es válida")
        return False


""" agenda al usuario a la sesion indicada """


def agendar_sesion(conn, id_usuario, id_sesion):
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM sincronizacion_ejercicio WHERE id_usuario=%s and id_sesion=%s",
                   (id_usuario, id_sesion))
    validation = cursor.fetchone()
    if validation is None:
        query = "INSERT INTO sincronizacion_ejercicio (id_usuario, id_sesion) VALUES (%s,%s)"
        cursor.execute(query, (id_usuario, id_sesion))
        conn.commit()

        cursor.execute("SELECT obtener_nombre(%s, 5)" % id_usuario)
        querry_bitacora = "CALL bitacora_admin(%s, %s, %s, %s);"
        descripcion = "El usuario %s creo un nuevo registro de sesion %s en sincronizacion_ejercicio" % (
            cursor.fetchone()[0], id_sesion)
        data_bitacora = (id, 5, descripcion, 1)
        cursor.execute(querry_bitacora, data_bitacora)
        conn.commit()
    else:
        print("Ya te encuentras agendado a esta sesion")


def mis_sesiones_semanales(conn, id_usuario):
    query = """SELECT ses.id_sesion, cat.ejercicio, ses.fecha, ses.hora_inicio, """ \
            """ses.hora_fin, t.nombres||' '||t.apellidos "Instructor" """ \
            "from sincronizacion_ejercicio sinc inner join usuario us on sinc.id_usuario = us.id_usuario " \
            "                                   inner join sesion_ejercicio ses on sinc.id_sesion = ses.id_sesion " \
            "                                   inner join trabajador t on ses.instructor = t.id " \
            "inner join categoria_ejercicio cat on ses.categoria = cat.id_categoria " \
            "where ses.fecha > current_date + interval '-1 week' and sinc.id_usuario = %s" % id_usuario
    print(pd.read_sql(query, conn))


def mis_sesiones_diarias(conn, id_usuario):
    cursor = conn.cursor()
    query = """SELECT ses.id_sesion, cat.ejercicio, ses.fecha, ses.hora_inicio, ses.hora_fin, t.nombres||' 
    '||t.apellidos "Instructor" """ \
            "from sincronizacion_ejercicio sinc inner join usuario us on sinc.id_usuario = us.id_usuario " \
            "inner join sesion_ejercicio ses on sinc.id_sesion = ses.id_sesion " \
            "inner join trabajador t on ses.instructor = t.id " \
            "inner join categoria_ejercicio cat on ses.categoria = cat.id_categoria " \
            "where fecha = current_date and sinc.id_usuario=%s" % id_usuario
    cursor.execute(query)
    validation = cursor.fetchall()
    if validation is None:
        print("No tienes sesiones el dia de hoy")
    else:
        print(pd.read_sql(query, conn))
        try:
            unirme = int(input("¿Deseas unirte a esta sesión?\n[1] Sí\n[2] No"))
            eleccion = 0
            hi, hf = "", ""
            if unirme == 1:
                bandier = False
                while bandier is False:
                    eleccion = int(input("Ingrese el id de la sesión a la que desea conectarse \n\t"))

                    for i in validation:
                        if i[0] == eleccion:
                            bandier = True
                            break

                    if bandier is True:
                        hi = i[3]
                        hf = i[4]
                    else:
                        print("La sesion que indicas no es valida\nVuelve a intentar ingresar la sesion")
                query = "SELECT 1 FROM sincronizacion_ejercicio WHERE calorias_quemadas=Null AND id_usuario=%s AND id_sesion=%s"
                cursor.execute(query, (id_usuario, eleccion))
                validation = cursor.fetchone()

                if validation is not None:
                    print("Se te pediran los datos de tu sincronizacion a la sesion seleccionada")
                    hora = solicitar_hora_sincronizacion(hi, hf)
                    if hora is not False:
                        pul, cal = solicitar_ritmo_cardiaco_calorias()
                        query = "UPDATE sincronizacion_ejercicio SET hora_inicio = %s, hora_fin = %s, " \
                                "ritmo_cardiaco = %s, calorias_quemadas = %s " \
                                "WHERE id_usuario = %s AND id_sesion = %s"
                        update = (hora[0], hora[1], pul, cal, id_usuario, eleccion)
                        cursor.execute(query, update)
                        conn.commit()

                        cursor.execute("SELECT obtener_nombre(%s, 5)" % id_usuario)
                        querry_bitacora = "CALL bitacora_admin(%s, %s, %s, %s);"
                        descripcion = "El usuario %s modifico el registro de su sesion %s en sincronizacion_ejercicio" % (
                            cursor.fetchone()[0], eleccion)
                        data_bitacora = (id_usuario, 5, descripcion, 2)
                        cursor.execute(querry_bitacora, data_bitacora)
                        conn.commit()
                else:
                     print("Ya te has unido a esta sesion")
            else:
                return False
        except ValueError:
            print("Tu entrada no es válida")
            return False
