import tkinter as tk
from tkinter import ttk
from Model.producto_dao import Productos, guardar, listar, editar, eliminar

class ProductosFrame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.pack(fill='both', expand=True)  # Ajustar el Frame al tamaño de la ventana
        self.id = None
        self.campos_productos()
        self.desabilitar_campos()
        self.tabla_productos()

    def campos_productos(self):
        # Labels de cada campo
        self.label_nombre = tk.Label(self, text='Descripcion:')
        self.label_nombre.config(font=('Arial', 12, 'bold'))
        self.label_nombre.grid(row=0, column=0, padx=10, pady=10)

        self.label_precio = tk.Label(self, text='Precio:')
        self.label_precio.config(font=('Arial', 12, 'bold'))
        self.label_precio.grid(row=1, column=0, padx=10, pady=10)

        self.label_cantidad = tk.Label(self, text='Cantidad:')
        self.label_cantidad.config(font=('Arial', 12, 'bold'))
        self.label_cantidad.grid(row=2, column=0, padx=10, pady=10)

        # Entrys de cada campo
        self.mi_nombre = tk.StringVar()
        self.entry_nombre = tk.Entry(self, textvariable=self.mi_nombre)
        self.entry_nombre.config(width=50, font=('Arial', 12))
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10, columnspan=2)

        self.mi_precio = tk.StringVar()
        self.entry_precio = tk.Entry(self, textvariable=self.mi_precio)
        self.entry_precio.config(width=50, font=('Arial', 12))
        self.entry_precio.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

        self.mi_cantidad = tk.StringVar()
        self.entry_cantidad = tk.Entry(self, textvariable=self.mi_cantidad)
        self.entry_cantidad.config(width=50, font=('Arial', 12))
        self.entry_cantidad.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

        # Botones
        self.boton_nuevo = tk.Button(self, text="Nuevo", command=self.habilitar_campos)
        self.boton_nuevo.config(width=20, font=('Arial', 12, 'bold'), fg='#fcf9f3', bg='#35ae0b', cursor='hand2', activebackground='#38a512')
        self.boton_nuevo.grid(row=3, column=0, padx=10, pady=10)

        self.boton_guardar = tk.Button(self, text="Guardar", command=self.guardar_datos)
        self.boton_guardar.config(width=20, font=('Arial', 12, 'bold'), fg='#fcf9f3', bg='#1461d2', cursor='hand2', activebackground='#125cc8')
        self.boton_guardar.grid(row=3, column=1, padx=10, pady=10)

        self.boton_cancelar = tk.Button(self, text="Cancelar", command=self.desabilitar_campos)
        self.boton_cancelar.config(width=20, font=('Arial', 12, 'bold'), fg='#fcf9f3', bg='#e30b3c', cursor='hand2', activebackground='#d40e3b')
        self.boton_cancelar.grid(row=3, column=2, padx=10, pady=10)

    def habilitar_campos(self):
        self.mi_nombre.set('')
        self.mi_precio.set('')
        self.mi_cantidad.set('')
        self.entry_nombre.config(state='normal')
        self.entry_precio.config(state='normal')
        self.entry_cantidad.config(state='normal')
        self.boton_guardar.config(state='normal')
        self.boton_cancelar.config(state='normal')

    def desabilitar_campos(self):
        self.id = None
        self.mi_nombre.set('')
        self.mi_precio.set('')
        self.mi_cantidad.set('')
        self.entry_nombre.config(state='disabled')
        self.entry_precio.config(state='disabled')
        self.entry_cantidad.config(state='disabled')
        self.boton_guardar.config(state='disabled')
        self.boton_cancelar.config(state='disabled')

    def guardar_datos(self):
        productos = Productos(self.mi_nombre.get(), self.mi_precio.get(), self.mi_cantidad.get())
        if self.id is None:
            guardar(productos)
        else:
            editar(productos, self.id)
        self.tabla_productos()
        self.desabilitar_campos()

    def tabla_productos(self):
        # Destruir cualquier tabla previa para evitar duplicados
        for widget in self.winfo_children():
            if isinstance(widget, ttk.Treeview):
                widget.destroy()

        # Crear el estilo para la tabla con bordes y centrado
        style = ttk.Style()
        style.configure(
            "Treeview",
            borderwidth=1,
            relief="solid",
            rowheight=30,  # Altura de las filas
            font=('Arial', 12)  # Fuente de los datos en la tabla
        )
        style.configure(
            "Treeview.Heading",
            font=('Arial', 12, 'bold'),  # Fuente de los encabezados
            height=30  # Altura de los encabezados
        )
        style.map(
            "Treeview",
            background=[("selected", "#0078d7")],  # Fondo azul para la fila seleccionada
            foreground=[("selected", "white")]    # Texto blanco para la fila seleccionada
        )

        # Crear la tabla con columnas ajustadas
        self.Lista_Productos = listar()
        self.tabla = ttk.Treeview(
            self, columns=('Descripcion', 'Precio', 'Cantidad'), style="Treeview"
        )
        self.tabla.grid(row=4, column=0, columnspan=3, sticky='nsew', padx=(10, 0))  # Espacio izquierdo

        # Encabezados de las columnas
        self.tabla.heading('#0', text='ID', anchor='center')
        self.tabla.heading('#1', text='Descripcion', anchor='center')
        self.tabla.heading('#2', text='Precio', anchor='center')
        self.tabla.heading('#3', text='Cantidad', anchor='center')

        # Configurar las columnas con más espacio y centrado
        self.tabla.column('#0', width=100, anchor='center')  # Columna ID
        self.tabla.column('#1', width=200, anchor='center')  # Descripcion
        self.tabla.column('#2', width=100, anchor='center')  # Precio
        self.tabla.column('#3', width=100, anchor='center')  # Cantidad

        # Insertar las filas con formato
        for p in self.Lista_Productos:
            # Formatear el precio con separador de miles y sin decimales
            precio_formateado = f"${int(float(p[2])):,.0f}".replace(',', '.')
            self.tabla.insert('', 'end', text=p[0], values=(p[1], precio_formateado, p[3]))

        # Agregar scroll vertical
        self.scroll = ttk.Scrollbar(self, orient='vertical', command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=self.scroll.set)
        self.scroll.grid(row=4, column=3, sticky='ns')

        # Botón Editar
        self.boton_editar = tk.Button(self, text="Editar", command=self.editar_datos)
        self.boton_editar.config(width=20, font=('Arial', 12, 'bold'), fg='#fcf9f3', bg='#35ae0b', cursor='hand2', activebackground='#38a512')
        self.boton_editar.grid(row=5, column=0, padx=10, pady=10)

        # Botón Eliminar
        self.boton_eliminar = tk.Button(self, text="Eliminar", command=self.eliminar_datos)
        self.boton_eliminar.config(width=20, font=('Arial', 12, 'bold'), fg='#fcf9f3', bg='#e30b3c', cursor='hand2', activebackground='#d40e3b')
        self.boton_eliminar.grid(row=5, column=1, padx=10, pady=10)

    def editar_datos(self):
        try:
            # Obtener el elemento seleccionado en la tabla
            self.id = self.tabla.item(self.tabla.selection())['text']
            self.nombre_producto = self.tabla.item(self.tabla.selection())['values'][0]
            precio_formateado = self.tabla.item(self.tabla.selection())['values'][1]
            self.precio_producto = precio_formateado.replace('$', '').replace('.', '').replace(',', '.')
            self.cantidad_producto = self.tabla.item(self.tabla.selection())['values'][2]

            # Habilitar campos para editar
            self.habilitar_campos()

            # Rellenar los campos con los valores seleccionados
            self.entry_nombre.insert(0, self.nombre_producto)
            self.entry_precio.insert(0, self.precio_producto)
            self.entry_cantidad.insert(0, self.cantidad_producto)
        except IndexError:
            # Controlar el error si no hay selección
            print("No se seleccionó ningún elemento.")

    def guardar_datos(self):
        try:
            # Quitar símbolos y convertir a número antes de guardar
            precio_sin_formato = float(self.mi_precio.get().replace('$', '').replace('.', '').replace(',', '.'))
            productos = Productos(self.mi_nombre.get(), precio_sin_formato, self.mi_cantidad.get())
            if self.id is None:
                guardar(productos)
            else:
                editar(productos, self.id)
            self.tabla_productos()
            self.desabilitar_campos()
        except ValueError:
            print("Error: Asegúrate de ingresar un precio válido.")

    def eliminar_datos(self):
        self.id = self.tabla.item(self.tabla.selection())['text']
        eliminar(self.id)
        self.tabla_productos()
        self.id = None