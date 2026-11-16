CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    email VARCHAR(100)
);
INSERT INTO usuarios (nombre, email) VALUES ('admin', 'admin_my@tienda.com'), ('maria', 'maria@tienda.com');

-- 🛡️ Defensa: RBAC
CREATE USER 'app'@'%' IDENTIFIED BY 'FuerteMY#2026';
GRANT SELECT, INSERT ON tienda.usuarios TO 'app'@'%';
FLUSH PRIVILEGES;

-- 🛡️ Fase 4: Auditoría MySQL
SET GLOBAL general_log = 'ON';
SET GLOBAL log_output = 'TABLE';
