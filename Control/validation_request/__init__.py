import psycopg2
from calendar import monthrange
from datetime import date
from prettytable import PrettyTable
from config import config

"""               REQUEST                      """
""" CONECTAR A BASE DE DATOS"""


def connect_db(opcion=7):
    # conexion a la base de datos
    try:
        # leer los paramatros del database.ini
        if opcion == 1:
            params = config('database.ini', 'postgresql')
        elif opcion == 2:
            params = config('database_admin_u.ini', 'postgresql')
        elif opcion == 3:
            params = config('database_admin_sesion.ini', 'postgresql')
        elif opcion == 4:
            params = config('database_admin_reporteria.ini', 'postgresql')
        elif opcion == 5:  # usuario
            params = config('database_u.ini', 'postgresql')
        else:
            params = config('database.ini', 'postgresql')
        conn = psycopg2.connect(**params)
        print("Sesion a la base de datos ha sido exitosa")
        return conn
    except psycopg2.OperationalError:
        print("Alguna credencial no ha sido ingresada correctamente")


""" solicitar datos de inicio de sesion"""


def credencial_login(pregunta):
    bandier = True
    while bandier:
        username = str(input("\t\t %s" % pregunta))
        passw = str(input("\t\t¿Cuál es tu contraseña?: "))

        if len(username) > 0 and len(passw) > 0:
            bandier = False
            return username, passw


""" recupera el id trabajador que se ha iniciado dentro de la base"""


def recuperar_id_trabajador(conn, correo, passw):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM trabajador WHERE correo='%s' AND passwordc='%s'" % (correo, passw))
    return str(cursor.fetchone())


""" solicita la fecha en un formato correcto """


def solicitar_datos_fecha(argumento, anio_limite):
    bandier = False
    anio = ""
    mes = ""
    dia = ""
    dat = ""
    while bandier is False:
        dat = input("Ingrese el año '%s' " % argumento)
        try:
            anio = int(dat)
        except ValueError:
            print("El dato ingresado no es numerico")

        if 1950 <= anio <= anio_limite:
            bandier = True
        else:
            print("El año '%s', debe de estar entre 1950 a 2022 " % argumento)

    bandier = False
    while bandier is False:
        dat = input("Ingrese el mes '%s' " % argumento)
        try:
            mes = int(dat)
        except ValueError:
            print("El dato ingresado no es numerico")

        if 1 <= mes <= 12:
            bandier = True
        else:
            print("El mes '%s', debe de estar entre 1 a 12 " % argumento)

    bandier = False
    while bandier is False:
        dat = input("Ingrese el dia '%s' " % argumento)
        try:
            dia = int(dat)
        except ValueError:
            print("El dato ingresado no es numerico")
        dias_aceptados = monthrange(anio, mes)[1]
        if 1 <= dia <= dias_aceptados:
            bandier = True
        else:
            print("El dia '%s', el mes '%s' tiene rango de dias entre 1 a '%s' " % (argumento, mes, dias_aceptados))
    return date(anio, mes, dia)


def solicitar_hora(argumento):
    bandier = False
    hora_i = 0
    min_i = 0
    hora_f = 0
    min_f = 0
    while bandier is False:
        dat = input("Ingrese la hora de inicio '%s' en formato de 24 horas" % argumento)
        try:
            hora_i = int(dat)
        except ValueError:
            print("El dato ingresado no es numerico")

        if 0 <= hora_i <= 23:
            bandier = True
        else:
            print("La hora '%s', debe de estar entre 0 y 23 " % argumento)

    bandier = False
    while bandier is False:
        dat = input("Ingrese los minutos '%s' " % argumento)
        min_i = 0
        try:
            min_i = int(dat)
        except ValueError:
            print("El dato ingresado no es numerico")

        if 0 <= min_i <= 59:
            bandier = True
        else:
            print("Los minutos '%s', debe de estar entre 0 a 59 " % argumento)

    bandier = False
    while bandier is False:
        dat = input("Ingrese la hora de finalización '%s' en formato de 24 horas" % argumento)
        try:
            hora_f = int(dat)
        except ValueError:
            print("El dato ingresado no es numerico")

        if 0 <= hora_i <= hora_f <= 23:
            bandier = True
        else:
            print(
                "La hora '%s', debe de estar entre 0 y 23 y debe ser mayor que su hora de inicio" % argumento)

    bandier = False
    while bandier is False:
        dat = input("Ingrese los minutos '%s' de la hora de finalizacion" % argumento)
        try:
            min_f = int(dat)
        except ValueError:
            print("El dato ingresado no es numerico")

        if 0 <= min_f <= 59:
            bandier = True
        else:
            print("Los minutos '%s', debe de estar entre 0 a 59 " % argumento)

    hora_i_minutos = (hora_i * 60) + min_i
    hora_f_minutos = (hora_f * 60) + min_f
    total_tiempo = hora_f_minutos - hora_i_minutos
    if (hora_f_minutos >= hora_i_minutos) and 30 <= total_tiempo <= 60:
        return ("%s:%s" % (hora_i, min_i)), ("%s:%s" % (hora_f, min_f)), total_tiempo
    else:
        print("Los datos ingresados no cumplen con que la sesion sea de 30min a 1 hora")
        return False


