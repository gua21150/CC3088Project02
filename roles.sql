-- creacion de rol para usuarios
CREATE ROLE usuario_ihealth;
-- tenga permisos de iniciar sesion
ALTER ROLE usuario_ihealth WITH LOGIN PASSWORD 'usuario';
-- permisos de los usuarios
GRANT SELECT    ON  usuario, usuario_suscripcion, usuario_registro_historico, metodo_pago,
                    suscripcion, sincronizacion_ejercicio, sesion_ejercicio,
                    categoria_ejercicio, trabajador 
                TO  usuario_ihealth;
GRANT INSERT    ON  usuario, usuario_registro_historico, metodo_pago, pago, sincronizacion_ejercicio,
                    bitacora_admin_usuarios, bitacora_usuario, usuario_suscripcion
                TO  usuario_ihealth;
GRANT UPDATE    ON usuario_suscripcion, sincronizacion_ejercicio TO usuario_ihealth;
GRANT USAGE, SELECT, UPDATE    ON SEQUENCE usuario_sequence TO usuario_ihealth;
GRANT EXECUTE   ON PROCEDURE bitacora_admin, bitacora_busqueda_usuario TO usuario_ihealth;
GRANT EXECUTE   ON FUNCTION obtener_nombre TO usuario_ihealth;

-- creacion de roles de administradores
    -- admin de usuarios
CREATE ROLE admin_usuarios;
    -- tenga permisos de iniciar sesion
ALTER ROLE admin_usuarios WITH LOGIN PASSWORD 'ad_user';
    -- permisos de los usuarios
-- permisos de los usuarios
GRANT SELECT    ON  usuario, usuario_suscripcion, suscripcion, trabajador, tipo_rol
                TO  admin_usuarios;
GRANT INSERT    ON  bitacora_admin
                TO  admin_usuarios;
GRANT UPDATE    ON usuario, usuario_suscripcion TO admin_usuarios;
GRANT SELECT,  DELETE ON pago TO admin_usuarios;
GRANT EXECUTE   ON PROCEDURE bitacora_admin TO admin_usuarios;
GRANT EXECUTE   ON FUNCTION obtener_nombre TO admin_usuarios;


   -- admin de sesiones
CREATE ROLE admin_sesiones;
    -- tenga permisos de iniciar sesion
ALTER ROLE admin_sesiones WITH LOGIN PASSWORD 'ad_sesion';
    -- permisos de los usuarios
-- permisos de los usuarios
GRANT SELECT    ON  trabajador, categoria_ejercicio, sesion_ejercicio
                TO  admin_sesiones;
GRANT INSERT    ON  bitacora_admin, sesion_ejercicio, trabajador
                TO  admin_sesiones;
GRANT UPDATE    ON  sesion_ejercicio 
                TO admin_sesiones;
GRANT SELECT, DELETE ON sesion_ejercicio TO admin_sesiones;
GRANT EXECUTE   ON PROCEDURE bitacora_admin TO admin_sesiones;
GRANT EXECUTE   ON FUNCTION obtener_nombre TO admin_sesiones;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE sesion_sequence, entrenador_sequence  TO admin_sesiones;

   -- admin de reporteria
CREATE ROLE admin_reporteria;
    -- tenga permisos de iniciar sesion
ALTER ROLE admin_reporteria WITH LOGIN PASSWORD 'ad_reporteria';
    -- permisos de los usuarios
-- permisos de los usuarios

GRANT CREATE    ON SCHEMA public TO admin_reporteria;
ALTER VIEW IF EXISTS reporteria3 OWNER TO admin_reporteria;
GRANT SELECT    ON  sincronizacion_ejercicio, sesion_ejercicio, categoria_ejercicio, 
                    trabajador, usuario_suscripcion, bitacora_admin, bitacora_admin_usuarios, usuario,
                    tipo_accion, bitacora_usuario, reporteria1, reporteria2, reporteria3, reporteria4
                TO  admin_reporteria;
GRANT INSERT    ON  bitacora_admin
                TO  admin_reporteria;
GRANT EXECUTE   ON PROCEDURE bitacora_admin TO admin_reporteria;
GRANT EXECUTE   ON FUNCTION obtener_nombre TO admin_reporteria;

-- admin de super admin
CREATE ROLE super_admin;
    -- tenga permisos de iniciar sesion
ALTER ROLE super_admin WITH LOGIN PASSWORD 'superman';
    -- permisos de los usuarios
-- permisos de los usuarios
GRANT SELECT    ON  trabajador, tipo_rol
                TO  super_admin;
GRANT INSERT    ON  bitacora_admin, trabajador
                TO  super_admin;
GRANT UPDATE    ON trabajador TO super_admin;                
GRANT EXECUTE   ON PROCEDURE bitacora_admin TO super_admin;
GRANT EXECUTE   ON FUNCTION obtener_nombre TO super_admin;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE entrenador_sequence  TO super_admin;
