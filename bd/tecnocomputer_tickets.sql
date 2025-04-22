-- Crear tabla de tickets
CREATE TABLE IF NOT EXISTS tickets (
    ticket_id INT AUTO_INCREMENT PRIMARY KEY,
    orden_id INT,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    departamento_id INT NOT NULL,
    estado ENUM('abierto', 'cerrado', 'en_progreso', 'pendiente') DEFAULT 'abierto',
    prioridad ENUM('baja', 'normal', 'alta', 'urgente') DEFAULT 'normal',
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    creado_por INT,
    asignado_a INT,
    FOREIGN KEY (orden_id) REFERENCES ordenes_servicio(orden_id) ON DELETE SET NULL,
    FOREIGN KEY (departamento_id) REFERENCES departamentos(departamento_id),
    FOREIGN KEY (creado_por) REFERENCES usuarios(usuario_id),
    FOREIGN KEY (asignado_a) REFERENCES usuarios(usuario_id)
);

-- Crear tabla de comentarios de tickets
CREATE TABLE IF NOT EXISTS ticket_comentarios (
    comentario_id INT AUTO_INCREMENT PRIMARY KEY,
    ticket_id INT NOT NULL,
    usuario_id INT NOT NULL,
    contenido TEXT NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
);

-- Crear tabla de departamentos
CREATE TABLE IF NOT EXISTS departamentos (
    departamento_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    estado ENUM('activo', 'inactivo') DEFAULT 'activo'
);

-- Insertar departamentos por defecto
INSERT INTO departamentos (nombre, descripcion) VALUES
('Soporte Técnico', 'Departamento de soporte técnico y mantenimiento'),
('Ventas', 'Departamento de ventas y atención al cliente'),
('Administración', 'Departamento administrativo'),
('Desarrollo', 'Departamento de desarrollo y programación');

-- Crear índice para búsquedas eficientes
CREATE INDEX idx_tickets_orden ON tickets(orden_id);
CREATE INDEX idx_tickets_estado ON tickets(estado);
CREATE INDEX idx_tickets_prioridad ON tickets(prioridad);
CREATE INDEX idx_tickets_fecha ON tickets(fecha_creacion); 