def solicitar_hora_busqueda(argumento):
    bandier = False
    hora_i = 0
    min_i = 0
    hora_f = 0
    min_f = 0
    while bandier is False:
        dat = input("Ingrese la hora de inicio '%s' en formato de 24 horas" % argumento)
        try:
            hora_i = int(dat)
        except ValueError:
            print("El dato ingresado no es numerico")

        if 0 <= hora_i <= 23:
            bandier = True
        else:
            print("La hora '%s', debe de estar entre 0 y 23 " % argumento)

    bandier = False
    while bandier is False:
        dat = input("Ingrese los minutos '%s' " % argumento)
        min_i = 0
        try:
            min_i = int(dat)
        except ValueError:
            print("El dato ingresado no es numerico")

        if 0 <= min_i <= 59:
            bandier = True
        else:
            print("Los minutos '%s', debe de estar entre 0 a 59 " % argumento)

    bandier = False
    while bandier is False:
        dat = input("Ingrese la hora de finalización '%s' en formato de 24 horas" % argumento)
        try:
            hora_f = int(dat)
        except ValueError:
            print("El dato ingresado no es numerico")

        if 0 <= hora_i <= hora_f <= 23:
            bandier = True
        else:
            print(
                "La hora '%s', debe de estar entre 0 y 23 y debe ser mayor que su hora de inicio" % argumento)

    bandier = False
    while bandier is False:
        dat = input("Ingrese los minutos '%s' de la hora de finalizacion" % argumento)
        try:
            min_f = int(dat)
        except ValueError:
            print("El dato ingresado no es numerico")

        if 0 <= min_f <= 59:
            bandier = True
        else:
            print("Los minutos '%s', debe de estar entre 0 a 59 " % argumento)

    hora_i_minutos = (hora_i * 60) + min_i
    hora_f_minutos = (hora_f * 60) + min_f
    total_tiempo = hora_f_minutos - hora_i_minutos
    if (hora_f_minutos >= hora_i_minutos):
        return ("%s:%s" % (hora_i, min_i)), ("%s:%s" % (hora_f, min_f)), total_tiempo
    else:
        print("Los datos ingresados no cumplen con que la hora de fin sea mayor a la hora de inicio")
        return False


def solicitar_duracion():
    bandier = False
    min_f = 0.0
    while bandier is False:
        dat = input("Ingrese el tiempo en minutos de la sesion")
        try:
            min_f = float(dat)
        except ValueError:
            print("El dato ingresado no es numerico")

        if 30.00 <= min_f <= 60.00:
            bandier = True
        else:
            print("La duracion debe de estar entre 30 a 60 min")
    return min_f


def solicitar_categoria(conn):
    bandier = False
    cursor = conn.cursor()
    cursor.execute("""SELECT id_categoria FROM categoria_ejercicio ORDER BY id_categoria ASC LIMIT 1;""")
    menor_valor = cursor.fetchone()[0]
    cursor.execute("""SELECT id_categoria FROM categoria_ejercicio ORDER BY id_categoria DESC LIMIT 1;""")
    mayor_valor = cursor.fetchone()[0]
    query = """SELECT id_categoria "ID", ejercicio "Ejercicio" FROM categoria_ejercicio ORDER BY id_categoria ASC;"""
    cat = 0
    while bandier is False:
        print_tables(query, conn)
        dat = input("Ingrese la categoria que desea consultar")
        try:
            cat = int(dat)
        except ValueError:
            print("El dato ingresado no es numerico")
        if menor_valor <= cat <= mayor_valor:
            bandier = True
        else:
            print("El id ingresado no pertenece a alguna categoria")
    return cat


