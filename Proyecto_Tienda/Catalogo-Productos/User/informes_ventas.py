import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  # Importar el selector de fecha
from Model.ventas_dao import listar_ventas_por_rango, obtener_rango

class InformeVentas(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.configure(bg="#f4f4f4")  # Fondo claro
        self.pack(fill='both', expand=True, padx=20, pady=20)
        self.campos_filtro()
        self.tabla_informes()

    def campos_filtro(self):
        # Menú desplegable para seleccionar el periodo
        self.label_periodo = tk.Label(
            self, text="Seleccione el periodo:", font=('Arial', 12, 'bold'), bg="#f4f4f4"
        )
        self.label_periodo.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.periodo_var = tk.StringVar(value="diario")
        self.menu_periodo = ttk.Combobox(self, textvariable=self.periodo_var, state='readonly', width=30, font=('Arial', 11))  # Ajuste de tamaño de letra
        self.menu_periodo['values'] = ("diario", "semanal", "mensual")
        self.menu_periodo.grid(row=0, column=1, padx=10, pady=10)
        self.menu_periodo.bind("<<ComboboxSelected>>", self.cambiar_campos)

        # Cambiar el tamaño de la fuente de las opciones del Combobox
        style = ttk.Style()
        style.configure("TCombobox",
                        font=('Arial', 12))  # Establecer el tamaño de la fuente para las opciones
        self.menu_periodo.configure(style="TCombobox")

        # Etiquetas y entradas de fechas con calendario
        self.label_inicio = tk.Label(
            self, text="Fecha Inicio:", font=('Arial', 12, 'bold'), bg="#f4f4f4"
        )
        self.label_inicio.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.entry_inicio = DateEntry(self, font=('Arial', 12), width=25, date_pattern='yyyy-MM-dd')  # Ajuste de tamaño de letra
        self.entry_inicio.grid(row=1, column=1, padx=10, pady=10)

        self.label_fin = tk.Label(
            self, text="Fecha Fin:", font=('Arial', 12, 'bold'), bg="#f4f4f4"
        )
        self.label_fin.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.entry_fin = DateEntry(self, font=('Arial', 12), width=25, date_pattern='yyyy-MM-dd')  # Ajuste de tamaño de letra
        self.entry_fin.grid(row=2, column=1, padx=10, pady=10)

        # Botón para filtrar
        self.boton_filtrar = tk.Button(
            self, text="Filtrar", font=('Arial', 10, 'bold'),
            bg="#4CAF50", fg="white", activebackground="#45a049",
            command=self.actualizar_informe
        )
        self.boton_filtrar.grid(row=3, column=0, columnspan=2, pady=15)

        # Inicializa los campos según el periodo
        self.cambiar_campos()

    def cambiar_campos(self, event=None):
        periodo = self.periodo_var.get()
        if periodo == "diario":
            self.label_fin.grid_remove()
            self.entry_fin.grid_remove()
        else:
            self.label_fin.grid()
            self.entry_fin.grid()

    def tabla_informes(self):
        # Tabla con estilos mejorados
        self.tabla = ttk.Treeview(self, columns=('Producto', 'Cantidad', 'Fecha', 'Total Vendido'), show='headings')
        self.tabla.grid(row=4, column=0, columnspan=3, sticky='nsew', pady=10)

        # Configuración de encabezados
        encabezados = ['Producto', 'Cantidad', 'Fecha', 'Total Vendido']
        for idx, encabezado in enumerate(encabezados):
            self.tabla.heading(f'#{idx + 1}', text=encabezado, anchor='center')
            self.tabla.column(f'#{idx + 1}', anchor='center', width=150)

        # Scrollbar
        self.scroll = ttk.Scrollbar(self, orient='vertical', command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=self.scroll.set)
        self.scroll.grid(row=4, column=3, sticky='ns')

    def actualizar_informe(self):
        periodo = self.periodo_var.get()
        fecha_inicio = self.entry_inicio.get()
        fecha_fin = self.entry_fin.get()

        try:
            if periodo == "diario":
                fecha_inicio, fecha_fin = obtener_rango(periodo, fecha_inicio)
            else:
                if not fecha_inicio or not fecha_fin:
                    raise ValueError("Debe ingresar un intervalo de fechas.")

            ventas = listar_ventas_por_rango(fecha_inicio, fecha_fin)

            # Limpia la tabla antes de agregar nuevos datos
            for row in self.tabla.get_children():
                self.tabla.delete(row)

            # Agrega los datos filtrados a la tabla
            for venta in ventas:
                # Formatear la fecha a "YYYY-MM-DD HH:MM"
                fecha_formateada = venta[3].strftime('%Y-%m-%d %H:%M')  # Usamos strftime para formatear la fecha
                # Formatear el total vendido a "$XX.XXX"
                total_formateado = f"${int(float(venta[4])):,.0f}".replace(',', '.')
                # Insertar en la tabla
                self.tabla.insert('', 'end', values=(venta[1], venta[2], fecha_formateada, total_formateado))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo filtrar: {e}")