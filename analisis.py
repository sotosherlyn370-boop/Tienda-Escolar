# analisis.py: Práctica 1. Modelos de servicio y análisis
capas = ["Aplicación", "Datos", "Entorno de ejecución", "Sistema operativo", "Servidores y red"]
# Cuántas capas (de arriba abajo) administra el CLIENTE en cada modelo
administra_cliente = {"IaaS": 4, "PaaS": 2, "SaaS": 0}

print(f"{'Capa':<22}" + "".join(f"{m:^11}" for m in administra_cliente))
for i, capa in enumerate(capas):
    fila = "".join(f"{('Tú' if i < n else 'Proveedor'):^11}" for n in administra_cliente.values())
    print(f"{capa:<22}{fila}")

def recomendar(necesita_controlar_so, desarrolla_su_codigo):
    """Análisis: ¿qué modelo de servicio conviene?"""
    if not desarrolla_su_codigo:
        return "SaaS" # solo usar un software ya hecho
    if necesita_controlar_so:
        return "IaaS" # máquinas virtuales a tu medida
    return "PaaS" # publicas tu código y el proveedor hace el resto

proyectos = [
    ("Correo y ofimática para la escuela", False, False),
    ("Tienda en línea desarrollada por el equipo", False, True),
    ("Sistema heredado que exige un sistema operativo específico", True, True),
]

print()
for nombre, so, codigo in proyectos:
    print(f"{nombre:<60} -> {recomendar(so, codigo)}")