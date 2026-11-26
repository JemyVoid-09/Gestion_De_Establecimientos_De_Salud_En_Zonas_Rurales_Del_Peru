import tkinter as tk
from tkinter import messagebox

from src.servicios.autenticacion_servicio import AutenticacionServicio

class VentanaLogin:
    def __init__(self, ventana, al_ingresar):
        self.ventana = ventana
        self.al_ingresar = al_ingresar
        self.servicio = AutenticacionServicio()

        # Configurar el título y las dimensiones de la ventana.
        self.ventana.title("GestiónEsSalud - Inicio de sesión")
        self.ventana.geometry("350x250")

        # Mostrar el título de la aplicación.
        tk.Label(
            ventana,
            text="GESTIONESALUD",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        # Crear los campos para ingresar las credenciales.
        tk.Label(ventana, text="Usuario").pack()
        self.usuario = tk.Entry(ventana)
        self.usuario.pack()

        tk.Label(ventana, text="Contraseña").pack()
        self.contrasena = tk.Entry(ventana, show="*")
        self.contrasena.pack()

        # Crear el botón para iniciar sesión.
        tk.Button(
            ventana,
            text="Ingresar",
            command=self.verificar_campos
        ).pack(pady=20)

        # Permitir iniciar sesión presionando la tecla Enter.
        self.ventana.bind("<Return>", lambda evento: self.verificar_campos())

    def verificar_campos(self):
        # Obtener las credenciales ingresadas.
        nombre = self.usuario.get().strip()
        contrasena = self.contrasena.get()

        # Verificar que ambos campos estén completos.
        if not nombre or not contrasena:
            messagebox.showwarning(
                "Advertencia",
                "Complete todos los campos."
            )
            return

        # Comprobar las credenciales mediante el servicio de autenticación.
        usuario = self.servicio.autenticar(nombre, contrasena)

        if usuario is None:
            messagebox.showerror(
                "Acceso denegado",
                "Usuario o contraseña incorrectos, o cuenta desactivada."
            )
            return

        # Confirmar el acceso y mostrar el rol del usuario.
        messagebox.showinfo(
            "Bienvenido",
            f"Inicio de sesión correcto. Rol: {usuario.get_rol().get_nombre()}"
        )

        # Enviar el usuario autenticado a la siguiente ventana.
        self.al_ingresar(usuario)
