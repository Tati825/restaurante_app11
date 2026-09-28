class Usuario:
    def __init__(self, id, nombre, usuario, password):
        self.id = id
        self.nombre = nombre
        self.usuario = usuario
        self.password = password

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "password": self.password
        }

    @classmethod
    def from_dict(cls, datos):
        return cls(
            datos["id"],
            datos["nombre"],
            datos["usuario"],
            datos["password"]
        )

    def __str__(self):
        return f"{self.nombre} ({self.usuario})"
