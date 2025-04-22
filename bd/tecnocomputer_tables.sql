-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    usuario_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    rol VARCHAR(20) NOT NULL,
    estado VARCHAR(20) DEFAULT 'activo',
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    ultimo_login DATETIME
);

-- Crear tabla de departamentos
CREATE TABLE IF NOT EXISTS departamentos (
    departamento_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT,
    estado VARCHAR(20) DEFAULT 'activo'
);

-- Crear tabla de tickets
CREATE TABLE IF NOT EXISTS tickets (
    ticket_id INT AUTO_INCREMENT PRIMARY KEY,
    orden_id INT,
    titulo VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    departamento_id INT NOT NULL,
    estado VARCHAR(20) NOT NULL,
    prioridad VARCHAR(20) NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_id INT NOT NULL,
    ultimo_comentario TEXT,
    tiempo_resolucion INT,
    FOREIGN KEY (orden_id) REFERENCES ordenes_servicio(idordenes_servicio) ON DELETE SET NULL,
    FOREIGN KEY (departamento_id) REFERENCES departamentos(departamento_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
);

-- Crear tabla de comentarios de tickets
CREATE TABLE IF NOT EXISTS ticket_comentarios (
    comentario_id INT AUTO_INCREMENT PRIMARY KEY,
    ticket_id INT NOT NULL,
    usuario_id INT NOT NULL,
    comentario TEXT NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
);

-- Insertar departamentos por defecto
INSERT INTO departamentos (nombre, descripcion) VALUES
('Soporte Técnico', 'Departamento de soporte técnico para equipos'),
('Ventas', 'Departamento de ventas y atención al cliente'),
('Administración', 'Departamento administrativo');

-- Insertar usuario administrador por defecto
INSERT INTO usuarios (nombre, apellido, email, password, rol) VALUES
('Admin', 'Sistema', 'admin@tecnocomputer.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'admin'); 