from datetime import date
from Control.validation_request import solicitar_datos_fecha, create_pandas_table, connect_db

""" solicitar datos para registrar un nuevo usuario """
def solicitar_credenciales(conn):
    try:
        print("\tA continuación se te solicitará información básica para crear tu perfil")
        print("\tSI ALGUNO DE TUS DATOS ES INCORRECTO SE TE NOTIFICARÁ")
        bandier = True
        nombres = str(input("¿Cuáles son tus nombres?"))
        apellidos = str(input("¿Cuáles son tus apellidos?"))
        nickname = str(input("¿Cuál es tu username?"))

        while bandier is True:  # conocer que el nickname no esta tomado
            cursor = conn.cursor()
            query = "SELECT 1 FROM usuario WHERE nickname='{nick}'"
            val = {"nick": nickname}
            cursor.execute(query, val)
            result = cursor.fetchone()
            if result != 'None':
                bandier = False
            else:
                nickname = str((input("Este nombre de usuario ya esta tomado, intenta con otro")))
        bandier = True
        correo = str(input("¿Cuál es tu correo?"))
        while bandier is True:  # conocer que el correo no esta registrado
            cursor = conn.cursor()
            query = "SELECT 1 FROM usuario WHERE correo='{correo}'"
            values = {"correo": correo}
            cursor.execute(query, values)
            result = cursor.fetchone()
            if result != 'None':
                bandier = False
            else:
                correo = str((input("Este correo ya está registrado, intenta con otro ")))

        password = str(input("¿Cuál es tu contraseña? "))
        password2 = str(input("Confirma tu contraseña "))

        bandier = True
        while bandier is True:
            if password == password2:
                bandier = False
            else:
                print("\tLas contraseñas no coinciden, te las vamos a solicitar nuevamente")
                password = str(input("¿Cuál es tu contraseña? "))
                password2 = str(input("Confirma tu contraseña "))

        edad = int(input("¿Cuál es tu edad? "))
        altura = float(input("¿Cuál es tu altura? "))
        peso = float(input("¿Cuál es tu peso actual? "))
        calorias = float(input("¿Cuáles son tus calorías actuales? "))

        return nombres, apellidos, nickname, edad, altura, calorias, peso, correo, password
    except ValueError:
        print("Los datos ingresados no son válidos, tendrá que regresar a esta parte del menú")
        return False


"""" registro del usuario dentro de la base de datos, retorna el id del usuario registrado """
def registrar_usuario(conn):
    data = solicitar_credenciales(conn)  # solicitar informacion usuario

    if data is not False:
        cursor = conn.cursor()  # se conecta a la base de datos
        # realizar nuevo codigo de usuario
        selection = "SELECT 'IDU_'||(nextval('usuario_sequence')::VARCHAR)"
        cursor.execute(selection)  # ultimo usuario
        id_sesion = cursor.fetchone()
        id_u = id_sesion[0]
        # insercion de dato
        insert_script = "INSERT INTO usuario(id_usuario, nombres, apellidos, nickname, edad, altura, caloria_actual,peso_actual, correo, passwordc)" \
                        "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        insert_values = (id_u, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8])
        cursor.execute(insert_script, insert_values)
        conn.commit()
        print("Registro realizado")

        return id_u  # el usuario queda "iniciada" su sesion



def iniciar_sesion_usuario(conn, usern, passw):
    cursor = conn.cursor()
    query = "SELECT usuario.id_usuario, us.id_suscripcion, ((us.fecha_inicio+'1 year'::INTERVAL) - current_date)::VARCHAR " \
            "FROM   usuario INNER JOIN usuario_suscripcion us ON usuario.id_usuario = us.id_usuario " \
            "WHERE nickname=%s AND passwordc=%s AND us.activo=True " \
            "AND now()<=fecha_inicio+'1 year'::INTERVAL " \
            "ORDER BY us.fecha_inicio DESC LIMIT 1;"
    data = (usern, passw)
    cursor.execute(query, data)
    user_data = cursor.fetchone()
    if user_data is not None:
        return user_data
    else:
        return False

"""" solicitar datos relacionados al registro de peso y calorias del usuario"""


