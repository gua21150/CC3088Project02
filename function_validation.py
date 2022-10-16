import psycopg2
from config import config

# conectar a base de datos
def conect_db():
    # conexion a la base de datos
    conn = None    
    try:
        # leer los paramatros del database.ini
        params = config()
        conn = psycopg2.connect(**params)
        cursor = conn.cursor()
        print("Sesion a la base de datos ha sido exitosa")
        
        return conn        
    except psycopg2.OperationalError:
        print("Alguna credencial no ha sido ingresada correctamente")

# validacion que exista el usuario
def validar_usuario(tipo, username, passw):
    try:
        conn = conect_db()        
        cur = conn.cursor()   
        if tipo == 1:
            cur.execute("SELECT id_usuario FROM usuario WHERE nickname='%s' AND passwordc='%s'" % (username, passw))
        elif tipo == 2:
            cur.execute("SELECT id FROM trabajador WHERE correo='%s' AND passwordc='%s'" % (username, passw))
        result = str(cur.fetchone())
        
        if result != 'None':
            print ("Sesión Iniciada con éxito")
            return True
        else:
            print("Este nickname o contraseña no está asociado a un usuario iHealth+")    
            return False    
    except psycopg2.OperationalError:
        print("Se ha producido un error")
