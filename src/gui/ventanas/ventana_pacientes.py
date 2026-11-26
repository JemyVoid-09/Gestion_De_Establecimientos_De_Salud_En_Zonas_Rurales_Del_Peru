import tkinter as tk
from tkinter import messagebox
from src.servicios.paciente_servicio import PacienteServicio

class VentanaPacientes:
    def __init__(self, ventana, usuario):
        self.ventana = ventana
        self.servicio = PacienteServicio()
        self.usuario = usuario

        # Configurar el título y las dimensiones de la ventana.
        self.ventana.title("GestiónEsSalud - Gestión de pacientes")
        self.ventana.geometry("650x500")

        # Mostrar el encabezado de la ventana.
        tk.Label(
            ventana,
            text="GESTIÓN DE PACIENTES",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        # Crear el formulario para registrar pacientes.
        formulario = tk.Frame(ventana)
        formulario.pack(pady=10)

        # Crear el campo para ingresar el nombre del paciente.
        tk.Label(formulario, text="Nombre:").grid(row=0, column=0)
        self.nombre = tk.Entry(formulario)
        self.nombre.grid(row=0, column=1, padx=5)
        
        # Crear el campo para ingresar el DNI del paciente.
        tk.Label(formulario, text="DNI:").grid(row=1, column=0)
        self.dni = tk.Entry(formulario, show="*")
        self.dni.grid(row=1, column=1, padx=5)

        # Crear el botón para registrar los datos ingresados.
        tk.Button(
            formulario,
            text="Registrar paciente",
            command=self.registrar
        ).grid(row=2, column=0, columnspan=2, pady=10)

        # Crear el campo y el botón para buscar pacientes por nombre.
        busqueda = tk.Frame(ventana)
        busqueda.pack(pady=10)

        tk.Label(busqueda, text="Buscar por nombre:").pack(side=tk.LEFT)

        self.criterio = tk.Entry(busqueda)
        self.criterio.pack(side=tk.LEFT, padx=5)

        # Mostrar todos los pacientes registrados.
        tk.Button(
            busqueda,
            text="Buscar",
            command=self.buscar
        ).pack(side=tk.LEFT)

        tk.Button(
            ventana,
            text="Mostrar todos",
            command=self.mostrar_todos
        ).pack(pady=5)

        # Crear la lista donde se visualizarán los resultados.
        self.resultados = tk.Listbox(ventana, width=75, height=12)
        self.resultados.pack(pady=10)

    def registrar(self):
        try:
            # Obtener los datos ingresados en los campos.
            nombre = self.nombre.get()
            dni = self.dni.get()
            
            # Registrar al paciente mediante el servicio correspondiente.
            paciente = self.servicio.registrar_paciente(
                nombre,
                dni,
                self.usuario
            )
            
            messagebox.showinfo(
                "Registro",
                f"Paciente registrado correctamente.\n"
                f"ID asignado: {paciente.get_id_paciente()}"
            )
            
            # Limpiar los campos después de completar el registro.
            self.nombre.delete(0, tk.END)
            self.dni.delete(0, tk.END)
            
            # Actualizar la lista de pacientes.
            self.mostrar_todos()
            
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def buscar(self):
        try:
            # Buscar pacientes según el nombre ingresado.
            pacientes = self.servicio.buscar_paciente_por_nombre(
                self.criterio.get(),
                self.usuario
            )

            # Limpiar los resultados anteriores.
            self.resultados.delete(0, tk.END)

            # Mostrar los datos de los pacientes encontrados.
            for paciente in pacientes:
                self.resultados.insert(
                    tk.END,
                    f"{paciente.get_id_paciente()} | "
                    f"{paciente.get_nombre()} | "
                    f"DNI: {paciente.get_dni_hash()[:12]}..."
                )

        except Exception as error:
            messagebox.showerror("Error", str(error))

    def mostrar_todos(self):
        # Obtener los pacientes disponibles para el usuario autenticado.
        pacientes = self.servicio.obtener_pacientes(self.usuario)

        # Limpiar la lista antes de mostrar los registros.
        self.resultados.delete(0, tk.END)

        # Mostrar los datos de todos los pacientes obtenidos.
        for paciente in pacientes:
            self.resultados.insert(
                tk.END,
                f"{paciente.get_id_paciente()} | "
                f"{paciente.get_nombre()} | "
                f"DNI: {paciente.get_dni_hash()[:12]}..."
            )
