# importacion de librerías
from Control.validation_request import *
from Control.menus import *
from Control.menus.menu_usuario__init___ import *


conn = connect_db()  # se conecta a la base de datos
print("---------------")  
print("Bienvenido a iHealth+")
try:
    menu_login()
    option = int(input("Ingrese su opción: "))

    while option != 0:
        if option == 1:  # iniciar sesion
            menu_iniciar_sesion()  # llamada al menu
            option2 = int(input("Ingrese su selección: "))

            if option2 == 1:  # iniciar sesion como usuario
                nick, passw = credencial_login("¿Cuál es tu nombre de usuario?")
                if validar_usuario(conn, 1, nick, passw):
                    registrar_peso(conn, nick, passw)
                    accion_usuario_no_suscrito(conn, id)

            elif option2 == 2:
                # iniciar sesion como trabajador
                correo, passw = credencial_login("¿Cuál es tu correo?")
                if validar_usuario(conn, 2, correo, passw):
                    print("gato")    
        elif option == 2:  # registrar usuario
            cant = int(input("Ingrese la cantidad de numeros aleatorios que desea obtener: "))
            
        menu_login()
        option = int(input("Ingrese su opción: "))
    
    print("Feliz día")    
except:
    print("Su entrada no es válida, feliz día") 
finally:
    conn.close()
