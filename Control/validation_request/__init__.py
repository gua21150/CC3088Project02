import psycopg2
from calendar import monthrange
from datetime import date
import pandas as pd
from config import config
"""               REQUEST                      """
""" CONECTAR A BASE DE DATOS"""
def connect_db():
    # conexion a la base de datos       
    try:
        # leer los paramatros del database.ini
        params = config()
        conn = psycopg2.connect(**params)
        cursor = conn.cursor()
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
def solicitar_fecha(argumento):
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

        if 1950 <= anio <= 2022:
            bandier = True
        else:
            dat = input("Ingrese el año '%s', debe de estar entre 1950 a 2022 " % argumento)

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
            dat = input("Ingrese el mes '%s', debe de estar entre 1 a 12 " % argumento)

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
            dat = input("Ingrese el dia '%s', el mes '%s' tiene rango de dias entre 1 a '%s' " % (argumento, mes, dias_aceptados))
    return date(anio, mes, dia)

""" visualiza la informacion en un formato mas estilizado """
def create_pandas_table(sql_query, conn):
    database = conn
    table = pd.read_sql_query(sql_query, database)
    return table


""" VALIDACION"""
""" valida que el usuario este dentro de la base de datos """
def validar_usuario(conn, tipo, username, passw):
    try:
        cur = conn.cursor()
        if tipo == 1:
            cur.execute("SELECT id_usuario FROM usuario WHERE nickname='%s' AND passwordc='%s'" % (username, passw))
        elif tipo == 2:
            cur.execute("SELECT id FROM trabajador WHERE correo='%s' AND passwordc='%s'" % (username, passw))
        result = str(cur.fetchone())

        if result != 'None':
            print("Sesión Iniciada con éxito")
            return True
        else:
            print("Este nickname o contraseña no está asociado a un usuario iHealth+")
            return False
    except psycopg2.OperationalError:
        print("Se ha producido un error")
