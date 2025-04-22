-- Agregar columna para tickets a la tabla de órdenes de servicio
ALTER TABLE `ordenes_servicio`
ADD COLUMN `ticket_id` INT DEFAULT NULL,
ADD CONSTRAINT `fk_orden_ticket` FOREIGN KEY (`ticket_id`) REFERENCES `tickets`(`ticket_id`) ON DELETE SET NULL;

-- Crear índice para búsquedas eficientes
CREATE INDEX `idx_orden_ticket` ON `ordenes_servicio`(`ticket_id`);

-- Actualizar comentarios de la tabla
ALTER TABLE `ordenes_servicio` COMMENT = 'Tabla de órdenes de servicio con soporte para tickets de seguimiento'; 