import pandas as pd

""" solicitar datos para registrar un nuevo entrenador """
def solicitar_credenciales(conn):
    try:
        print("\tA continuación se te solicitará información básica para crear el perfil del entrenador")
        print("\tSI ALGUNO DE LOS DATOS ES INCORRECTO SE TE NOTIFICARÁ")
        bandier = True
        nombres = str(input("¿Cuáles son sus nombres?"))
        apellidos = str(input("¿Cuáles son sus apellidos?"))
        correo = str(input("¿Cuál es su correo?"))

        bandier = True
        while bandier is True:  # conocer que el correo no esta registrado
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM trabajador WHERE correo='%s'" % correo)
            result = cursor.fetchone()
            if result != 'None':
                bandier = False
            else:
                correo = str((input("Este correo ya está registrado, intenta con otro")))

        password = str(input("¿Cuál es tu contraseña?"))
        password2 = str(input("Confirma tu contraseña"))

        bandier = True
        while bandier is True:
            if password == password2:
                bandier = False
            else:
                print("\tLas contraseñas no coinciden, te las vamos a solicitar nuevamente")
                password = str(input("¿Cuál es tu contraseña?"))
                password2 = str(input("Confirma tu contraseña"))
        return nombres, apellidos, correo, password, True, 6
    except ValueError:
        print("Los datos ingresados no son válidos, tendrá que regresar a esta parte del menú")
        return False


"""" registro del entrenador dentro de la base de datos """
def registrar_entrenador(conn, id_admin, rol):
    data = solicitar_credenciales(conn)  # solicitar informacion usuario

    if data is not False:
        cursor = conn.cursor()     # se conecta a la base de datos

        # realizar nuevo codigo de usuario
        selection = "SELECT nextval('entrenador_sequence')"
        cursor.execute(selection)  # ultimo id de trabajador
        id_trab = cursor.fetchone()
        id_t = id_trab[0]
        # insercion de dato
        insert_script = "INSERT INTO trabajador(id, nombres, apellidos, correo, passwordc, activo, rol) "\
                        "VALUES(%s,%s,%s,%s,%s,%s,%s)"
        insert_values = (id_t, data[0], data[1], data[2], data[3], data[4], data[5])
        cursor.execute(insert_script, insert_values)
        conn.commit()

        cursor.execute("SELECT obtener_nombre(%s,%s)" % (id_admin, rol))
        admin_name = cursor.fetchone()[0]
        querry_bitacora = "CALL bitacora_admin(%s, %s, %s, %s);"
        descripcion = "El administrador %s creo la cuenta del nuevo entrenador %s" % (admin_name, data[0]+' '+data[1])
        data_bitacora = (id_admin, rol, descripcion, 1)
        cursor.execute(querry_bitacora, data_bitacora)
        conn.commit()
        print("Registro realizado\nSe mostraran los entrenadores")
        mostrar_entrenadores(conn)


""" Desactiva al entrenador indicado """
def dar_baja_entrenador(conn, id_trabajador, id_admin, rol):
    cursor = conn.cursor()
    query = "UPDATE trabajador set activo = False where id = %s" % id_trabajador
    cursor.execute(query)
    conn.commit()

    # registro en bitacora
    cursor.execute("SELECT obtener_nombre(%s,%s)" % (id_admin, rol))
    admin_name = cursor.fetchone()[0]
    cursor.execute("SELECT obtener_nombre(%s,6)" % id_trabajador)
    entre_name = cursor.fetchone()[0]
    querry_bitacora = "CALL bitacora_admin(%s, %s, %s, %s);"
    descripcion = "El administrador %s modifico el estado de actividad del entrenador %s" % (admin_name, entre_name)
    data_bitacora = (id_admin, rol, descripcion, 2)
    cursor.execute(querry_bitacora, data_bitacora)
    conn.commit()
    print("Se ha desactivado al entrenador\nA continuación puede ver el cambio")
    mostrar_entrenadores(conn)


""" Muestra los entrenadores que están dentro de la base de datos"""
def mostrar_entrenadores(conn):
    query = "SELECT  id, nombres, apellidos, activo, tipo_rol.rol FROM trabajador " \
            "INNER JOIN tipo_rol ON trabajador.rol = tipo_rol.cod_rol " \
            "WHERE trabajador.rol = 6 ORDER BY activo DESC;"
    result = pd.read_sql(query, conn)
    print(result)


""" Muestra los entrenadores que están disponibles segun fecha y rango de horas"""
def mostrar_entrenadores_activos(conn,hi, hf, fecha):
    query = "SELECT trab.id, trab.nombres, trab.apellidos "\
            "FROM trabajador trab "\
            "WHERE trab.id NOT IN ( "\
            "                        SELECT instructor FROM sesion_ejercicio "\
            "                        WHERE ((EXTRACT(HOUR FROM hora_inicio))"\
            "                        BETWEEN EXTRACT(HOUR FROM time'%s') AND EXTRACT(HOUR FROM time'%s')) AND "\
            "                       ((EXTRACT(HOUR FROM hora_fin)) "\
            "                       BETWEEN EXTRACT(HOUR FROM time'%s') AND EXTRACT(HOUR FROM time'%s'))"\
            "                       AND (fecha = '%s') "\
            "                      )  AND trab.activo = True AND trab.rol=6 "\
            "GROUP BY trab.id, trab.nombres, trab.apellidos;" % (hi, hf, hi, hf, fecha)
    result = pd.read_sql(query, conn)
    print(result)
