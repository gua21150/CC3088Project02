from Control.validation_request import create_pandas_table, solicitar_datos_fecha, connect_db, solicitar_hora
from Control.control_entrenador_nutricionista import mostrar_entrenadores_activos

""" categorias disponibles"""
def mostrar_categorias_ejercicio(conn):
    query = "SELECT  id_categoria, ejercicio FROM categoria_ejercicio"

    result = create_pandas_table(query, conn)
    print(result)


""" solicitar datos para registrar un nuevo entrenador """
def solicitar_datos_sesion(conn):
    try:
        print("\tA continuación se te solicitará información para crear la sesión")
        print("\tSI ALGUNO DE LOS DATOS ES INCORRECTO SE TE NOTIFICARÁ")
        bandier = True
        fecha = solicitar_datos_fecha(" para la sesión ", 2022)
        data = solicitar_hora(" de la sesión ")
        if data is not False:
            hora_inicio, hora_final, tiempo = data

            mostrar_entrenadores_activos(conn, hora_inicio, hora_final, fecha)
            entrenador = str(input("¿A quién le asignarás esta sesión? Ingresa su id\n*Si no se mostraron entrenadores, quiere decir que no hay datos disponibles*?"))
            mostrar_categorias_ejercicio(conn)
            categoria = str(input("¿De qué será la sesión? Ingresa el código"))

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
        selection = "SELECT 'IDEj_'||(nextval('sesion_sequence')::VARCHAR)"
        cursor.execute(selection)  # ultimo usuario
        id_sesion = cursor.fetchone()
        id_u = id_sesion[0]
        # insercion de dato
        insert_script = "INSERT INTO sesion_ejercicio(id_sesion, fecha, hora_inicio, hora_fin, duracion, instructor, categoria) " \
                        "VALUES(%s,%s,%s,%s,%s,%s,%s)"
        insert_values = (id_u, data[0], data[1], data[2], data[3], data[4], data[5])
        cursor.execute(insert_script, insert_values)
        conn.commit()
        print("Registro realizado\nSe mostraran las sesiones ")
        mostrar_sesiones(conn)
    else:
        print("La sesion no se pudo registrar debido a error en los datos ingresados, puede ser por falta de entrenadores")


""" Desactiva la sesion indicada """
def modificar_sesion(conn, id_sesion, id_categoria):
    cursor = conn.cursor()
    query = "UPDATE sesion_ejercicio SET categoria = '%s' WHERE id_sesion = '%s'" % (id_categoria, id_sesion)
    cursor.execute(query)
    conn.commit()
    print("Se ha modificado la categoría de la sesión '%s'\nA continuación puede ver el cambio" %id_sesion)
    mostrar_sesiones(conn)


""" Desactiva la sesion indicada """
def dar_baja_sesion(conn, id_sesion):
    cursor = conn.cursor()
    query = "DELETE FROM sesion_ejercicio WHERE id_sesion = '%s'" %id_sesion
    cursor.execute(query)
    conn.commit()
    print("Se ha eliminado la sesión\nA continuacion puede ver el cambio")
    mostrar_sesiones(conn)


""" mostrar sesiones que pueden ser modificadas """
def mostrar_sesiones_modificar(conn):
    query = "SELECT ses.id_sesion, ses.fecha, ses.hora_inicio,ses.hora_fin, ce.ejercicio, t.nombres, t.apellidos "\
            "FROM  sesion_ejercicio ses INNER JOIN categoria_ejercicio ce on ce.id_categoria = ses.categoria " \
            "INNER JOIN trabajador t on t.id = ses.instructor "\
            "WHERE ses.fecha > current_date"
    result = create_pandas_table(query, conn)
    print(result)


""" mostrar las sesiones dentro de la base de datos """
def mostrar_sesiones(conn):
    query = "SELECT ses.id_sesion, ses.fecha, ses.hora_inicio,ses.hora_fin, ce.ejercicio, t.nombres, t.apellidos " \
            "FROM  sesion_ejercicio ses INNER JOIN categoria_ejercicio ce on ce.id_categoria = ses.categoria " \
            "INNER JOIN trabajador t on t.id = ses.instructor ORDER BY fecha DESC"
    result = create_pandas_table(query, conn)
    print(result)
