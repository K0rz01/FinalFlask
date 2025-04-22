-- Modificar la tabla ordenes_servicio para corregir el tipo de id_cliente
ALTER TABLE ordenes_servicio 
MODIFY COLUMN id_cliente varchar(50),
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
ADD CONSTRAINT fk_cliente 
FOREIGN KEY (id_cliente) REFERENCES clientes(cliente_id)
ON DELETE RESTRICT
ON UPDATE CASCADE;

-- Agregar índices básicos para mejorar el rendimiento
ALTER TABLE ordenes_servicio
ADD INDEX idx_fecha_entrada (fecha_entrada),
ADD INDEX idx_estado (estado);

ALTER TABLE clientes
ADD INDEX idx_phone (phone_number),
ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- Agregar algunos estados predefinidos para ordenes_servicio
ALTER TABLE ordenes_servicio
MODIFY COLUMN estado varchar(45) DEFAULT 'Pendiente' 
CHECK (estado IN ('Pendiente', 'En Revisión', 'En Reparación', 'Completado', 'Entregado', 'Cancelado'));

-- Deshabilitar restricciones de clave foránea temporalmente
SET FOREIGN_KEY_CHECKS = 0;

-- Eliminar la tabla user si existe
DROP TABLE IF EXISTS `user`;

-- Crear la tabla user con la estructura correcta
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `name` varchar(100) NOT NULL,
  `rol` ENUM('cliente', 'tecnico') NOT NULL DEFAULT 'cliente',
  `estado` ENUM('activo', 'inactivo') NOT NULL DEFAULT 'activo',
  `fecha_creacion` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `ultimo_login` DATETIME DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insertar usuario técnico por defecto
INSERT INTO `user` (`email`, `password`, `name`, `rol`, `estado`) 
VALUES ('tecnico@tecnocomputer.com', '2bd5100f475915a8990f6a4b342ac161e5eb754581d81a4b6462843e63601ada', 'Técnico Principal', 'tecnico', 'activo');

-- Insertar usuario cliente por defecto
INSERT INTO `user` (`email`, `password`, `name`, `rol`, `estado`) 
VALUES ('cliente@tecnocomputer.com', '09a31a7001e261ab1e056182a71d3cf57f582ca9a29cff5eb83be0f0549730a9', 'Cliente Demo', 'cliente', 'activo');

-- Habilitar restricciones de clave foránea
SET FOREIGN_KEY_CHECKS = 1;
