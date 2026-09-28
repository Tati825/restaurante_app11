import tkinter as tk
from tkinter import ttk, messagebox
import os

class LoginView(ttk.Frame):

    def __init__(self, parent, restaurante_servicio, on_login):
        super().__init__(parent)

        self.restaurante_servicio = restaurante_servicio
        self.on_login = on_login

        self.configure(padding=30)

        self.crear_interfaz()

    def crear_interfaz(self):

        logo_frame = ttk.Frame(self)
        logo_frame.pack(pady=(20, 10))

        logo_path = "assets/logo.png"

        if os.path.exists(logo_path):
            try:
                self.logo = tk.PhotoImage(file=logo_path)

                logo_label = ttk.Label(
                    logo_frame,
                    image=self.logo
                )

                logo_label.pack()

            except tk.TclError:
                self.crear_titulo(logo_frame)

        else:
            self.crear_titulo(logo_frame)

        ttk.Label(
            self,
            text="Restaurante App",
            font=("Arial", 24, "bold")
        ).pack(pady=10)

        ttk.Label(
            self,
            text="Sistema de gestión de restaurante",
            font=("Arial", 11)
        ).pack(pady=(0, 25))

        formulario = ttk.LabelFrame(
            self,
            text="Inicio de sesión",
            padding=20
        )

        formulario.pack(
            padx=30,
            pady=10
        )

        ttk.Label(
            formulario,
            text="Usuario:"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.usuario_entry = ttk.Entry(
            formulario,
            width=30
        )

        self.usuario_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        ttk.Label(
            formulario,
            text="Contraseña:"
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.password_entry = ttk.Entry(
            formulario,
            width=30,
            show="*"
        )

        self.password_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=10
        )

        ttk.Button(
            formulario,
            text="Iniciar sesión",
            command=self.iniciar_sesion
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            pady=20
        )

        self.usuario_entry.focus()

        self.password_entry.bind(
            "<Return>",
            lambda event: self.iniciar_sesion()
        )

    def crear_titulo(self, parent):

        ttk.Label(
            parent,
            text="🍽",
            font=("Arial", 40)
        ).pack()

    def iniciar_sesion(self):

        usuario = self.usuario_entry.get().strip()
        password = self.password_entry.get()

        if not usuario or not password:
            messagebox.showwarning(
                "Datos incompletos",
                "Ingrese usuario y contraseña"
            )
            return

        usuario_obj = self.restaurante_servicio.autenticar_usuario(
            usuario,
            password
        )

        if usuario_obj:

            self.on_login(usuario_obj)

        else:

            messagebox.showerror(
                "Acceso denegado",
                "Usuario o contraseña incorrectos"
            )