def peso():
    try:
        peso = float((input("¿Cuál es tu peso? ")))
        calorias = float((input("¿Cuál son sus calorias? ")))
        fecha = date.today()  # por default se ingresa el peso del dia del dispositivo
        return peso, calorias, str(fecha)
    except ValueError:
        print("En peso y calorias ingrese datos numericos")
        return False


"""" registrar el peso y calorias del usuario """


def registrar_peso(conn, id):
    data = peso()
    if data is not False:
        cursor = conn.cursor()
        insert_script = "INSERT INTO usuario_registro_historico(id_usuario, peso, caloria, fecha) "\
                        "VALUES(%s, %s, %s, %s)"
        values = (id, data[0], data[1], data[2])
        cursor.execute(insert_script, values)
        conn.commit()
        print("Se ha registrado tu peso y calorías actuales")

        query ="SELECT id_usuario, peso, caloria, fecha FROM usuario_registro_historico WHERE id_usuario='%s'"\
               "ORDER BY fecha " %id
        result = create_pandas_table(query, conn)
        print(result)


""" verifica que el metodo de pago no este ya dentro de la base de datos 
    retorna True cuando el dato no se encuentra y False cuando ya se encuentra """

def validar_metodo_pago(conn, cod_tarjeta):
    cursor = conn.cursor()
    select_script = """SELECT 1 FROM metodo_pago WHERE cod_tarjeta='%s' """ % str(cod_tarjeta)
    cursor.execute(select_script)
    value = cursor.fetchone()

    if value is None:  # no hay tarjetas con este codigo
        return False
    else:
        return True


"""" solicita los datos para el metodo de pago """


def credencial_metodo_pago(conn):
    try:
        cod_tarjeta = str(input("Ingrese el codigo de su tarjeta"))
        value = validar_metodo_pago(conn, cod_tarjeta)
        if value is not True:
            nombre = str(input("Ingrese el nombre que aparece en su tarjeta"))
            fecha = solicitar_datos_fecha(" de vencimiento de su tarjeta", 2030)
            cvv = int(input("Ingrese el CVV de su tarjeta"))
            tarjeta = int(input("¿Cuál es el tipo de esta tarjeta?\n[1]Crédito\n[2]Débito "))
            tipo_tarjeta = ""
            if tarjeta == 1:
                tipo_tarjeta = "IDTT_C"
            elif tarjeta == 2:
                tipo_tarjeta = "IDTT_D"

            return cod_tarjeta, nombre, fecha, cvv, tipo_tarjeta
        else:
            print(
                "Este codigo de tarjeta ya existe, dirigite a la seccion de seleccionar tipo de suscripcion y realiza tu pago de mensualidad")
            return False
    except ValueError:
        print("El tipo de dato no coincide con lo ingresado\n\tIntentelo de nuevo")
        return False


"""" se registra el metodo de pago dentro de la base de datos"""


def registro_metodo_pago(conn):
    data = credencial_metodo_pago(conn)
    cod_tarjeta = 0
    if data is not False:
        cursor = conn.cursor()
        insert_script = "INSERT INTO metodo_pago(cod_tarjeta, nombre_tarjeta, fecha_caducidad, cvv, tipo_tarjeta) " \
                        "VALUES(%s, %s, %s, %s, %s)"
        insert_values = (data[0], data[1], data[2], data[3], data[4])
        cursor.execute(insert_script, insert_values)
        conn.commit()
        print("Se ha registrado este metodo de pago")


""" muestra los planes disponibles para el usuario. 
    retorna el id del tipo de plan que el usuario desea suscribirse 
"""


def presentar_tipos_planes(conn):
    print("\tEstos son los planes que te ofrecemos ")
    query = "SELECT tipo, precio FROM suscripcion;"
    planes_info = create_pandas_table(query, conn)
    print(planes_info)
    print("En diamante tendrás un IHealthWatch+ de regalo y una sesión mensual con nutricionista")
    print("En oro tendrás un IHealthWatch+ de alquiler")

    try:
        plan = int(input("\t\t¿Cuál plan te gustaría obtener?\n\t\t[1]Diamante\n\t\t[2]Oro"))
        if plan == 1:
            return 'IDS_D'
        elif plan == 2:
            return 'IDS_O'
        else:
            print("Se le asignara el plan oro")
            return 'IDS_O'
    except ValueError:
        print("Su respuesta no es valida")


