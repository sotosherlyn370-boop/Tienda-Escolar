# monitor.py: Práctica 7. Monitoreo de disponibilidad y latencia (reporte gráfico)
import os
import threading
import time
import urllib.request
from http.server import ThreadingHTTPServer
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

URL = os.environ.get("URL_APP") # si no se define, se usa una app local
MUESTRAS = int(os.environ.get("MUESTRAS", "30"))
INTERVALO = float(os.environ.get("INTERVALO", "0.3")) # segundos entre sondeos

if not URL:
    import app # el app.py de la Práctica 3
    servidor = ThreadingHTTPServer(("127.0.0.1", 0), app.Handler)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    URL = f"http://127.0.0.1:{servidor.server_address[1]}"

print("Monitoreando:", URL)
latencias, estados = [], []
for _ in range(MUESTRAS):
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(URL + "/health", timeout=10) as r:
            ok = r.status == 200
    except Exception:
        ok = False
    latencias.append((time.perf_counter() - t0) * 1000)
    estados.append(ok)
    time.sleep(INTERVALO)

disponibilidad = 100 * sum(estados) / len(estados)
ordenadas = sorted(latencias)
p95 = ordenadas[int(0.95 * (len(ordenadas) - 1))]
promedio = sum(latencias) / len(latencias)
print(f"Disponibilidad: {disponibilidad:.1f} %")
print(f"Latencia promedio: {promedio:.1f} ms | p95: {p95:.1f} ms")

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(range(1, MUESTRAS + 1), latencias, marker="o", color="#2E7DD1", label="Latencia")
ax.axhline(promedio, color="#FF8A3D", linestyle="--", label=f"Promedio {promedio:.1f} ms")
for i, ok in enumerate(estados, start=1):
    if not ok:
        ax.axvline(i, color="#E5484D", alpha=0.4) # marca las caídas
ax.set_title(f"Monitoreo de /health: disponibilidad {disponibilidad:.1f} %")
ax.set_xlabel("Número de sondeo")
ax.set_ylabel("Latencia (ms)")
ax.legend()
fig.tight_layout()
fig.savefig("reporte_monitoreo.png", dpi=150)
print("Gráfica guardada: reporte_monitoreo.png")