def solicitar_entrenador(conn):
    bandier = False
    cursor = conn.cursor()
    cursor.execute("""SELECT id FROM trabajador WHERE rol=6 AND activo=TRUE ORDER BY id ASC LIMIT 1;""")
    menor_valor = cursor.fetchone()[0]
    cursor.execute("""SELECT id FROM trabajador WHERE rol=6 AND activo=TRUE ORDER BY id DESC LIMIT 1;""")
    mayor_valor = cursor.fetchone()[0]
    query = """SELECT id "ID", nombres||' '||apellidos "Nombre del entrenador" FROM trabajador WHERE rol=6 AND activo=TRUE ORDER BY id ASC;"""
    ent = 0
    while bandier is False:
        print_tables(query, conn)
        dat = input("Ingrese el id del entrenador que desea consultar")
        try:
            ent = int(dat)
        except ValueError:
            print("El dato ingresado no es numerico")
        if menor_valor <= ent <= mayor_valor:
            bandier = True
        else:
            print("El id ingresado no pertenece a ni un entrenador")
    return ent


def solicitar_hora_sincronizacion(hi, hf):
    bandier = False
    hora_i = 0
    min_i = 0
    hora_f = 0
    min_f = 0
    hi = str(hi)
    hf = str(hf)
    while bandier is False:
        dat = input("Ingrese la hora de en que ingreso a la sesion en formato de 24 horas")
        try:
            hora_i = int(dat)
        except ValueError:
            print("El dato ingresado no es numerico")
        hora = '%s:%s:00' % (hora_i, hi[3:5])
        if (0 <= hora_i <= 23) and (hi <= hora <= hf):
            bandier = True
        else:
            print("La hora debe de estar entre %s y %s " % (hi, hf))

    bandier = False
    while bandier is False:
        dat = input("Ingrese los minutos a los ingreso ")
        min_i = 0
        try:
            min_i = int(dat)
        except ValueError:
            print("El dato ingresado no es numerico")
        hora = '%s:%s:00' % (hora_i, min_i)
        if (0 <= min_i <= 59) and (hi <= hora <= hf):
            bandier = True
        else:
            print("La hora debe de estar entre %s y %s " % (hi, hf))

    bandier = False
    while bandier is False:
        dat = input("Ingrese la hora a la que se retiro de la sesion en formato de 24 horas")
        try:
            hora_f = int(dat)
        except ValueError:
            print("El dato ingresado no es numerico")
        hora = '%s:%s:00' % (hora_f, hi[3:5])
        if (0 <= hora_i <= hora_f <= 23) and (hi <= hora <= hf):
            bandier = True
        else:
            print(
                "La hora a la que se retiro debe de estar entre %s y %s y debe ser mayor que su hora de inicio" % (
                    hi, hf))

    bandier = False
    while bandier is False:
        dat = input("Ingrese los minutos de cuando salio de la sesion")
        try:
            min_f = int(dat)
        except ValueError:
            print("El dato ingresado no es numerico")
        hora = '%s:%s:00' % (hora_f, min_f)
        if (0 <= min_f <= 59) and (hi <= hora <= hf):
            bandier = True
        else:
            print("La hora debe de estar entre %s y %s " % (hi, hf))

    hora_i_minutos = (hora_i * 60) + min_i
    hora_f_minutos = (hora_f * 60) + min_f
    total_tiempo = hora_f_minutos - hora_i_minutos
    if hora_f_minutos >= hora_i_minutos:
        return ("%s:%s" % (hora_i, min_i)), ("%s:%s" % (hora_f, min_f))
    else:
        print("Los datos ingresados no cumplen con que la hora de fin sea mayor a la hora de inicio")
        return False


def solicitar_ritmo_cardiaco_calorias():
    bandier = False
    pul = 0
    cal = 0
    while bandier is False:
        dat = input(
            "Ingrese su frencuencia cardiaca despues de ejercitarse\nDebe de estar en un rango de 80 y 160 pulsaciones por minuto")
        dat2 = input("Ingrese las calorias quemadas")
        try:
            pul = float(dat)
            cal = float(dat2)
        except ValueError:
            print("El dato ingresado no es numerico")
        if (80 <= pul <= 160) and (0 < cal):
            bandier = True
        else:
            print(
                "Las pulsaciones por minutos deben de estar entre 80 y 160\nSus calorias quemadas deben de ser superior a 0")
    return pul, cal



def solicitar_hora_sesion_simulacion(argumento, anio_limite):
    bandier = False
    anio = ""
    mes = ""
    dat = ""
    while bandier is False:
        dat = input("Ingrese el año '%s' " % argumento)
        try:
            anio = int(dat)
        except ValueError:
            print("El dato ingresado no es numerico")

        if 1950 <= anio <= anio_limite:
            bandier = True
        else:
            print("El año '%s', debe de estar entre 1950 a 2022 " % argumento)

    bandier = False
    while bandier is False:
        dat = input("Ingrese el mes '%s' " % argumento)
        try:
            mes = int(dat)
        except ValueError:
            print("El dato ingresado no es numerico")

        if 1 <= mes <= 12:
            bandier = True
        else:
            print("El mes '%s', debe de estar entre 1 a 12 " % argumento)
            
    return date(anio, mes)




