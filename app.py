# app.py (versión 2): Práctica 3. Estado de salud y registros en formato JSON
import json
import logging
import os
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORT", "8000"))
NOMBRE = os.environ.get("APP_NOMBRE", "Mi app en la nube")
ENTORNO = os.environ.get("ENTORNO", "desarrollo")
INICIO = time.time()

# Los registros salen por la salida estándar; la plataforma los recolecta
logging.basicConfig(level=logging.INFO, format="%(message)s")

def log(evento, **datos):
    registro = {"ts": round(time.time(), 3), "evento": evento, **datos}
    logging.info(json.dumps(registro, ensure_ascii=False))

class Handler(BaseHTTPRequestHandler):
    def responder(self, codigo, cuerpo, tipo="application/json"):
        datos = cuerpo.encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", f"{tipo}; charset=utf-8")
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)

    def do_GET(self):
        t0 = time.perf_counter()
        if self.path == "/":
            self.responder(200, f"<h1>{NOMBRE}</h1><p>Entorno: {ENTORNO}</p>", "text/html")
        elif self.path == "/health":
            estado = {"estado": "ok", "uptime_s": round(time.time() - INICIO, 1)}
            self.responder(200, json.dumps(estado))
        else:
            self.responder(404, json.dumps({"error": "no encontrado"}))
        log("peticion", ruta=self.path, ms=round((time.perf_counter() - t0) * 1000, 2))

    def log_message(self, *args):
        pass # silenciamos el log por defecto; usamos el nuestro

if __name__ == "__main__":
    log("inicio", puerto=PORT, entorno=ENTORNO)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()

# test_app.py: Práctica 4. Pruebas automatizadas antes de desplegar
import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
import app # el app.py de la Práctica 3

class PruebasApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Puerto 0: el sistema elige uno libre
        cls.servidor = ThreadingHTTPServer(("127.0.0.1", 0), app.Handler)
        cls.base = f"http://127.0.0.1:{cls.servidor.server_address[1]}"
        threading.Thread(target=cls.servidor.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.servidor.shutdown()
        cls.servidor.server_close()

    def test_inicio_responde_200(self):
        with urllib.request.urlopen(self.base + "/") as r:
            self.assertEqual(r.status, 200)
            self.assertIn(app.NOMBRE, r.read().decode("utf-8"))

    def test_health_devuelve_ok(self):
        with urllib.request.urlopen(self.base + "/health") as r:
            datos = json.loads(r.read())
            self.assertEqual(datos["estado"], "ok")

    def test_ruta_inexistente_devuelve_404(self):
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(self.base + "/no-existe")
        self.assertEqual(ctx.exception.code, 404)

if __name__ == "__main__":
    unittest.main(verbosity=2)