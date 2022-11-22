from Control.validation_request import print_tables, solicitar_nombre_apellido, solicitar_password, solicitar_credenciales

"""" registro del entrenador dentro de la base de datos """


def registrar_entrenador(conn, id_admin, rol):
    data = solicitar_credenciales(conn, "entrenador", 1)  # solicitar informacion usuario

    if data is not False:
        cursor = conn.cursor()  # se conecta a la base de datos
        # realizar nuevo codigo de usuario
        selection = "SELECT nextval('entrenador_sequence')"
        cursor.execute(selection)  # ultimo id de trabajador
        id_trab = cursor.fetchone()
        id_t = id_trab[0]
        # insercion de dato
        insert_script = "INSERT INTO trabajador(id, nombres, apellidos, correo, passwordc, activo, rol) " \
                        "VALUES(%s,%s,%s,%s,%s,%s,%s)"
        insert_values = (id_t, data[0], data[1], data[2], data[3], data[4], data[5])
        cursor.execute(insert_script, insert_values)
        conn.commit()

        cursor.execute("SELECT obtener_nombre(%s,%s)" % (id_admin, rol))
        admin_name = cursor.fetchone()[0]
        querry_bitacora = "CALL bitacora_admin(%s, %s, %s, %s);"
        descripcion = "El administrador %s creo la cuenta del nuevo entrenador %s" % (
        admin_name, data[0] + '' + data[1])
        data_bitacora = (id_admin, rol, descripcion, 1)
        cursor.execute(querry_bitacora, data_bitacora)
        conn.commit()
        print("Registro realizado\nSe mostraran los entrenadores")
        mostrar_entrenadores(conn)


""" Desactiva al entrenador indicado """


def dar_baja_entrenador(conn, id_trabajador, id_admin, rol):
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM trabajador WHERE id = %s AND activo = True" % id_trabajador)
    validation = cursor.fetchone()
    if validation is not None:
        query = "UPDATE trabajador set activo = False where id = %s" % id_trabajador
        cursor.execute(query)
        conn.commit()

        # registro en bitacora
        cursor.execute("SELECT obtener_nombre(%s,%s)" % (id_admin, rol))
        admin_name = cursor.fetchone()[0]
        cursor.execute("SELECT obtener_nombre(%s,6)" % id_trabajador)
        entre_name = cursor.fetchone()[0]
        querry_bitacora = "CALL bitacora_admin(%s, %s, %s, %s);"
        descripcion = "El administrador %s modifico el estado de actividad del entrenador %s a INACTIVO" % (
        admin_name, entre_name)
        data_bitacora = (id_admin, rol, descripcion, 2)
        cursor.execute(querry_bitacora, data_bitacora)
        conn.commit()
        print("Se ha desactivado al entrenador\nA continuación puede ver el cambio")
        mostrar_entrenadores(conn)
    else:
        print("Este entrenador ya se encuentra INACTIVO")


""" Activa al entrenador indicado """


def activar_entrenador(conn, id_trabajador, id_admin, rol):
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM trabajador WHERE id = %s AND activo = False" % id_trabajador)
    validation = cursor.fetchone()
    if validation is not None:
        query = "UPDATE trabajador set activo = True where id = %s" % id_trabajador
        cursor.execute(query)
        conn.commit()

        # registro en bitacora
        cursor.execute("SELECT obtener_nombre(%s,%s)" % (id_admin, rol))
        admin_name = cursor.fetchone()[0]
        cursor.execute("SELECT obtener_nombre(%s,6)" % id_trabajador)
        entre_name = cursor.fetchone()[0]
        querry_bitacora = "CALL bitacora_admin(%s, %s, %s, %s);"
        descripcion = "El administrador %s modifico el estado de actividad del entrenador %s a ACTIVO" % (
        admin_name, entre_name)
        data_bitacora = (id_admin, rol, descripcion, 2)
        cursor.execute(querry_bitacora, data_bitacora)
        conn.commit()
        print("Se ha desactivado al entrenador\nA continuación puede ver el cambio")
        mostrar_entrenadores(conn)
    else:
        print("Este entrenador ya se encuentra ACTIVO")


""" Muestra los entrenadores que están dentro de la base de datos"""


def mostrar_entrenadores(conn):
    query = """SELECT id "ID Trabajador", nombres||' '||apellidos "Entrenador", """ \
            """activo "Estado", tipo_rol.rol "Rol" FROM trabajador """ \
            "INNER JOIN tipo_rol ON trabajador.rol = tipo_rol.cod_rol " \
            "WHERE trabajador.rol = 6 ORDER BY activo DESC;"
    print_tables(query, conn)


""" Muestra los entrenadores que están disponibles segun fecha y rango de horas"""


