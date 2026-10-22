-- datos que necesita el inventario para funcionar. Se puede correr varias veces, no duplica nada.
-- correr en pgAdmin sobre sistema_erp_db despues de script_bd.sql

INSERT INTO Categoria (nombre) VALUES
    ('Calzado'), ('Ropa'), ('Bolsos'), ('Accesorios'), ('Bisutería')
ON CONFLICT (nombre) DO NOTHING;

INSERT INTO Estado_Producto (nombre) VALUES ('Activo'), ('Inactivo')
ON CONFLICT (nombre) DO NOTHING;

INSERT INTO Tipo_Movimiento (nombre) VALUES ('Entrada'), ('Salida')
ON CONFLICT (nombre) DO NOTHING;

-- el que crea usuarios ahora es el Auxiliar administrativo. Si todavia no tienen ninguno,
-- cambien el rol de su usuario de prueba con esto (poner el correo de ustedes):
-- UPDATE Usuario SET id_rol = (SELECT id_rol FROM Rol WHERE nombre = 'Auxiliar administrativo')
-- WHERE correo = 'su_correo@empresa.com';
