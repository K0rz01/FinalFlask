-- Estandarizar los estados
UPDATE ordenes_servicio 
SET estado = 'REPARADO' 
WHERE estado = 'REPARADADO';

UPDATE ordenes_servicio 
SET estado = 'PENDIENTE' 
WHERE estado = 'Pendiente por revision' 
   OR estado IS NULL;

UPDATE ordenes_servicio 
SET estado = 'NO REPARADO' 
WHERE estado = 'INDETERMINADO';

UPDATE ordenes_servicio 
SET estado = 'EN REVISION' 
WHERE estado = 'FALTA PRUEBA DE CARGA';

-- Agregar restricción de estados válidos
ALTER TABLE ordenes_servicio
MODIFY estado ENUM('PENDIENTE', 'EN REVISION', 'REPARADO', 'NO REPARADO') NOT NULL DEFAULT 'PENDIENTE';
