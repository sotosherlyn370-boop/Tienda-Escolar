# costos.py: Práctica 8. Administración de costos con presupuesto y alertas
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# PRECIOS FICTICIOS: sustitúyelos con los de la calculadora de tu proveedor
HORAS_MES = 730
recursos = [
    # nombre, precio por hora (USD), horas de uso al mes, entorno
    ("app-web", 0.020, HORAS_MES, "produccion"),
    ("base-de-datos", 0.035, HORAS_MES, "produccion"),
    ("app-web-pruebas", 0.020, HORAS_MES, "desarrollo"),
    ("almacenamiento", 0.005, HORAS_MES, "produccion"),
    ("balanceador", 0.025, HORAS_MES, "produccion"),
]
PRESUPUESTO = 90.0 # USD al mes

costos = {nombre: precio * horas for nombre, precio, horas, _ in recursos}
total = sum(costos.values())
print(f"{'Recurso':<18}{'USD/mes':>10}")
for nombre, c in costos.items():
    print(f"{nombre:<18}{c:>10.2f}")
print(f"{'TOTAL':<18}{total:>10.2f} (presupuesto {PRESUPUESTO:.2f})")

uso = total / PRESUPUESTO
if uso >= 1:
    print("ALERTA CRÍTICA: se superó el presupuesto")
elif uso >= 0.8:
    print(f"ALERTA: se ha consumido el {uso:.0%} del presupuesto")
else:
    print(f"Dentro del presupuesto ({uso:.0%})")

# Directiva de control de costos: apagar desarrollo fuera de horario (8 h x 22 días)
horas_apagado = 8 * 22
ahorro = sum(p * (h - horas_apagado) for _, p, h, e in recursos if e == "desarrollo")
print(f"Directiva 'apagar desarrollo fuera de horario' -> ahorro: {ahorro:.2f} USD/mes")

colores = ["#2E7DD1" if e == "produccion" else "#FF8A3D" for *_, e in recursos]
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(costos.keys(), costos.values(), color=colores)
ax.axhline(PRESUPUESTO / len(recursos), color="#E5484D", linestyle="--",
           label="Promedio permitido por recurso")
ax.set_title(f"Costo mensual por recurso (total {total:.2f} USD)")
ax.set_ylabel("USD al mes")
plt.setp(ax.get_xticklabels(), rotation=20, ha="right")
ax.legend()
fig.tight_layout()
fig.savefig("reporte_costos.png", dpi=150)
print("Gráfica guardada: reporte_costos.png")