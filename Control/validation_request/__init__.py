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
            dat = input("Ingrese el dia '%s', el mes '%s' tiene rango de dias entre 1 a '%s' " % (
            argumento, mes, dias_aceptados))
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
            dat = input("Ingrese la hora '%s', debe de estar entre 0 y 23 " % argumento)

    bandier = False
    while bandier is False:
        dat = input("Ingrese los minutos '%s' " % argumento)
        mes = 0
        try:
            mes = int(dat)
        except ValueError:
            print("El dato ingresado no es numerico")

        if 0 <= mes <= 59:
            bandier = True
        else:
            dat = input("Ingrese los minutos '%s', debe de estar entre 0 a 59 " % argumento)

    while bandier is False:
        dat = input("Ingrese la hora de finalización '%s' en formato de 24 horas" % argumento)
        try:
            hora_f = int(dat)
        except ValueError:
            print("El dato ingresado no es numerico")

        if 0 <= hora_i <= hora_f <= 23:
            bandier = True
        else:
            dat = input(
                "Ingrese la hora '%s', debe de estar entre 0 y 23 y debe ser mayor que su hora de inicio" % argumento)

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
            dat = input("Ingrese los minutos '%s', debe de estar entre 0 a 59 " % argumento)

    hora_i_minutos = (hora_i * 60) + min_i
    hora_f_minutos = (hora_f * 60) + min_f
    total_tiempo = hora_f_minutos - hora_i_minutos
    if (hora_f_minutos >= hora_i_minutos) and 30 <= total_tiempo <= 60:
        return ("%s:%s" % (hora_i, min_i)), ("%s:%s" % (hora_f, min_f)), total_tiempo
    else:
        print("Los datos ingresados no cumplen con que la sesion sea de 30min a 1 hora")
        return False


""" visualiza la informacion en un formato mas estilizado """


def create_pandas_table(sql_query, conn):
    database = conn
    table = pd.read_sql_query(sql_query, database)
    return table
