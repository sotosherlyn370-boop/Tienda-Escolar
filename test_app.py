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