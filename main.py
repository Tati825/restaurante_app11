import tkinter as tk
from tkinter import ttk
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView

class RestauranteApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Restaurante - Semana 15"
        )

        self.root.geometry(
            "1100x700"
        )

        self.root.minsize(
            900,
            600
        )

        self.configurar_estilos()

        self.restaurante_servicio = (
            RestauranteServicio()
        )

        self.mostrar_login()

    def configurar_estilos(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "TButton",
            padding=8,
            font=("Arial", 10)
        )

        style.configure(
            "TLabel",
            font=("Arial", 10)
        )

        style.configure(
            "Treeview",
            rowheight=30,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

        style.configure(
            "TNotebook.Tab",
            padding=(15, 8)
        )

    def limpiar_ventana(self):

        for widget in self.root.winfo_children():
            widget.destroy()

    def mostrar_login(self):

        self.limpiar_ventana()

        login_view = LoginView(
            self.root,
            self.restaurante_servicio,
            self.iniciar_sesion
        )

        login_view.pack(
            fill="both",
            expand=True
        )

    def iniciar_sesion(self, usuario):

        self.mostrar_main(
            usuario
        )

    def mostrar_main(self, usuario):

        self.limpiar_ventana()

        main_view = MainView(
            self.root,
            self.restaurante_servicio,
            usuario,
            self.cerrar_sesion
        )

        main_view.pack(
            fill="both",
            expand=True
        )

    def cerrar_sesion(self):

        self.mostrar_login()

def main():

    root = tk.Tk()

    app = RestauranteApp(root)

    root.mainloop()

if __name__ == "__main__":
    main()
