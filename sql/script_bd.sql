-- Script de la base de datos (PostgreSQL). Ejecutar en una base vacia llamada sistema_erp_db.

CREATE TABLE Rol (
    id_rol SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE Tipo_Documento (
    id_tipo_documento SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE Estado_Usuario (
    id_estado_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE Categoria (
    id_categoria SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE Estado_Producto (
    id_estado_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE Tipo_Movimiento (
    id_tipo_movimiento SERIAL PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE Tipo_Reporte (
    id_tipo_reporte SERIAL PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE Usuario (
    id_usuario SERIAL PRIMARY KEY,
    id_rol INT NOT NULL,
    id_tipo_documento INT NOT NULL,
    id_estado_usuario INT NOT NULL,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    primer_nombre VARCHAR(50) NOT NULL,
    segundo_nombre VARCHAR(50),
    primer_apellido VARCHAR(50) NOT NULL,
    segundo_apellido VARCHAR(50),
    correo VARCHAR(50) NOT NULL UNIQUE,
    numero_documento VARCHAR(30) NOT NULL UNIQUE,
    contrasenia VARCHAR(100) NOT NULL,
    CONSTRAINT fk_usuario_rol FOREIGN KEY (id_rol) REFERENCES Rol(id_rol),
    CONSTRAINT fk_usuario_tipo_doc FOREIGN KEY (id_tipo_documento) REFERENCES Tipo_Documento(id_tipo_documento),
    CONSTRAINT fk_usuario_estado FOREIGN KEY (id_estado_usuario) REFERENCES Estado_Usuario(id_estado_usuario)
);

CREATE TABLE Producto (
    id_producto SERIAL PRIMARY KEY,
    codigo_identificacion VARCHAR(50) NOT NULL UNIQUE,
    id_categoria INT NOT NULL,
    id_estado_producto INT NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    unidad_medida VARCHAR(20) NOT NULL,
    precio_venta NUMERIC(12, 2) NOT NULL CHECK (precio_venta >= 0),
    stock_actual INT NOT NULL CHECK (stock_actual >= 0),
    stock_minimo INT NOT NULL CHECK (stock_minimo >= 0),
    CONSTRAINT fk_producto_categoria FOREIGN KEY (id_categoria) REFERENCES Categoria(id_categoria),
    CONSTRAINT fk_producto_estado FOREIGN KEY (id_estado_producto) REFERENCES Estado_Producto(id_estado_producto)
);

CREATE TABLE Registro_Bitacora (
    id_registro_bitacora SERIAL PRIMARY KEY,
    id_usuario_afectado INT NOT NULL,
    id_usuario_responsable INT NOT NULL,
    accion VARCHAR(50) NOT NULL,
    cambio_realizado TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_bitacora_afectado FOREIGN KEY (id_usuario_afectado) REFERENCES Usuario(id_usuario),
    CONSTRAINT fk_bitacora_responsable FOREIGN KEY (id_usuario_responsable) REFERENCES Usuario(id_usuario)
);

CREATE TABLE Movimiento_Inventario (
    id_movimiento_inventario SERIAL PRIMARY KEY,
    id_producto INT NOT NULL,
    id_usuario INT NOT NULL,
    id_tipo_movimiento INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    costo_unitario NUMERIC(12, 2) NOT NULL CHECK (costo_unitario >= 0),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_movimiento_producto FOREIGN KEY (id_producto) REFERENCES Producto(id_producto),
    CONSTRAINT fk_movimiento_usuario FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    CONSTRAINT fk_movimiento_tipo FOREIGN KEY (id_tipo_movimiento) REFERENCES Tipo_Movimiento(id_tipo_movimiento)
);

CREATE TABLE Reporte (
    id_reporte SERIAL PRIMARY KEY,
    id_usuario_gerente INT NOT NULL,
    id_tipo_reporte INT NOT NULL,
    fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_inicial_reporte DATE NOT NULL,
    fecha_final_reporte DATE NOT NULL,
    CONSTRAINT fk_reporte_gerente FOREIGN KEY (id_usuario_gerente) REFERENCES Usuario(id_usuario),
    CONSTRAINT fk_reporte_tipo FOREIGN KEY (id_tipo_reporte) REFERENCES Tipo_Reporte(id_tipo_reporte)
);

INSERT INTO Rol (nombre) VALUES ('Administrador'), ('Vendedor'), ('Auxiliar administrativo');
INSERT INTO Tipo_Documento (nombre) VALUES ('Cédula de Ciudadanía'), ('Cédula de extranjería');
INSERT INTO Estado_Usuario (nombre) VALUES ('Contratado'), ('Suspendido'), ('En vacaciones'), ('Retirado');


ALTER TABLE registro_bitacora ALTER COLUMN id_usuario_afectado DROP NOT NULL;
ALTER TABLE registro_bitacora ALTER COLUMN id_usuario_responsable DROP NOT NULL;


select * from registro_bitacora;
select * from usuario;

ALTER TABLE registro_bitacora ALTER COLUMN id_usuario_afectado DROP NOT NULL;
ALTER TABLE registro_bitacora ALTER COLUMN id_usuario_responsable DROP NOT NULL;

CREATE OR REPLACE FUNCTION proteger_documentos_usuario()
RETURNS TRIGGER AS $$
BEGIN

    IF NEW.id_tipo_documento IS DISTINCT FROM OLD.id_tipo_documento THEN
        RAISE EXCEPTION 'No está permitido modificar el tipo de documento ';
    END IF;

    IF NEW.numero_documento IS DISTINCT FROM OLD.numero_documento THEN
        RAISE EXCEPTION 'No está permitido modificar el número de documento ';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_proteger_documentos_usuario ON Usuario;

CREATE TRIGGER trg_proteger_documentos_usuario
BEFORE UPDATE ON Usuario
FOR EACH ROW
EXECUTE FUNCTION proteger_documentos_usuario();