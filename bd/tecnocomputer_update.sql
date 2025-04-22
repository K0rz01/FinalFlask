-- Actualizar tabla de tickets para mejorar la integración con órdenes
ALTER TABLE tickets
ADD COLUMN orden_id INT AFTER ticket_id,
ADD FOREIGN KEY (orden_id) REFERENCES ordenes_servicio(idordenes_servicio) ON DELETE SET NULL,
ADD COLUMN fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
ADD COLUMN ultimo_comentario TEXT,
ADD COLUMN tiempo_resolucion INT COMMENT 'Tiempo en minutos para resolver el ticket';

-- Crear tabla de historial de tickets
CREATE TABLE IF NOT EXISTS ticket_historial (
    historial_id INT AUTO_INCREMENT PRIMARY KEY,
    ticket_id INT NOT NULL,
    usuario_id INT NOT NULL,
    accion VARCHAR(50) NOT NULL,
    descripcion TEXT,
    fecha_cambio DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
);

-- Crear índices para optimizar consultas
CREATE INDEX idx_tickets_orden ON tickets(orden_id);
CREATE INDEX idx_tickets_estado ON tickets(estado);
CREATE INDEX idx_tickets_prioridad ON tickets(prioridad);
CREATE INDEX idx_tickets_fecha ON tickets(fecha_creacion);
CREATE INDEX idx_tickets_ultima_actualizacion ON tickets(fecha_actualizacion);
CREATE INDEX idx_historial_ticket ON ticket_historial(ticket_id);
CREATE INDEX idx_historial_fecha ON ticket_historial(fecha_cambio);

-- Actualizar tabla de órdenes de servicio
ALTER TABLE ordenes_servicio
ADD COLUMN ticket_id INT,
ADD FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id) ON DELETE SET NULL,
ADD COLUMN tiempo_estimado INT COMMENT 'Tiempo estimado en minutos para la reparación',
ADD COLUMN costo_estimado DECIMAL(10,2) COMMENT 'Costo estimado de la reparación',
ADD COLUMN notas_internas TEXT COMMENT 'Notas internas para el técnico';

-- Crear vista para tickets y órdenes
CREATE VIEW vista_tickets_ordenes AS
SELECT 
    t.ticket_id,
    t.titulo,
    t.descripcion,
    t.estado as estado_ticket,
    t.prioridad,
    t.fecha_creacion,
    t.fecha_actualizacion,
    t.ultimo_comentario,
    t.tiempo_resolucion,
    o.idordenes_servicio as orden_id,
    o.marca,
    o.modelo,
    o.serial,
    o.estado as estado_orden,
    o.diag_inicial,
    o.diag_final,
    o.fecha_entrada,
    o.fecha_salida,
    o.tiempo_estimado,
    o.costo_estimado
FROM tickets t
LEFT JOIN ordenes_servicio o ON t.orden_id = o.idordenes_servicio; 