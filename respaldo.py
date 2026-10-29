# respaldo.py: Práctica 6. Copia de seguridad y registro de transacciones
import json
import os
import shutil
import sqlite3

DB, RESPALDO, BITACORA = "pedidos.db", "respaldo.db", "transacciones.log"

for archivo in (DB, RESPALDO, BITACORA):
    if os.path.exists(archivo):
        os.remove(archivo)

def conectar():
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS pedidos "
                "(id INTEGER PRIMARY KEY, cliente TEXT, monto REAL)")
    return con

def registrar(con, cliente, monto):
    cur = con.execute("INSERT INTO pedidos (cliente, monto) VALUES (?, ?)", (cliente, monto))
    con.commit()
    # Registro de transacciones: una línea por cada operación
    with open(BITACORA, "a", encoding="utf-8") as f:
        f.write(json.dumps({"id": cur.lastrowid, "cliente": cliente, "monto": monto}) + "\n")

def total(con):
    return con.execute("SELECT COUNT(*), COALESCE(SUM(monto), 0) FROM pedidos").fetchone()

con = conectar()
for cliente, monto in [("Ana", 500), ("Luis", 750), ("Marta", 300)]:
    registrar(con, cliente, monto)

# 1) Copia de seguridad completa
destino = sqlite3.connect(RESPALDO)
con.backup(destino)
destino.close()
print("Respaldo hecho. Pedidos y total:", total(con))

# 2) Siguen llegando pedidos DESPUÉS del respaldo
for cliente, monto in [("Pedro", 900), ("Sofía", 120)]:
    registrar(con, cliente, monto)
print("Antes del desastre:", total(con))

# 3) Desastre: se pierde la base de datos
con.close()
os.remove(DB)
print("¡Base de datos perdida!")

# 4) Restauración: respaldo + repetir el registro de transacciones
shutil.copy(RESPALDO, DB)
con = conectar()
ultimo_id = con.execute("SELECT COALESCE(MAX(id), 0) FROM pedidos").fetchone()[0]
with open(BITACORA, encoding="utf-8") as f:
    for linea in f:
        t = json.loads(linea)
        if t["id"] > ultimo_id:
            con.execute("INSERT INTO pedidos (id, cliente, monto) VALUES (?, ?, ?)",
                        (t["id"], t["cliente"], t["monto"]))
con.commit()
print("Después de restaurar:", total(con))