class Producto:
    def __init__(self, id, nombre, precio, categoria):
        self.id = id
        self.nombre = nombre
        self.precio = float(precio)
        self.categoria = categoria

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "categoria": self.categoria
        }

    @classmethod
    def from_dict(cls, datos):
        return cls(
            datos["id"],
            datos["nombre"],
            datos["precio"],
            datos["categoria"]
        )

    def __str__(self):
        return f"{self.nombre} - ${self.precio:.2f}"
