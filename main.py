# importacion de librerías
from function_validation import *
from menus import *
from gestion_trabajador import *


# credenciales de la base de datos
# host, dbname, user, password = credenciales()
conexion = conect_db('localhost', 'proyecto02', 'postgres', 'moon!9920!2')
 
print("---------------")  
print("Bienvenido a iHealth+")
conexion.close()
try:               
    menu_login()
    option = int(input("Ingrese su opción: "))

    while(option != 0):
        if option == 1: # iniciar sesion
            menu_iniciar_sesion() # llamada al menu 
            option2 = int(input("Ingrese su selección: "))

            if option2 == 1: # iniciar sesion como usuario             
                nick, passw = credencial_login()
                if validar_usuario(1, nick, passw):
                    print("perro")                   
            elif option2 == 2:
                # iniciar sesion como trabajador
                correo, passw = credencial_login_trabajador()
                if validar_usuario(2, correo, passw):
                    print("gato")    
        elif option == 2: # registrar usuario
            cant = int(input("Ingrese la cantidad de numeros aleatorios que desea obtener: "))
            
        menu_login()
        option = int(input("Ingrese su opción: "))
    
    print("Feliz día")    
except:
    print("Su entrada no es válida, feliz día")    
