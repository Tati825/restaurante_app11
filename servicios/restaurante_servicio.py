from datetime import datetime
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio

class RestauranteServicio:
    def __init__(self):
        self.productos_archivo = ArchivoServicio(
            "datos/productos.json"
        )

        self.usuarios_archivo = ArchivoServicio(
            "datos/usuarios.json"
        )

        self.ventas_archivo = ArchivoServicio(
            "datos/ventas.json"
        )

        self.productos = []
        self.usuarios = []
        self.ventas = []

        self.cargar_datos()

    def cargar_datos(self):
        productos_data = self.productos_archivo.cargar()
        usuarios_data = self.usuarios_archivo.cargar()
        ventas_data = self.ventas_archivo.cargar()

        self.productos = [
            Producto.from_dict(producto)
            for producto in productos_data
        ]

        self.usuarios = [
            Usuario.from_dict(usuario)
            for usuario in usuarios_data
        ]

        self.ventas = [
            Venta.from_dict(venta)
            for venta in ventas_data
        ]

    def autenticar_usuario(self, usuario, password):
        for usuario_obj in self.usuarios:
            if (
                usuario_obj.usuario == usuario
                and usuario_obj.password == password
            ):
                return usuario_obj

        return None

    def obtener_productos(self):
        return self.productos

    def agregar_producto(self, nombre, precio, categoria):
        if not nombre.strip():
            return False, "El nombre del producto es obligatorio"

        try:
            precio = float(precio)
        except ValueError:
            return False, "El precio debe ser numérico"

        if precio <= 0:
            return False, "El precio debe ser mayor que cero"

        nuevo_id = 1

        if self.productos:
            nuevo_id = max(
                producto.id for producto in self.productos
            ) + 1

        producto = Producto(
            nuevo_id,
            nombre.strip(),
            precio,
            categoria.strip()
        )

        self.productos.append(producto)

        self.productos_archivo.guardar(
            [producto.to_dict() for producto in self.productos]
        )

        return True, "Producto registrado correctamente."

    def obtener_usuarios(self):
        return self.usuarios

    def obtener_ventas(self):
        return self.ventas

    def registrar_venta(self, usuario_id, producto_id):

        # Validar usuario
        usuario = next(
            (
                usuario
                for usuario in self.usuarios
                if usuario.id == usuario_id
            ),
            None
        )

        if usuario is None:
            return False, "El usuario seleccionado no existe"

        # Validar producto
        producto = next(
            (
                producto
                for producto in self.productos
                if producto.id == producto_id
            ),
            None
        )

        if producto is None:
            return False, "El producto seleccionado no existe"

        # Generar ID
        nuevo_id = 1

        if self.ventas:
            nuevo_id = max(
                venta.id for venta in self.ventas
            ) + 1

        # Fecha y hora
        fecha = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        nueva_venta = Venta(
            nuevo_id,
            usuario.id,
            producto.id,
            fecha
        )

        self.ventas.append(nueva_venta)

        self.ventas_archivo.guardar(
            [venta.to_dict() for venta in self.ventas]
        )

        return True, "Venta registrada correctamente"

    def obtener_ventas_detalladas(self):
        resultado = []

        for venta in self.ventas:

            usuario = next(
                (
                    usuario
                    for usuario in self.usuarios
                    if usuario.id == venta.usuario_id
                ),
                None
            )

            producto = next(
                (
                    producto
                    for producto in self.productos
                    if producto.id == venta.producto_id
                ),
                None
            )

            resultado.append({
                "id": venta.id,
                "usuario": (
                    usuario.nombre
                    if usuario
                    else "Usuario desconocido"
                ),
                "producto": (
                    producto.nombre
                    if producto
                    else "Producto desconocido"
                ),
                "fecha": venta.fecha
            })

        return resultado
