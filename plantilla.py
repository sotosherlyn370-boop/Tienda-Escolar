# plantilla.py: Práctica 10. Aceleración de la implementación con plantillas
import json
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PLANTILLA = {
    "recursos": [
        {"tipo": "web", "tamano": "pequeno", "cifrado": True},
        {"tipo": "db", "tamano": "pequeno", "cifrado": True},
        {"tipo": "almacenamiento", "tamano": "pequeno", "cifrado": True},
    ],
    "etiquetas": {"responsable": "equipo-1", "centro_costo": "escuela"},
}

def crear_entorno(entorno, proyecto="tienda", tamano="pequeno"):
    """Genera un entorno COMPLETO y coherente a partir de la misma plantilla."""
    recursos = []
    for r in PLANTILLA["recursos"]:
        recursos.append({**r, "tamano": tamano,
                         "nombre": f"{entorno}-{r['tipo']}-{proyecto}",
                         "etiquetas": {**PLANTILLA["etiquetas"], "entorno": entorno}})
    return recursos

t0 = time.perf_counter()
entornos = {"dev": crear_entorno("dev"),
            "test": crear_entorno("test"),
            "prod": crear_entorno("prod", tamano="mediano")}
segundos_plantilla = time.perf_counter() - t0

with open("entornos.json", "w", encoding="utf-8") as f:
    json.dump(entornos, f, indent=2, ensure_ascii=False)
for nombre, recursos in entornos.items():
    print(nombre, "->", [r["nombre"] for r in recursos])

# Comparación: creación manual (supuesto editable) vs plantilla
MINUTOS_POR_RECURSO = 15 # supuesto: cada recurso se crea a mano desde el portal
n_recursos = sum(len(v) for v in entornos.values())
minutos_manual = n_recursos * MINUTOS_POR_RECURSO
print(f"\nManual: {minutos_manual} min | Plantilla: {segundos_plantilla * 1000:.2f} ms "
      f"({n_recursos} recursos)")

fig, ax = plt.subplots(figsize=(6, 4))
barras = ax.bar(["Manual", "Con plantilla"], [minutos_manual, segundos_plantilla / 60],
                color=["#FF8A3D", "#2E7DD1"])
ax.bar_label(barras, fmt="%.4g min")
ax.set_ylabel("Minutos")
ax.set_title(f"Tiempo para crear {len(entornos)} entornos ({n_recursos} recursos)")
fig.tight_layout()
fig.savefig("reporte_aceleracion.png", dpi=150)
print("Gráfica guardada: reporte_aceleracion.png")