def solicitar_nombre_apellido(option):
    bandier = False
    nombres = ""
    apellidos = ""
    if option == 1:  # cambiar nombre
        while bandier is False:
            nombres = str(input("¿Cuáles son sus nombres?"))
            if nombres.isspace() is False:
                bandier = True
        return nombres
    elif option == 2:  # cambiar apellido
        while bandier is False:
            apellidos = str(input("¿Cuáles son sus apellidos?"))
            if apellidos.isspace() is False:
                bandier = True
        return apellidos
    elif option == 3:  # cambiar nombre y apellido
        while bandier is False:
            nombres = str(input("¿Cuáles son sus nombres?"))
            if nombres.isspace() is False:
                bandier = True
        bandier = False
        while bandier is False:
            apellidos = str(input("¿Cuáles son sus apellidos?"))
            if apellidos.isspace() is False:
                bandier = True
        return nombres, apellidos


def solicitar_password():
    password = ""
    password2 = ""
    bandier = True
    while bandier is True:
        password = str(input("¿Cuál es la contraseña?"))
        password2 = str(input("Confirma la contraseña"))
        if (password == password2) and (password.isspace() is False) and (password2.isspace() is False):
            bandier = False
        else:
            print("\tLas contraseñas no coinciden, te las vamos a solicitar nuevamente")
    return password


def print_tables(query, conn):
    cursor = conn.cursor()
    cursor.execute(query)  # ejecuta el query indicado
    data = cursor.fetchall()
    if len(data) != 0:
        colnames = [desc[0] for desc in cursor.description]  # el nombre de las columnas
        t = PrettyTable(colnames)  # las columnas en la tabla
        for info in data:
            t.add_row(info)  # las filas en la tabla
        print(t)
    else:
        print("No hay registros sobre el dato que deseas ver")


""" solicitar datos para registrar un nuevo trabajador """


def solicitar_credenciales(conn, argumento, tipo_trabajador):
    try:
        print("\tA continuación se te solicitará información básica para crear el perfil del %s" % argumento)
        print("\tSI ALGUNO DE LOS DATOS ES INCORRECTO SE TE NOTIFICARÁ")
        bandier = True
        nombres, apellidos = solicitar_nombre_apellido(3)
        correo = str(input("¿Cuál es su correo?"))

        while bandier is True:  # conocer que el correo no esta registrado
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM trabajador WHERE correo='%s'" % correo)
            result = cursor.fetchone()
            if result is None:
                bandier = False
            else:
                correo = str((input("Este correo ya está registrado, intenta con otro")))

        password = solicitar_password()
        if tipo_trabajador == 1:  # es un entrenador
            return nombres, apellidos, correo, password, True, 6
        if tipo_trabajador == 2:  # es un administrador, se debe de mostrar los roles disponibles
            query = """SELECT cod_rol "ID", tipo_rol "Tipo de rol" FROM tipo_rol WHERE cod_rol BETWEEN 2 and 4 ORDER BY cod_rol ASC;"""
            tipo_admin = 0
            while bandier is False:
                print_tables(query, conn)
                dat = input("Ingrese el id del tipo de administrador que desea agregar")
                try:
                    tipo_admin = int(dat)
                except ValueError:
                    print("El dato ingresado no es numerico")
                if 2 <= tipo_admin <= 4:
                    bandier = True
                else:
                    print("El id ingresado no pertenece a ni un entrenador")
            return nombres, apellidos, correo, password, True, tipo_admin
    except ValueError:
        print("Los datos ingresados no son válidos, tendrá que regresar a esta parte del menú")
        return False


def solicitar_admins(conn, argumento):
    bandier = False
    cursor = conn.cursor()
    cursor.execute("""SELECT id FROM trabajador WHERE rol BETWEEN 2 AND 4 ORDER BY id ASC LIMIT 1;""")
    menor_valor = cursor.fetchone()[0]
    cursor.execute("""SELECT id FROM trabajador WHERE rol BETWEEN 2 AND 4 ORDER BY id DESC LIMIT 1;""")
    mayor_valor = cursor.fetchone()[0]

    ent = 0
    while bandier is False:
        dat = input("Ingrese el id del administrador que desea %s" % argumento)
        try:
            ent = int(dat)
        except ValueError:
            print("El dato ingresado no es numerico")
        if menor_valor <= ent <= mayor_valor:
            bandier = True
        else:
            print("El id ingresado no pertenece a ni un administrador valido")
    return ent




