## datos para trabajador 
def credencial_login_trabajador():    
    bandera = False
    while(bandera == False):
        username = str(input("¿Cuál es tu correo? "))
        passw = str(input("¿Cuál es tu contraseña?: "))
        
        if len(username)>0 and len(passw)>0:
            bandera = True
            return username, passw  