from datetime import date
from Control.function_validation import solicitar_fecha

"""recupera el id del usuario con el que se estara trabajando"""
def recuperar_id_usuario(conn, usern, passw):
    cursor = conn.cursor()
    cursor.execute("SELECT id_usuario FROM usuario WHERE nickname='%s' AND passwordc='%s'" % (usern, passw))
    id = cursor.fetchone()
    return id[0]


""" solicitar datos para registrar un nuevo usuario """
def solicitar_credenciales(conn):
    try:
        print("\tA continuación se te solicitará información básica para crear tu perfil")
        print("\tSI ALGUNO DE TUS DATOS ES INCORRECTO SE TE NOTIFICARÁ")
        bandier = True
        nombres = str(input("¿Cuáles son tus nombres?"))
        apellidos = str(input("¿Cuáles son tus apellidos?"))
        nickname = str(input("¿Cuál es tu username?"))

        while bandier:  # conocer que el nickname no esta tomado
            cursor = conn.cursor()
            result = cursor.execute("SELECT 1 FROM usuario WHERE nickname='%s'" % nickname)

            if str(result) != 'None':
                bandier = False
            else:
                nickname = str((input("Este nombre de usuario ya esta tomado, intenta con otro")))
        bandier = True
        correo = str(input("¿Cuál es tu correo?"))
        while bandier: # conocer que el correo no esta registrado
            cursor = conn.cursor()
            result = cursor.execute("SELECT 1 FROM usuario WHERE correo='%s'" % correo)

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

        edad = int(input("¿Cuáles son tus nombres?"))
        altura = float(input("¿Cuál es tu altura?"))
        peso = float(input("¿Cuál es tu peso actual?"))
        calorias = float(input("¿Cuáles son tus calorías actuales?"))

        return nombres, apellidos, nickname, edad,  altura, calorias, peso, correo, password
    except ValueError:
        print("Los datos ingresados no son válidos, tendrá que regresar a esta parte del menú")
        return False


"""" registro del usuario dentro de la base de datos, retorna el id del usuario registrado """
def registrar_usuario(conn):
    data = solicitar_credenciales(conn)

    if data is not False:
        cursor = conn.cursor()
        # realizar nuevo codigo de usuario
        cursor.execute("SELECT id_usuario FROM usuario ORDER BY id_usuario DESC LIMIT 1;")  # ultimo usuario
        id_usuario = cursor.fetchone()
        id_usuario = id_usuario[0]  # de la tupla se recupera el primer valor
        last_id = id_usuario[0][4:]  # se recupera los ultimos digitos del id
        new_id = int(last_id)+1    # se aumenta en uno el valor del ultimo id
        id = id_usuario[0].replace(str(last_id), str(new_id))  # el id correspondiente es este
        # insercion de dato
        insert_script = "INSERT INTO usuario(id_usuario, nombres, apellidos, nickname, edad, altura, caloria_actual,peso_actual, correo, passwordc) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        insert_values = (id, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8])
        cursor.execute(insert_script, insert_values)
        conn.commit()
        print("Registro realizado")
        return id, data[8]  # el usuario queda "iniciada" su sesion


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
def registrar_peso(conn, usern, passw):
    data = peso()
    if data is not False:
        id = recuperar_id_usuario(conn, usern, passw)
        cursor = conn.cursor()

        insert_script = "INSERT INTO usuario_registro_historico(id_usuario, peso, caloria, fecha) VALUES(%s, %s, %s, %s)"
        insert_values = (id, data[0], data[1], data[2])
        cursor.execute(insert_script, insert_values)
        conn.commit()
        print("Se ha registrado tu peso y calorías actuales")


""" verifica que el metodo de pago no este ya dentro de la base de datos """
def validar_metodo_pago(conn, cod_tarjeta):
    cursor = conn.conect()
    select_script = "SELECT cvv FROM metodo_pago WHERE cod_tarjeta=%s"
    cursor.execute(select_script % cod_tarjeta)
    value = cursor.fetchone()

    if value == 'None':  # no hay tarjetas con este codigo
        return True
    else:
        return value[0] # retorna el cvv


"""" solicita los datos para el metodo de pago """
def solicitar_pago(conn):
    try:
        cod_tarjeta = str(input("Ingrese el codigo de su tarjeta"))
        value = validar_metodo_pago(conn, cod_tarjeta)
        if value is True:
            nombre = str(input("Ingrese el nombre que aparece en su tarjeta"))
            fecha = solicitar_fecha(" de su tarjeta")
            cvv = int(input("Ingrese el CVV de su tarjeta"))
            tarjeta = int(input("¿Cuál es el tipo de esta tarjeta?\n[1]Crédito\n[2]Débito "))
            tipo_tarjeta = ""
            if tarjeta == 1:
                tipo_tarjeta = "IDTT_C"
            elif tarjeta == 2:
                tipo_tarjeta = "IDTT_D"
            facturacion = date.today()
            print("La fecha de facturacion se tomara como el '%s' de cada mes" % facturacion.day)

            return cod_tarjeta, nombre, fecha, cvv, tipo_tarjeta, facturacion
        else:
            print("Este codigo de tarjeta ya existe")
            # se procede a pedir el cvv
            cvv = int(input("Ingrese el CVV de su tarjeta\n\tSi es correcto, se agregara esta tarjeta como metodo de pago a su usuario"))
            if cvv == int(value):
                return cod_tarjeta
            else:
                print("El CVV no coincide, esta tarjeta no le pertenece")
                return False
    except ValueError:
        print("El tipo de dato no coincide con lo ingresado\n\tIntentelo de nuevo")
        return False


"""" se registra el metodo de pago dentro de la base de datos y se asigna el metodo de pago al usuario """
def registro_metodo_pago(conn, id):
    data = solicitar_pago()
    cod_tarjeta = 0
    if data is not False:
        if len(data) > 1:  # indica que es una nueva tarjeta de pago
            cursor = conn.conect()
            insert_script = "INSERT INTO metodo_pago(cod_tarjeta, nombre_tarjeta, fecha_caducidad, cvv, tipo_tarjeta, fecha_facturacion) VALUES(%s,%s,%s,%s,%s,%s)"
            insert_values = data
            cursor.execute(insert_script, insert_values)
            conn.commit()

            cod_tarjeta = data[0]
        else:
            cod_tarjeta = data

        # insertar en la relacion de la tabla
        insert_script = "INSERT INTO pago(id_usuario, cod_tarjeta) VALUES (%s,%s)"
        insert_values = (id, cod_tarjeta)
        cursor.execute(insert_script, insert_values)
        conn.commit()
        cursor.close()


""" registrar suscripcion """
def registrar_suscripcion(conn, id, tipo):
    print("Tu fecha de inicio se registrara como el día actual en tu dispositivo")
    cursor = conn.conect()
    insert_script = "INSERT INTO usuario_suscripcion(id_usuario, id_suscripcion, activo, fecha_inicio) VALUES(%s,%s,%s,%s)"
    insert_values = (id, tipo, True, str(date.today()))
    cursor.execute(insert_script, insert_values)
    conn.commit()
    # falta arreglar metodo de pago y pago
    print("Se ha suscrito con exito")
    cursor.close()