def mostrar_entrenadores_activos(conn, hi, hf, fecha):
    query = """SELECT trab.id "ID Trabajador", trab.nombres||' '||trab.apellidos "Entrenador" """ \
            "FROM trabajador trab " \
            "WHERE trab.id NOT IN ( " \
            "                        SELECT instructor FROM sesion_ejercicio " \
            "                        WHERE ((EXTRACT(HOUR FROM hora_inicio))" \
            "                        BETWEEN EXTRACT(HOUR FROM time'%s') AND EXTRACT(HOUR FROM time'%s')) AND " \
            "                       ((EXTRACT(HOUR FROM hora_fin)) " \
            "                       BETWEEN EXTRACT(HOUR FROM time'%s') AND EXTRACT(HOUR FROM time'%s'))" \
            "                       AND (fecha = '%s') " \
            "                      )  AND trab.activo = True AND trab.rol=6 " \
            """GROUP BY "ID Trabajador", "Entrenador";""" % (hi, hf, hi, hf, fecha)
    print_tables(query, conn)


""" Modifica el nombre o apellido del entrenador indicado """


def modificar_nombre(conn, id_entre, id_admin, rol, tipo_cambio):
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM trabajador WHERE id = %s AND rol = 6" % id_entre)  # existe el id
    validation = cursor.fetchone()

    if validation is not None:
        if tipo_cambio == 1:  # nombre
            nombre = solicitar_nombre_apellido(1)
            query = "UPDATE trabajador set nombres='%s' WHERE id = %s" % (str(nombre), id_entre)
            cursor.execute(query)
            conn.commit()

            # registro en bitacora
            cursor.execute("SELECT obtener_nombre(%s,%s)" % (id_admin, rol))
            admin_name = cursor.fetchone()[0]
            cursor.execute("SELECT obtener_nombre(%s,6)" % id_entre)
            entre_name = cursor.fetchone()[0]
            querry_bitacora = "CALL bitacora_admin(%s, %s, %s, %s);"
            descripcion = "El administrador %s modifico el nombre del entrenador %s" % (
                admin_name, entre_name)
            data_bitacora = (id_admin, rol, descripcion, 2)
            cursor.execute(querry_bitacora, data_bitacora)
            conn.commit()
            print("Se ha modificado el nombre al entrenador\nA continuación puede ver el cambio")
        elif tipo_cambio == 2:
            apellido = solicitar_nombre_apellido(2)
            query = "UPDATE trabajador set apellidos = '%s' WHERE id = %s" % (apellido, id_entre)
            cursor.execute(query)
            conn.commit()

            # registro en bitacora
            cursor.execute("SELECT obtener_nombre(%s,%s)" % (id_admin, rol))
            admin_name = cursor.fetchone()[0]
            cursor.execute("SELECT obtener_nombre(%s,6)" % id_entre)
            entre_name = cursor.fetchone()[0]
            querry_bitacora = "CALL bitacora_admin(%s, %s, %s, %s);"
            descripcion = "El administrador %s modifico el apellido del entrenador %s" % (
                admin_name, entre_name)
            data_bitacora = (id_admin, rol, descripcion, 2)
            cursor.execute(querry_bitacora, data_bitacora)
            conn.commit()
            print("Se ha modificado el apellido al entrenador\nA continuación puede ver el cambio")
        elif tipo_cambio == 3:
            nombre, apellido = solicitar_nombre_apellido(3)
            query = "UPDATE trabajador set nombres= %s, apellidos = %s WHERE id = %s"
            cursor.execute(query, (nombre, apellido, id_entre))
            conn.commit()

            # registro en bitacora
            cursor.execute("SELECT obtener_nombre(%s,%s)" % (id_admin, rol))
            admin_name = cursor.fetchone()[0]
            cursor.execute("SELECT obtener_nombre(%s,6)" % id_entre)
            entre_name = cursor.fetchone()[0]
            querry_bitacora = "CALL bitacora_admin(%s, %s, %s, %s);"
            descripcion = "El administrador %s modifico el nombre y apellido del entrenador %s" % (
                admin_name, entre_name)
            data_bitacora = (id_admin, rol, descripcion, 2)
            cursor.execute(querry_bitacora, data_bitacora)
            conn.commit()
            print("Se ha modificado el nombre y apellido al entrenador\nA continuación puede ver el cambio")
        mostrar_entrenadores(conn)
    else:
        print("Este id indicado no es valido")


""" Modifica la password del entrenador indicado """


def modificar_password_entre(conn, id_entre, id_admin, rol):
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM trabajador WHERE id = %s AND rol = 6" % id_entre)  # existe el id
    validation = cursor.fetchone()

    if validation is not None:
        password = solicitar_password()
        query = "UPDATE trabajador set passwordc = %s WHERE id = %s"
        cursor.execute(query, (password, id_entre))
        conn.commit()

        # registro en bitacora
        cursor.execute("SELECT obtener_nombre(%s,%s)" % (id_admin, rol))
        admin_name = cursor.fetchone()[0]
        cursor.execute("SELECT obtener_nombre(%s,6)" % id_entre)
        entre_name = cursor.fetchone()[0]
        querry_bitacora = "CALL bitacora_admin(%s, %s, %s, %s);"
        descripcion = "El administrador %s modifico la contraseña del entrenador %s" % (admin_name, entre_name)
        data_bitacora = (id_admin, rol, descripcion, 2)
        cursor.execute(querry_bitacora, data_bitacora)
        conn.commit()
        print("Se ha modificado la contraseña del entrenador\nA continuación puede ver el cambio")

        mostrar_entrenadores(conn)
    else:
        print("Este id indicado no es valido")
