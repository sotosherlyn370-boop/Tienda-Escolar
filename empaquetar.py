# empaquetar.py: Práctica 5. Archivos de implementación y lista de verificación
from pathlib import Path

archivos = {
    "Dockerfile": """FROM python:3.12-slim
WORKDIR /app
COPY . .
ENV PORT=8000
EXPOSE 8000
CMD ["python", "app.py"]
""",
    "Procfile": "web: python app.py\n",
    "requirements.txt": "# Solo biblioteca estándar\n",
    ".env.example": "PORT=8000\nAPP_NOMBRE=Mi app en la nube\nENTORNO=produccion\n",
    ".gitignore": ".env\n__pycache__/\n*.db\n*.log\n",
}

for nombre, contenido in archivos.items():
    Path(nombre).write_text(contenido, encoding="utf-8")
    print(f"Creado: {nombre}")

# Lista de verificación previa al despliegue
requeridos = ["app.py", "test_app.py", "Dockerfile", "Procfile", "requirements.txt", ".env.example"]
print("\nVerificación previa al despliegue:")
faltan = [f for f in requeridos if not Path(f).exists()]
for f in requeridos:
    print(f" [{'OK' if f not in faltan else 'FALTA'}] {f}")
print("\nListo para desplegar" if not faltan else f"\nFaltan archivos: {faltan}")

# El secreto real nunca se sube al repositorio
assert ".env" in archivos[".gitignore"], ".env debe estar en .gitignore"