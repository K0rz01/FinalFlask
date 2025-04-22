-- Asegurarnos de que los usuarios existentes en la tabla user permanezcan
INSERT IGNORE INTO user (email, password, name, rol, estado)
VALUES 
('admin@tecnocomputer.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN.jvXjvFPZGV1LF0Tt1e', 'Administrador', 'tecnico', 'activo'),
('cliente@tecnocomputer.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN.jvXjvFPZGV1LF0Tt1e', 'Cliente Demo', 'cliente', 'activo'),
('tecnico@tecnocomputer.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN.jvXjvFPZGV1LF0Tt1e', 'Técnico Demo', 'tecnico', 'activo');

-- Nota: La contraseña hasheada corresponde a "password123" para todos los usuarios 