import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime
from Model.cuentas_credito_dao import crear_cuenta_credito, listar_cuentas_credito, registrar_pago, obtener_detalles_cuenta, listar_cuentas_pendientes


class CuentasCreditoFrame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.pack(fill='both', expand=True)

        self.cuentas = []  # Lista para almacenar cuentas
        self.crear_componentes()

    def crear_componentes(self):
        # Labels de entrada
        self.label_cliente = tk.Label(self, text="Cliente:")
        self.label_cliente.config(font=('Arial', 12, 'bold'))
        self.label_cliente.grid(row=0, column=0, padx=10, pady=10)

        self.label_deuda = tk.Label(self, text="Deuda:")
        self.label_deuda.config(font=('Arial', 12, 'bold'))
        self.label_deuda.grid(row=1, column=0, padx=10, pady=10)

        # Entradas de texto
        self.cliente = tk.StringVar()  # Variable para el campo Cliente
        self.entry_cliente = tk.Entry(self, textvariable=self.cliente, font=('Arial', 12))
        self.entry_cliente.config(width=30)
        self.entry_cliente.grid(row=0, column=1, padx=10, pady=10, columnspan=2)

        self.deuda = tk.DoubleVar()  # Variable para el campo Deuda
        self.entry_deuda = tk.Entry(self, textvariable=self.deuda, font=('Arial', 12))
        self.entry_deuda.config(width=30)
        self.entry_deuda.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

        # Botón para crear cuenta
        self.boton_crear_cuenta = tk.Button(self, text="Crear Cuenta", command=self.crear_cuenta_credito)
        self.boton_crear_cuenta.config(width=20, font=('Arial', 12, 'bold'), fg='#fcf9f3', bg='#35ae0b', cursor='hand2',
                                       activebackground='#38a512')
        self.boton_crear_cuenta.grid(row=2, column=1, padx=10, pady=10)

        # Botón para ver cuentas pendientes
        self.boton_cuentas_pendientes = tk.Button(self, text="Cuentas Pendientes", command=self.mostrar_cuentas_pendientes)
        self.boton_cuentas_pendientes.config(width=20, font=('Arial', 12, 'bold'), fg='#fcf9f3', bg='#e67e22',
                                             cursor='hand2', activebackground='#d35400')
        self.boton_cuentas_pendientes.grid(row=4, column=2, padx=10, pady=10)

        # Estilos para la tabla
        style = ttk.Style()
        style.theme_use('clam')  # Usar un tema compatible con estilos personalizados

        style.configure(
            "Treeview",
            font=('Arial', 12),
            rowheight=30,
            fieldbackground='#f8f9fa',  # Fondo de las filas
        )
        style.configure(
            "Treeview.Heading",
            font=('Arial', 12, 'bold'),  # Negrita para los encabezados
            background='#0078d7',  # Fondo azul
            foreground='white',  # Texto blanco
            relief="raised",  # Relieve en los encabezados
        )
        style.map(
            "Treeview.Heading",
            background=[('active', '#005bb5')],  # Fondo más oscuro al pasar el mouse
            foreground=[('active', 'white')]  # Texto blanco al pasar el mouse
        )
        style.map(
            "Treeview",
            background=[("selected", "#0078d7")],  # Fondo azul al seleccionar
            foreground=[("selected", "white")]  # Texto blanco al seleccionar
        )

        # Tabla de cuentas de crédito
        self.tabla_cuentas = ttk.Treeview(self, columns=("Cliente", "Deuda", "Saldo", "Estado", "Fecha"), show="headings")

        # Configuración de encabezados
        self.tabla_cuentas.heading("Cliente", text="Cliente")
        self.tabla_cuentas.heading("Deuda", text="Deuda")
        self.tabla_cuentas.heading("Saldo", text="Saldo")
        self.tabla_cuentas.heading("Estado", text="Estado")
        self.tabla_cuentas.heading("Fecha", text="Fecha Creación")

        # Configuración de columnas
        self.tabla_cuentas.column("Cliente", anchor='center', width=200)
        self.tabla_cuentas.column("Deuda", anchor='center', width=100)
        self.tabla_cuentas.column("Saldo", anchor='center', width=100)
        self.tabla_cuentas.column("Estado", anchor='center', width=100)
        self.tabla_cuentas.column("Fecha", anchor='center', width=120)

        self.tabla_cuentas.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        # Scroll vertical para la tabla
        self.scroll = ttk.Scrollbar(self, orient='vertical', command=self.tabla_cuentas.yview)
        self.tabla_cuentas.configure(yscrollcommand=self.scroll.set)
        self.scroll.grid(row=3, column=3, sticky='ns')

        # Botones de acciones
        self.boton_ver_detalles = tk.Button(self, text="Ver Detalles", command=self.ver_detalles_cuenta)
        self.boton_ver_detalles.config(width=20, font=('Arial', 12, 'bold'), fg='#fcf9f3', bg='#0078d7', cursor='hand2',
                                       activebackground='#005bb5')
        self.boton_ver_detalles.grid(row=4, column=0, padx=10, pady=10)

        self.boton_registrar_pago = tk.Button(self, text="Registrar Pago", command=self.registrar_pago)
        self.boton_registrar_pago.config(width=20, font=('Arial', 12, 'bold'), fg='#fcf9f3', bg='#35ae0b', cursor='hand2',
                                         activebackground='#38a512')
        self.boton_registrar_pago.grid(row=4, column=1, padx=10, pady=10)

        self.actualizar_tabla_cuentas()

    def crear_cuenta_credito(self):
        cliente = self.cliente.get().strip()
        deuda = self.deuda.get()
        if not cliente or deuda <= 0:
            messagebox.showerror("Error", "Debe ingresar un nombre de cliente y una deuda válida.")
            return

        try:
            crear_cuenta_credito(cliente, deuda)
            messagebox.showinfo("Éxito", "La cuenta de crédito se creó correctamente.")
            self.actualizar_tabla_cuentas()
            # Limpiar los campos después de crear la cuenta
            self.cliente.set("")
            self.deuda.set(0.0)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def actualizar_tabla_cuentas(self):
        self.cuentas = listar_cuentas_credito()
        for item in self.tabla_cuentas.get_children():
            self.tabla_cuentas.delete(item)

        for cuenta in self.cuentas:
            self.tabla_cuentas.insert("", "end", values=(cuenta[1], f"${cuenta[2]:,.2f}", f"${cuenta[3]:,.2f}", cuenta[4], cuenta[5]))

    def ver_detalles_cuenta(self):
        cuenta_seleccionada = self.tabla_cuentas.focus()
        if not cuenta_seleccionada:
            messagebox.showerror("Error", "Debe seleccionar una cuenta.")
            return

        # Obtener el índice y los detalles de la cuenta seleccionada
        index = int(self.tabla_cuentas.index(cuenta_seleccionada))
        cuenta_id = self.cuentas[index][0]
        detalles, pagos = obtener_detalles_cuenta(cuenta_id)

        # Crear la información de los detalles de la cuenta
        detalles_texto = f"Cliente: {detalles[1]}\nDeuda: ${int(detalles[2]):,}\nSaldo: ${int(detalles[3]):,}\nEstado: {detalles[4]}\nFecha: {detalles[5]}"

        # Crear la información de los pagos, ajustando el formato
        pagos_texto = ""
        for p in pagos:
            try:
                # Intentar analizar la fecha con hora
                if " " in p[2]:  # Si incluye espacio, asume que tiene hora
                    fecha_original = datetime.datetime.strptime(p[2], '%d/%m/%Y %H:%M:%S')
                    fecha_formateada = fecha_original.strftime('%d/%m/%y %H:%M')
                else:  # Si no incluye hora, formatea solo la fecha
                    fecha_original = datetime.datetime.strptime(p[2], '%d/%m/%Y')
                    fecha_formateada = fecha_original.strftime('%d/%m/%y')
            except ValueError:
                # Si no tiene el formato esperado, usar la fecha tal cual
                fecha_formateada = p[2]

            # Formatear el monto sin ID ni decimales
            pagos_texto += f"Monto: ${int(p[1]):,}, Fecha: {fecha_formateada}\n"

        # Mostrar el mensaje con los detalles y los pagos formateados
        messagebox.showinfo("Detalles de la Cuenta", f"{detalles_texto}\n\nPagos:\n{pagos_texto.strip()}")

    def registrar_pago(self):
        cuenta_seleccionada = self.tabla_cuentas.focus()
        if not cuenta_seleccionada:
            messagebox.showerror("Error", "Debe seleccionar una cuenta.")
            return

        # Obtener el índice de la cuenta seleccionada y sus detalles
        index = int(self.tabla_cuentas.index(cuenta_seleccionada))
        cuenta = self.cuentas[index]  # Información de la cuenta seleccionada
        cuenta_id = cuenta[0]  # ID de la cuenta
        estado = cuenta[4]  # Estado de la cuenta (posición 4 del registro)

        # Verificar si el estado es "Completado"
        if estado.lower() == "completado":
            messagebox.showerror("Acción no permitida", "No se puede registrar un pago para una cuenta completada.")
            return

        # Solicitar el monto del pago
        monto = simpledialog.askfloat("Registrar Pago", "Ingrese el monto del pago:")
        if not monto or monto <= 0:
            messagebox.showerror("Error", "Debe ingresar un monto válido.")
            return

        # Intentar registrar el pago
        try:
            registrar_pago(cuenta_id, monto)
            messagebox.showinfo("Éxito", "El pago se registró correctamente.")
            self.actualizar_tabla_cuentas()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def mostrar_cuentas_pendientes(self):
        """
        Actualiza la tabla para mostrar solo cuentas con estado 'Pendiente'.
        """
        try:
            # Obtiene las cuentas pendientes del modelo
            self.cuentas = listar_cuentas_pendientes()

            # Limpia la tabla
            for item in self.tabla_cuentas.get_children():
                self.tabla_cuentas.delete(item)

            # Inserta las cuentas pendientes en la tabla
            for cuenta in self.cuentas:
                self.tabla_cuentas.insert("", "end", values=(cuenta[1], f"${cuenta[2]:,.2f}", f"${cuenta[3]:,.2f}", cuenta[4], cuenta[5]))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las cuentas pendientes: {e}")