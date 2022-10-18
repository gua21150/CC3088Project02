# importacion de librerías
from Control.validation_request import *
from Control.menus import *
from Control.menus.menu_usuario__init___ import *
from Control.menus.menu_admin__init__ import *
from Control.control_admin import iniciar_sesion_admin

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
                validacion = iniciar_sesion_usuario(conn, nick, passw)
                if validacion is not False:
                    id_usuario, suscrip, dias = validacion
                    print("Faltan %s para tu próxima renovación de servicio" % dias)
                    # presentar menu de acciones
                else:
                    print("Este usuario no esta registrado. Valide su nickname y contraseña")

            elif option2 == 2:
                # iniciar sesion como trabajador
                if iniciar_sesion_admin(conn, correo, passw):
                    menu_usuario_admin()
        elif option == 2:  # registrar usuario
            cant = int(input("Ingrese la cantidad de numeros aleatorios que desea obtener: "))

        menu_login()
        option = int(input("Ingrese su opción: "))

    print("Feliz día")
except:
    print("Su entrada no es válida, feliz día")
finally:
    conn.close()
