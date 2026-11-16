import psycopg2, pymysql, time, sys, os

print("Iniciando aplicación SEGURA...")
time.sleep(10) # Espera a que levanten BBDD

try:
    # 🛡️ Defensa: Conexión con usuarios RBAC desde el entorno
    pg = psycopg2.connect(host="postgres", dbname="postgres", 
                          user=os.getenv("PG_APP_USER"), password=os.getenv("PG_APP_PASS"))
    my = pymysql.connect(host="mysql", database="tienda", autocommit=True,
                         user=os.getenv("MY_APP_USER"), password=os.getenv("MY_APP_PASS"))
    
    # Intento de ataque
    nombre_malicioso = "admin' OR '1'='1" 
    
    # 🛡️ Defensa: Parametrización (%s en vez de f-strings)
    print(f"\n[POSTGRESQL] Previniendo SQLi. Buscando usuario literal: {nombre_malicioso}")
    cur_pg = pg.cursor()
    cur_pg.execute("SELECT id,nombre FROM usuarios WHERE nombre=%s;", (nombre_malicioso,))
    res_pg = cur_pg.fetchall()
    print("RESULTADO:", res_pg if res_pg else "Usuario no encontrado (Ataque mitigado)")

    print(f"\n[MYSQL] Previniendo SQLi. Buscando usuario literal: {nombre_malicioso}")
    cur_my = my.cursor()
    cur_my.execute("SELECT id,nombre FROM usuarios WHERE nombre=%s;", (nombre_malicioso,))
    res_my = cur_my.fetchall()
    print("RESULTADO:", res_my if res_my else "Usuario no encontrado (Ataque mitigado)")

    while True:
        time.sleep(60)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
