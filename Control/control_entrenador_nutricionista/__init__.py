from Control.validation_request import create_pandas_table
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
        correo = str(input("¿Cuál es tu correo?"))
        while bandier:  # conocer que el correo no esta registrado
            cursor = conn.cursor()
            result = cursor.execute("SELECT 1 FROM trabajador WHERE correo='%s'" % correo)

            if str(result) != 'None':
                bandier = False
            else:
                correo = str((input("Este correo ya está registrado, intenta con otro")))

        password = str(input("¿Cuál es tu contraseña?"))
        password2 = str(input("Confirma tu contraseña"))

        bandier = True
        while bandier:
            if password == password2:
                bandier = False
            else:
                print("\tLas contraseñas no coinciden, te las vamos a solicitar nuevamente")
                password = str(input("¿Cuál es tu contraseña?"))
                password2 = str(input("Confirma tu contraseña"))

        return nombres, apellidos, correo, password, True, 'IDR_EP'
    except ValueError:
        print("Los datos ingresados no son válidos, tendrá que regresar a esta parte del menú")
        return False


"""" registro del entrenador dentro de la base de datos """
def registrar_entrenador(conn):
    data = solicitar_credenciales(conn)  # solicitar informacion usuario

    if data is not False:
        cursor = conn.cursor()     # se conecta a la base de datos
        # realizar nuevo codigo de usuario
        cursor.execute("SELECT id FROM trabajador ORDER BY id DESC LIMIT 1;")  # ultimo trabajador registrado
        id_trab = cursor.fetchone()
        id_trab = id_trab[0]  # de la tupla se recupera el primer valor
        last_id = id_trab[0][4:]  # se recupera los ultimos digitos del id
        new_id = int(last_id)+1    # se aumenta en uno el valor del ultimo id
        id = id_trab[0].replace(str(last_id), str(new_id))  # el id correspondiente es este
        # insercion de dato
        insert_script = "INSERT INTO trabajador(id, nombres, apellidos, correo, passwordc, activo, rol) "\
                        "VALUES(%s,%s,%s,%s,%s,%s,%s)"
        insert_values = (id, data[0], data[1], data[2], data[3], data[4], data[5])
        cursor.execute(insert_script, insert_values)
        conn.commit()
        print("Registro realizado\nSe mostraran los entrenadores")
        mostrar_entrenadores()


""" Desactiva al entrenador indicado """
def dar_baja_entrenador(conn, id_trabajador):
    cursor = conn.cursor()
    query = "UPDATE trabajador set activo = False where id = '%s'"
    cursor.execute(query, id_trabajador)
    conn.commit()
    print("Se ha desactivado al entrenador\nA continuación puede ver el cambio")
    mostrar_entrenadores()


""" Muestra los entrenadores que están dentro de la base de datos"""
def mostrar_entrenadores(conn):
    query = "SELECT  id, nombres, apellidos, activo, tipo_rol.rol FROM trabajador " \
            "INNER JOIN tipo_rol ON trabajador.rol = tipo_rol.cod_rol " \
            "WHERE trabajador.rol = 'IDR_EP' ORDER BY  activo DESC;"

    from Control.validation_request import create_pandas_table
    result = create_pandas_table(query, conn)
    print(result)


""" Muestra los entrenadores que están disponibles segun fecha y rango de horas"""
def mostrar_entrenadores_activos(conn,hi, hf, fecha):
    query = "SELECT trab.id, trab.nombres, trab.apellidos "\
            "FROM trabajador trab INNER JOIN sesion_ejercicio se on trab.id = se.instructor "\
            "WHERE trab.id NOT IN ( "\
            "                        SELECT instructor FROM sesion_ejercicio "\
            "                        WHERE ((EXTRACT(HOUR FROM hora_inicio))"\
            "                        BETWEEN EXTRACT(HOUR FROM time'%s') AND EXTRACT(HOUR FROM time'%s')) AND "\
            "                       ((EXTRACT(HOUR FROM hora_fin)) "\
            "                       BETWEEN EXTRACT(HOUR FROM time'%s') AND EXTRACT(HOUR FROM time'%s'))"\
            "                       AND (fecha = '%s') "\
            "                      )  AND trab.activo = True "\
            "GROUP BY trab.id, trab.nombres, trab.apellidos;" %(hi, hf, hi, hf, fecha)

    result = create_pandas_table(query, conn)
    print(result)