""" registrar suscripcion """


def registrar_suscripcion(conn, id, tipo):
    print("Tu fecha de inicio de esta plan se registrara como el día actual en tu dispositivo")
    cursor = conn.cursor()
    plan_anterior = "UPDATE usuario_suscripcion SET activo = FALSE " \
                    "WHERE id_usuario=%s AND fecha_inicio =" \
                    "(SELECT  fecha_inicio FROM usuario_suscripcion " \
                    "WHERE   id_usuario=%s ORDER BY fecha_inicio DESC LIMIT 1)"
    variable = (id, id)
    cursor.execute(plan_anterior, variable)  # se desactiva el plan anterior en caso que exista
    conn.commit()
    conn = connect_db()
    cursor = conn.cursor()
    insert_script = "INSERT INTO usuario_suscripcion(id_usuario, id_suscripcion, activo, fecha_inicio) " \
                    "VALUES(%s,%s,%s,%s)"
    datos = (str(id), str(tipo), True, str(date.today()))
    cursor.execute(insert_script, datos)
    conn.commit()

    print("Se ha suscrito con éxito\nSe procedera a registrar su pago del correspondiente mes")


def validar_cvv(conn, cod_tarjeta):
    cursor = conn.cursor()
    select_script = "SELECT cvv FROM metodo_pago WHERE cod_tarjeta='%s' " %str(cod_tarjeta)
    cursor.execute(select_script)
    value = cursor.fetchone()

    if value is None:  # no hay tarjetas con este codigo
        return True
    else:
        return value[0]  # retorna el cvv


def realizar_pago_suscripcion(conn, id_usuario):
    cursor = conn.cursor()
    cod_tarjeta = ""
    cvv = 0
    bandier = True
    bandier1 = True
    while bandier is True:
        while bandier1 is True:
            try:
                cod_tarjeta = str\
                    (input("Ingrese el número de su tarjeta con la que realizará el pago "))
                cvv = int(input("Ingrese el CVV de su tarjeta"))
                if len(cod_tarjeta) > 0:
                    bandier1 = False
            except ValueError:
                print("El CVV es un dato numerico\nSe volveran a pedir sus datos")

        cvv_valido = validar_cvv(conn, cod_tarjeta)

        if cvv_valido == cvv:
            fecha = str(date.today())
            print("\t\tLa fecha de pago se registrará la fecha de su dispositivo")
            # insertar en la relacion de la tabla
            insert_script = "INSERT INTO pago(id_usuario, cod_tarjeta) "\
                            "VALUES (%s, %s)"

            insert_values = (id_usuario, cod_tarjeta)
            cursor.execute(insert_script, insert_values)
            conn.commit()
            bandier = False
            print("Su pago ha sido procesado correctamente")
        else:
            print(
                "Su CVV no coincide con el registrado en su metodo de pago, se procedera a reiniciar el proceso de pago")


""" funcion usada por usuario admin para poder desactivar un usuario """
def desactivar_usuario(conn, id_usuario):
    cursor = conn.cursor()
    query = "UPDATE usuario_suscripcion SET activo = False WHERE id_usuario =%s "
    query_value = (id_usuario,)
    cursor.execute(query, query_value)
    conn.commit()
    conn = connect_db()
    cursor = conn.cursor()
    print("El usuario ha sido DESACTIVADO, se procedera ha ELIMINAR su informacion de pago")
    query = "DELETE FROM pago WHERE id_usuario=%s "
    cursor.execute(query, query_value)
    conn.commit()
    print("Informacion de pago ELIMINADA correctamente")
    print("Se ha actualizado el estado de este usuario")


""" mostrar informacion basica de los usuarios """
def mostrar_usuarios(conn):
    query = "SELECT us.id_usuario, us.nombres, us.apellidos, us.nickname, sus.tipo, u.activo, u.fecha_inicio " \
            "FROM usuario us INNER JOIN usuario_suscripcion u on us.id_usuario = u.id_usuario " \
            "INNER JOIN suscripcion sus ON sus.id_suscripcion = u.id_suscripcion "\
            "WHERE u.activo = True ORDER BY sus.tipo, u.activo, u.fecha_inicio;"
    result = create_pandas_table(query, conn)
    print(result)
