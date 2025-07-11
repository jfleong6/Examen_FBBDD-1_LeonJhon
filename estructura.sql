CREATE DATABASE gestion_inventario;
USE DATABASE gestion_inventario;

CREATE TABLE IF NOT EXISTS Clientes (
    id INTEGER,
    cedula INTEGER UNIQUE,
    nombre VARCHAR(100),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS Productos (
    id INTEGER,
    nombre VARCHAR(100),
    precio_unitario INTEGER,
    stock INTEGER,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS Usuarios (
    id INTEGER,
    cedula INTEGER UNIQUE,
    nombre VARCHAR(100),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS Proveedor (
    id INTEGER,
    nit INTEGER,
    nombre VARCHAR(100),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS Ventas (
    id INTEGER,
    fecha DATETIME,
    cantidad INTEGER,
    total INTEGER,
    id_cliente INTEGER,
    id_usuario INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id),
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id)
);

CREATE TABLE IF NOT EXISTS Venta_producto (
    id_venta INTEGER,
    id_producto INTEGER,
    cantidad INTEGER,
    total INTEGER,
    FOREIGN KEY (id_venta) REFERENCES Ventas(id),
    FOREIGN KEY (id_producto) REFERENCES Productos(id)
);

CREATE TABLE IF NOT EXISTS Compra (
    id INTEGER,
    fecha DATETIME,
    cantidad INTEGER,
    total INTEGER,
    id_proveedor INTEGER,
    id_usuario INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (id_proveedor) REFERENCES Proveedor(id),
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id)
);

CREATE TABLE IF NOT EXISTS compra_producto (
    id_compra INTEGER,
    id_producto INTEGER,
    cantidad INTEGER,
    total INTEGER,
    FOREIGN KEY (id_compra) REFERENCES Compra(id),
    FOREIGN KEY (id_producto) REFERENCES Productos(id)
);

CREATE TABLE IF NOT EXISTS Roles (
    id INTEGER,
    rol VARCHAR(100),
    PRIMARY KEY (id)
);

