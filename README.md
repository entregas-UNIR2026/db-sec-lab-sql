# Laboratorio de Seguridad en Bases de Datos (PostgreSQL y MySQL)

Repositorio con la infraestructura como código (Docker Compose), scripts de aprovisionamiento SQL, certificados TLS y aplicación cliente en Python 3.11 (versión vulnerable y versión bastionada).

## 1. Estructura del Repositorio

- docker-compose.yml: Orquestación de servicios (red interna aislada y variables .env)
- .env: Secretos y credenciales robustas de administración y aplicación
- certs/: Certificados X.509 autofirmados para cifrado en tránsito (TLS)
- app/vulnerable.py: Script inseguro (concatenación SQL y credenciales en claro)
- app/seguro.py: Script bastionado (consultas parametrizadas y variables de entorno)
- app/requirements.txt: Dependencias (psycopg2-binary, pymysql, cryptography)
- init_postgres.sql: Esquema inicial, RBAC (appuser) y auditoría en PostgreSQL 15
- init_mysql.sql: Esquema inicial, RBAC (app) y auditoría en MySQL 8
- backup_mysql.sql: Volcado lógico de respaldo de MySQL (Fase 6)
- README.md: Guía de despliegue y verificación paso a paso

## 2. Requisitos Previos
- Docker Engine y Docker Compose
- OpenSSL

## 3. Guía de Reproducción Paso a Paso

### 3.1 Despliegue del Entorno Bastionado (Fase 3)
1. Situarse en el directorio del proyecto:
   cd ~/db-sec-lab-sql
2. Levantar los contenedores en segundo plano:
   sudo docker-compose up -d
3. Verificar la mitigación del ataque de Inyección SQL mediante consultas parametrizadas:
   sudo docker-compose logs --tail=15 app

### 3.2 Verificación de Auditoría / Logging (Fase 4)
- PostgreSQL (registro de conexiones autorizadas con appuser):
  sudo docker-compose logs postgres | grep "connection authorized"
- MySQL (consulta a la tabla de auditoría mysql.general_log):
  sudo docker-compose exec mysql mysql -u root -p'RootFuerte#2026' -e "SELECT event_time, user_host, argument FROM mysql.general_log WHERE argument LIKE '%SELECT%' LIMIT 5;"

### 3.3 Configuración y Verificación de TLSv1.3 (Fases 4 y 7)
1. Copiar los certificados autofirmados al contenedor de PostgreSQL y ajustar permisos:
   sudo docker cp certs/server.key db-sec-lab-sql_postgres_1:/var/lib/postgresql/data/server.key
   sudo docker cp certs/server.crt db-sec-lab-sql_postgres_1:/var/lib/postgresql/data/server.crt
   sudo docker exec -it --user root db-sec-lab-sql_postgres_1 chown postgres:postgres /var/lib/postgresql/data/server.key /var/lib/postgresql/data/server.crt
2. Habilitar SSL en el motor y reiniciar el servicio:
   sudo docker-compose exec -e PGPASSWORD='AdminFuerte#2026' postgres psql -U postgres -d postgres -c "ALTER SYSTEM SET ssl = 'on';"
   sudo docker-compose exec -e PGPASSWORD='AdminFuerte#2026' postgres psql -U postgres -d postgres -c "ALTER SYSTEM SET ssl_cert_file = 'server.crt';"
   sudo docker-compose exec -e PGPASSWORD='AdminFuerte#2026' postgres psql -U postgres -d postgres -c "ALTER SYSTEM SET ssl_key_file = 'server.key';"
   sudo docker-compose restart postgres
3. Verificar la negociación TLSv1.3:
   sudo docker-compose exec -e PGPASSWORD='AdminFuerte#2026' postgres psql -h localhost -U postgres -d postgres -c "\conninfo"

### 3.4 Cifrado en Reposo con pgcrypto (Fase 5)
   sudo docker-compose exec -e PGPASSWORD='AdminFuerte#2026' postgres psql -U postgres -d postgres -c "CREATE EXTENSION IF NOT EXISTS pgcrypto;"
   sudo docker-compose exec -e PGPASSWORD='AdminFuerte#2026' postgres psql -U postgres -d postgres -c "ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS email_enc BYTEA;"
   sudo docker-compose exec -e PGPASSWORD='AdminFuerte#2026' postgres psql -U postgres -d postgres -c "UPDATE usuarios SET email_enc = pgp_sym_encrypt(email, 'PassCifrado#2026');"
   sudo docker-compose exec -e PGPASSWORD='AdminFuerte#2026' postgres psql -U postgres -d postgres -c "SELECT id, nombre, pgp_sym_decrypt(email_enc, 'PassCifrado#2026') AS email_descifrado FROM usuarios;"

### 3.5 Backups y Restauración (Fase 6)
   sudo docker-compose exec -e PGPASSWORD='AdminFuerte#2026' postgres pg_dump -U postgres -F c -f /tmp/backup_pg.dump postgres
   sudo docker-compose exec -e MYSQL_PWD='RootFuerte#2026' mysql mysqldump -u root tienda > backup_mysql.sql
   sudo docker-compose exec -e PGPASSWORD='AdminFuerte#2026' postgres psql -U postgres -d postgres -c "DELETE FROM usuarios WHERE nombre='juan';"
   sudo docker-compose exec -e PGPASSWORD='AdminFuerte#2026' postgres pg_restore -U postgres -d postgres -1 --clean /tmp/backup_pg.dump
   sudo docker-compose exec -e PGPASSWORD='AdminFuerte#2026' postgres psql -U postgres -d postgres -c "SELECT nombre FROM usuarios;"
