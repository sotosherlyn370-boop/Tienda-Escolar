# gobernanza.py: Práctica 9. Directivas, línea base de seguridad e identidad
import json
import re

recursos = [
    {"nombre": "prod-web-ventas", "region": "us-east", "cifrado": True, "publico": True,
     "etiquetas": {"responsable": "ana", "centro_costo": "ventas", "entorno": "prod"}},
    {"nombre": "prod-db-ventas", "region": "us-east", "cifrado": True, "publico": False,
     "etiquetas": {"responsable": "ana", "centro_costo": "ventas", "entorno": "prod"}},
    {"nombre": "MiBaseDePruebas", "region": "asia-sur", "cifrado": False, "publico": True,
     "etiquetas": {"responsable": "luis"}},
]
usuarios = [
    {"nombre": "ana", "mfa": True, "rol": "propietario"},
    {"nombre": "luis", "mfa": False, "rol": "colaborador"},
    {"nombre": "compartida-ti", "mfa": False, "rol": "propietario"},
]

ETIQUETAS_OBLIGATORIAS = {"responsable", "centro_costo", "entorno"}
REGIONES_PERMITIDAS = {"us-east", "us-west"}
PATRON_NOMBRE = re.compile(r"^(dev|test|prod)-[a-z]+-[a-z0-9]+$")

# Cada directiva devuelve True si el recurso CUMPLE
def nombre_valido(r):
    return bool(PATRON_NOMBRE.match(r["nombre"]))

def etiquetas_completas(r):
    return ETIQUETAS_OBLIGATORIAS <= set(r["etiquetas"])

def region_permitida(r):
    return r["region"] in REGIONES_PERMITIDAS

def sin_acceso_publico(r):
    return (not r["publico"]) or "-web-" in r["nombre"] # solo la web es pública

directivas_recursos = {
    "Coherencia: nombre entorno-tipo-proyecto": nombre_valido,
    "Coherencia: etiquetas obligatorias": etiquetas_completas,
    "Costos: región permitida": region_permitida,
    "Seguridad: cifrado activado": lambda r: r["cifrado"],
    "Seguridad: sin acceso público (salvo web)": sin_acceso_publico,
}
directivas_identidad = {
    "Identidad: MFA activado": lambda u: u["mfa"],
    "Identidad: no usar cuentas compartidas": lambda u: not u["nombre"].startswith("compartida"),
}

incumplimientos = []
for r in recursos:
    for nombre, regla in directivas_recursos.items():
        if not regla(r):
            incumplimientos.append({"objeto": r["nombre"], "directiva": nombre})

for u in usuarios:
    for nombre, regla in directivas_identidad.items():
        if not regla(u):
            incumplimientos.append({"objeto": u["nombre"], "directiva": nombre})

propietarios = [u["nombre"] for u in usuarios if u["rol"] == "propietario"]
if len(propietarios) > 1:
    incumplimientos.append({"objeto": ", ".join(propietarios),
                            "directiva": "Identidad: mínimo privilegio (1 propietario)"})

total = (len(recursos) * len(directivas_recursos)
         + len(usuarios) * len(directivas_identidad) + 1)
print(f"Revisiones: {total} | Incumplimientos: {len(incumplimientos)}")
for i in incumplimientos:
    print(f" [X] {i['objeto']}: {i['directiva']}")
cumplen = total - len(incumplimientos)
print(f"Nivel de cumplimiento: {100 * cumplen / total:.0f} %")

with open("reporte_gobernanza.json", "w", encoding="utf-8") as f:
    json.dump(incumplimientos, f, indent=2, ensure_ascii=False)