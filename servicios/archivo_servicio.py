import json
import os

class ArchivoServicio:
    def __init__(self, ruta):
        self.ruta = ruta

    def cargar(self):
        if not os.path.exists(self.ruta):
            return []

        try:
            with open(self.ruta, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def guardar(self, datos):
        directorio = os.path.dirname(self.ruta)

        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)

        with open(self.ruta, "w", encoding="utf-8") as archivo:
            json.dump(
                datos,
                archivo,
                indent=4,
                ensure_ascii=False
            )
