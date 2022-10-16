## menus para todos 
def menu_login():    
    print("\t¿Cuál acción deseas realizar?")
    print("\t\t[1] Iniciar sesión")    
    print("\t\t[2] Registrarse")
    print("\t\t[0] Salir del programa")

def menu_iniciar_sesion():
    print("\t¿Cuál miembro iHealth+ eres?")
    print("\t\t[1] Usuario")    
    print("\t\t[2] Trabajador")
    print("\t\t[0] Regresar")

## datos para usuario
def credencial_login():    
    bandera = False
    while(bandera == False):
        username = str(input("\t\t¿Cuál es tu nombre de usuario? "))
        passw = str(input("\t\t¿Cuál es tu contraseña?: "))
        
        if len(username)>0 and len(passw)>0:
            bandera = True
            return username, passw   

