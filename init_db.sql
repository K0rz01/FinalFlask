-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS tecnocomputer;

-- Crear el usuario y otorgar privilegios
CREATE USER IF NOT EXISTS 'user1'@'localhost' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON tecnocomputer.* TO 'user1'@'localhost';
FLUSH PRIVILEGES;

-- Usar la base de datos
USE tecnocomputer;

-- Crear tabla clientes
CREATE TABLE IF NOT EXISTS clientes (
    cliente_id varchar(50) NOT NULL,
    first_name varchar(50) NOT NULL,
    last_name varchar(50) NOT NULL,
    email varchar(100) NOT NULL,
    phone_number varchar(20) DEFAULT NULL,
    street_address varchar(100) DEFAULT NULL,
    city varchar(50) DEFAULT NULL,
    state varchar(50) DEFAULT NULL,
    postal_code varchar(10) DEFAULT NULL,
    country varchar(50) DEFAULT NULL,
    gender varchar(10) DEFAULT NULL,
    registration_date datetime DEFAULT CURRENT_TIMESTAMP,
    account_status varchar(20) DEFAULT 'active',
    notes text,
    contact_preferences varchar(50) DEFAULT NULL,
    referred_by varchar(50) DEFAULT NULL,
    customer_type varchar(20) DEFAULT NULL,
    PRIMARY KEY (cliente_id),
    UNIQUE KEY email (email)
);

-- Crear tabla ordenes_servicio
CREATE TABLE IF NOT EXISTS ordenes_servicio (
    idordenes_servicio int NOT NULL AUTO_INCREMENT,
    marca varchar(45) DEFAULT NULL,
    modelo varchar(45) DEFAULT NULL,
    serial varchar(45) DEFAULT NULL,
    diag_inicial varchar(500) DEFAULT NULL,
    diag_final varchar(500) DEFAULT NULL,
    serial_ram_1 varchar(45) DEFAULT NULL,
    serial_ram_2 varchar(45) DEFAULT NULL,
    serial_disco_1 varchar(45) DEFAULT NULL,
    serial_disco_2 varchar(45) DEFAULT NULL,
    serial_cargador varchar(45) DEFAULT NULL,
    serial_bateria varchar(45) DEFAULT NULL,
    fecha_entrada datetime DEFAULT CURRENT_TIMESTAMP,
    fecha_salida datetime DEFAULT NULL,
    id_cliente bigint DEFAULT NULL,
    inicio_trabajo datetime DEFAULT NULL,
    fin_trabajo datetime DEFAULT NULL,
    estado varchar(45) DEFAULT NULL,
    id_tecnico varchar(45) DEFAULT NULL,
    PRIMARY KEY (idordenes_servicio)
);

-- Insertar algunos datos de ejemplo
INSERT INTO clientes (cliente_id, first_name, last_name, email, phone_number, city, state, country)
VALUES 
('1', 'Juan', 'Pérez', 'juan@example.com', '123456789', 'Pereira', 'Risaralda', 'Colombia'),
('2', 'María', 'García', 'maria@example.com', '987654321', 'Pereira', 'Risaralda', 'Colombia');

INSERT INTO ordenes_servicio (marca, modelo, serial, diag_inicial, estado, id_cliente)
VALUES 
('HP', 'Pavilion', 'SN123456', 'No enciende', 'Pendiente por revision', 1),
('Dell', 'Inspiron', 'SN789012', 'Pantalla dañada', 'En Revision', 2);
