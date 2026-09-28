import tkinter as tk
from tkinter import ttk, messagebox
import os

class MainView(ttk.Frame):

    def __init__(
        self,
        parent,
        restaurante_servicio,
        usuario_actual,
        on_logout
    ):
        super().__init__(parent)

        self.restaurante_servicio = restaurante_servicio
        self.usuario_actual = usuario_actual
        self.on_logout = on_logout

        self.configure(padding=15)

        self.crear_interfaz()

        self.cargar_productos()
        self.cargar_usuarios()
        self.cargar_ventas()

    def crear_interfaz(self):

        header = ttk.Frame(self)
        header.pack(
            fill="x",
            pady=(0, 15)
        )

        logo_path = "assets/logo.png"

        if os.path.exists(logo_path):

            try:
                self.logo = tk.PhotoImage(
                    file=logo_path
                )

                ttk.Label(
                    header,
                    image=self.logo
                ).pack(
                    side="left",
                    padx=(0, 15)
                )

            except tk.TclError:
                pass

        titulo_frame = ttk.Frame(header)
        titulo_frame.pack(
            side="left",
            fill="x",
            expand=True
        )

        ttk.Label(
            titulo_frame,
            text="Restaurante App",
            font=("Arial", 20, "bold")
        ).pack(
            anchor="w"
        )

        ttk.Label(
            titulo_frame,
            text=f"Sesión: {self.usuario_actual.nombre}"
        ).pack(
            anchor="w"
        )

        ttk.Button(
            header,
            text="Cerrar sesión",
            command=self.cerrar_sesion
        ).pack(
            side="right"
        )

        self.notebook = ttk.Notebook(self)

        self.notebook.pack(
            fill="both",
            expand=True
        )

        self.productos_tab = ttk.Frame(
            self.notebook,
            padding=15
        )

        self.usuarios_tab = ttk.Frame(
            self.notebook,
            padding=15
        )

        self.ventas_tab = ttk.Frame(
            self.notebook,
            padding=15
        )

        self.notebook.add(
            self.productos_tab,
            text="Productos"
        )

        self.notebook.add(
            self.usuarios_tab,
            text="Usuarios"
        )

        self.notebook.add(
            self.ventas_tab,
            text="Ventas"
        )

        self.crear_productos_tab()
        self.crear_usuarios_tab()
        self.crear_ventas_tab()

    def crear_productos_tab(self):

        ttk.Label(
            self.productos_tab,
            text="Gestión de productos",
            font=("Arial", 16, "bold")
        ).pack(
            anchor="w",
            pady=(0, 15)
        )

        formulario = ttk.LabelFrame(
            self.productos_tab,
            text="Nuevo producto",
            padding=15
        )

        formulario.pack(
            fill="x",
            pady=(0, 15)
        )

        ttk.Label(
            formulario,
            text="Nombre:"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.producto_nombre = ttk.Entry(
            formulario,
            width=25
        )

        self.producto_nombre.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Label(
            formulario,
            text="Precio:"
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=5
        )

        self.producto_precio = ttk.Entry(
            formulario,
            width=12
        )

        self.producto_precio.grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )

        ttk.Label(
            formulario,
            text="Categoría:"
        ).grid(
            row=0,
            column=4,
            padx=5,
            pady=5
        )

        self.producto_categoria = ttk.Entry(
            formulario,
            width=20
        )

        self.producto_categoria.grid(
            row=0,
            column=5,
            padx=5,
            pady=5
        )

        ttk.Button(
            formulario,
            text="Agregar producto",
            command=self.agregar_producto
        ).grid(
            row=0,
            column=6,
            padx=10,
            pady=5
        )

        columnas = (
            "id",
            "nombre",
            "precio",
            "categoria"
        )

        self.productos_tree = ttk.Treeview(
            self.productos_tab,
            columns=columnas,
            show="headings"
        )

        self.productos_tree.heading(
            "id",
            text="ID"
        )

        self.productos_tree.heading(
            "nombre",
            text="Producto"
        )

        self.productos_tree.heading(
            "precio",
            text="Precio"
        )

        self.productos_tree.heading(
            "categoria",
            text="Categoría"
        )

        self.productos_tree.column(
            "id",
            width=60,
            anchor="center"
        )

        self.productos_tree.column(
            "nombre",
            width=250
        )

        self.productos_tree.column(
            "precio",
            width=100,
            anchor="center"
        )

        self.productos_tree.column(
            "categoria",
            width=180
        )

        self.productos_tree.pack(
            fill="both",
            expand=True
        )

    def cargar_productos(self):

        for item in self.productos_tree.get_children():
            self.productos_tree.delete(item)

        productos = self.restaurante_servicio.obtener_productos()

        for producto in productos:

            self.productos_tree.insert(
                "",
                "end",
                values=(
                    producto.id,
                    producto.nombre,
                    f"${producto.precio:.2f}",
                    producto.categoria
                )
            )

    def agregar_producto(self):

        nombre = self.producto_nombre.get()
        precio = self.producto_precio.get()
        categoria = self.producto_categoria.get()

        correcto, mensaje = (
            self.restaurante_servicio.agregar_producto(
                nombre,
                precio,
                categoria
            )
        )

        if correcto:

            messagebox.showinfo(
                "Producto",
                mensaje
            )

            self.producto_nombre.delete(0, tk.END)
            self.producto_precio.delete(0, tk.END)
            self.producto_categoria.delete(0, tk.END)

            self.cargar_productos()
            self.actualizar_combo_productos()

        else:

            messagebox.showerror(
                "Error",
                mensaje
            )

    def crear_usuarios_tab(self):

        ttk.Label(
            self.usuarios_tab,
            text="Usuarios registrados",
            font=("Arial", 16, "bold")
        ).pack(
            anchor="w",
            pady=(0, 15)
        )

        columnas = (
            "id",
            "nombre",
            "usuario"
        )

        self.usuarios_tree = ttk.Treeview(
            self.usuarios_tab,
            columns=columnas,
            show="headings"
        )

        self.usuarios_tree.heading(
            "id",
            text="ID"
        )

        self.usuarios_tree.heading(
            "nombre",
            text="Nombre"
        )

        self.usuarios_tree.heading(
            "usuario",
            text="Usuario"
        )

        self.usuarios_tree.column(
            "id",
            width=70,
            anchor="center"
        )

        self.usuarios_tree.column(
            "nombre",
            width=250
        )

        self.usuarios_tree.column(
            "usuario",
            width=200
        )

        self.usuarios_tree.pack(
            fill="both",
            expand=True
        )

    def cargar_usuarios(self):

        for item in self.usuarios_tree.get_children():
            self.usuarios_tree.delete(item)

        usuarios = self.restaurante_servicio.obtener_usuarios()

        for usuario in usuarios:

            self.usuarios_tree.insert(
                "",
                "end",
                values=(
                    usuario.id,
                    usuario.nombre,
                    usuario.usuario
                )
            )

    def crear_ventas_tab(self):

        ttk.Label(
            self.ventas_tab,
            text="Registro de ventas",
            font=("Arial", 16, "bold")
        ).pack(
            anchor="w",
            pady=(0, 15)
        )

        formulario = ttk.LabelFrame(
            self.ventas_tab,
            text="Registrar nueva venta",
            padding=15
        )

        formulario.pack(
            fill="x",
            pady=(0, 15)
        )

        ttk.Label(
            formulario,
            text="Usuario:"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.usuario_combo = ttk.Combobox(
            formulario,
            state="readonly",
            width=30
        )

        self.usuario_combo.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Label(
            formulario,
            text="Producto:"
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=5
        )

        self.producto_combo = ttk.Combobox(
            formulario,
            state="readonly",
            width=30
        )

        self.producto_combo.grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )

        ttk.Button(
            formulario,
            text="Registrar venta",
            command=self.registrar_venta
        ).grid(
            row=0,
            column=4,
            padx=15,
            pady=5
        )

        ttk.Label(
            self.ventas_tab,
            text="Ventas registradas",
            font=("Arial", 12, "bold")
        ).pack(
            anchor="w",
            pady=(10, 5)
        )

        columnas = (
            "id",
            "usuario",
            "producto",
            "fecha"
        )

        self.ventas_tree = ttk.Treeview(
            self.ventas_tab,
            columns=columnas,
            show="headings"
        )

        self.ventas_tree.heading(
            "id",
            text="ID"
        )

        self.ventas_tree.heading(
            "usuario",
            text="Usuario"
        )

        self.ventas_tree.heading(
            "producto",
            text="Producto"
        )

        self.ventas_tree.heading(
            "fecha",
            text="Fecha"
        )

        self.ventas_tree.column(
            "id",
            width=60,
            anchor="center"
        )

        self.ventas_tree.column(
            "usuario",
            width=220
        )

        self.ventas_tree.column(
            "producto",
            width=250
        )

        self.ventas_tree.column(
            "fecha",
            width=180,
            anchor="center"
        )

        self.ventas_tree.pack(
            fill="both",
            expand=True
        )

    def cargar_usuarios_combo(self):

        usuarios = self.restaurante_servicio.obtener_usuarios()

        self.usuarios_combo_data = {
            f"{usuario.id} - {usuario.nombre}": usuario.id
            for usuario in usuarios
        }

        self.usuario_combo["values"] = list(
            self.usuarios_combo_data.keys()
        )

    def cargar_productos_combo(self):

        productos = self.restaurante_servicio.obtener_productos()

        self.productos_combo_data = {
            f"{producto.id} - {producto.nombre}": producto.id
            for producto in productos
        }

        self.producto_combo["values"] = list(
            self.productos_combo_data.keys()
        )

    def actualizar_combo_productos(self):
        self.cargar_productos_combo()

    def cargar_ventas(self):

        self.cargar_usuarios_combo()
        self.cargar_productos_combo()

        for item in self.ventas_tree.get_children():
            self.ventas_tree.delete(item)

        ventas = (
            self.restaurante_servicio
            .obtener_ventas_detalladas()
        )

        for venta in ventas:

            self.ventas_tree.insert(
                "",
                "end",
                values=(
                    venta["id"],
                    venta["usuario"],
                    venta["producto"],
                    venta["fecha"]
                )
            )

    def registrar_venta(self):

        usuario_seleccionado = (
            self.usuario_combo.get()
        )

        producto_seleccionado = (
            self.producto_combo.get()
        )

        if not usuario_seleccionado:

            messagebox.showwarning(
                "Venta",
                "Seleccione un usuario"
            )

            return

        if not producto_seleccionado:

            messagebox.showwarning(
                "Venta",
                "Seleccione un producto"
            )

            return

        usuario_id = self.usuarios_combo_data[
            usuario_seleccionado
        ]

        producto_id = self.productos_combo_data[
            producto_seleccionado
        ]

        correcto, mensaje = (
            self.restaurante_servicio.registrar_venta(
                usuario_id,
                producto_id
            )
        )

        if correcto:

            messagebox.showinfo(
                "Venta registrada",
                mensaje
            )

            self.usuario_combo.set("")
            self.producto_combo.set("")

            self.cargar_ventas()

        else:

            messagebox.showerror(
                "Error al registrar",
                mensaje
            )

    def cerrar_sesion(self):

        respuesta = messagebox.askyesno(
            "Cerrar sesión",
            "¿Desea cerrar la sesión actual?"
        )

        if respuesta:
            self.on_logout()
