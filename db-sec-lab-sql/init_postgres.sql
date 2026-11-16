CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50),
    email VARCHAR(100)
);
INSERT INTO usuarios (nombre, email) VALUES ('admin', 'admin_pg@tienda.com'), ('juan', 'juan@tienda.com');

-- 🛡️ Defensa: RBAC
CREATE ROLE appuser LOGIN PASSWORD 'FuertePG#2026';
GRANT CONNECT ON DATABASE postgres TO appuser;
GRANT USAGE ON SCHEMA public TO appuser;
GRANT SELECT, INSERT ON usuarios TO appuser;

-- 🛡️ Fase 4: Auditoría PostgreSQL
ALTER SYSTEM SET log_connections = 'on';
ALTER SYSTEM SET log_disconnections = 'on';
ALTER SYSTEM SET log_statement = 'all';
SELECT pg_reload_conf();
