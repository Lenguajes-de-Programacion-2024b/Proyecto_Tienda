import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from Model.ventas_dao import Venta, registrar_venta, listar_ventas, listar, eliminar_venta

class VentasFrame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.pack(fill='both', expand=True)

        # Lista temporal para manejar múltiples productos
        self.productos_seleccionados = []

        # Ventana emergente para productos seleccionados
        self.ventana_productos = None

        self.campos_ventas()
        self.tabla_ventas()

    def campos_ventas(self):
        self.label_producto = tk.Label(self, text='Producto:')
        self.label_producto.config(font=('Arial', 12, 'bold'))
        self.label_producto.grid(row=0, column=0, padx=10, pady=10)

        self.producto_id = tk.StringVar()
        self.combobox_producto = ttk.Combobox(self, textvariable=self.producto_id, state="readonly", font=('Arial', 12))
        self.actualizar_productos()
        self.combobox_producto.grid(row=0, column=1, padx=10, pady=10)

        self.label_cantidad = tk.Label(self, text='Cantidad:')
        self.label_cantidad.config(font=('Arial', 12, 'bold'))
        self.label_cantidad.grid(row=1, column=0, padx=10, pady=10)

        self.cantidad_venta = tk.StringVar()
        self.entry_cantidad = tk.Entry(self, textvariable=self.cantidad_venta)
        self.entry_cantidad.config(width=50, font=('Arial', 12))
        self.entry_cantidad.grid(row=1, column=1, padx=10, pady=10)

        self.label_cliente = tk.Label(self, text='Cliente:')
        self.label_cliente.config(font=('Arial', 12, 'bold'))
        self.label_cliente.grid(row=2, column=0, padx=10, pady=10)

        self.cliente = tk.StringVar()
        self.entry_cliente = tk.Entry(self, textvariable=self.cliente)
        self.entry_cliente.config(width=50, font=('Arial', 12))
        self.entry_cliente.grid(row=2, column=1, padx=10, pady=10)

        self.label_metodo_pago = tk.Label(self, text='Método de Pago:')
        self.label_metodo_pago.config(font=('Arial', 12, 'bold'))
        self.label_metodo_pago.grid(row=3, column=0, padx=10, pady=10)

        self.metodo_pago = tk.StringVar()
        self.combobox_metodo_pago = ttk.Combobox(self, textvariable=self.metodo_pago, state="readonly", font=('Arial', 12))
        self.actualizar_metodos_pago()
        self.combobox_metodo_pago.grid(row=3, column=1, padx=10, pady=10)

        # Botón agregar producto
        self.boton_agregar_producto = tk.Button(self, text="Agregar Producto", command=self.agregar_producto)
        self.boton_agregar_producto.config(width=20, font=('Arial', 12, 'bold'), fg='#fcf9f3', bg='#1461d2', cursor='hand2')
        self.boton_agregar_producto.grid(row=4, column=0, padx=10, pady=10)

        # Botón registrar venta
        self.boton_registrar_venta = tk.Button(self, text="Registrar Venta", command=self.registrar_venta)
        self.boton_registrar_venta.config(width=20, font=('Arial', 12, 'bold'), fg='#fcf9f3', bg='#1461d2', cursor='hand2')
        self.boton_registrar_venta.grid(row=4, column=1, padx=10, pady=10)

    def actualizar_metodos_pago(self):
        from Model.ventas_dao import listar_metodos_pago_para_ventas
        metodos = listar_metodos_pago_para_ventas()
        self.metodos_pago = {m[1]: m[0] for m in metodos}
        self.combobox_metodo_pago['values'] = list(self.metodos_pago.keys())

    def actualizar_productos(self):
        productos = listar()
        self.combobox_producto['values'] = [f"{p[0]} - {p[1]}" for p in productos]

    def abrir_ventana_productos(self):
        """
        Abre una ventana emergente para mostrar los productos seleccionados.
        """
        if self.ventana_productos is not None and tk.Toplevel.winfo_exists(self.ventana_productos):
            self.ventana_productos.lift()
            return

        self.ventana_productos = Toplevel(self)
        self.ventana_productos.title("Productos Seleccionados")
        self.ventana_productos.geometry("400x300")
        self.ventana_productos.resizable(False, False)

        self.tabla_productos = ttk.Treeview(self.ventana_productos, columns=('Producto', 'Cantidad'), show='headings')
        self.tabla_productos.heading('Producto', text='Producto')
        self.tabla_productos.heading('Cantidad', text='Cantidad')
        self.tabla_productos.pack(fill='both', expand=True)

        self.actualizar_tabla_productos_seleccionados()

    def agregar_producto(self):
        """
        Agrega un producto a la lista temporal y muestra la ventana emergente.
        """
        try:
            producto_id_texto = self.producto_id.get()
            cantidad = int(self.cantidad_venta.get())

            if not producto_id_texto:
                raise ValueError("Debe seleccionar un producto.")
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a 0.")

            producto_id = int(producto_id_texto.split(" - ")[0])
            producto_nombre = producto_id_texto.split(" - ")[1]

            self.productos_seleccionados.append({
                'producto_id': producto_id,
                'nombre': producto_nombre,
                'cantidad': cantidad
            })

            self.abrir_ventana_productos()
            self.actualizar_tabla_productos_seleccionados()

            self.cantidad_venta.set('')
            self.producto_id.set('')
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def actualizar_tabla_productos_seleccionados(self):
        """
        Actualiza la tabla de productos en la ventana emergente.
        """
        if self.ventana_productos and hasattr(self, 'tabla_productos'):
            for item in self.tabla_productos.get_children():
                self.tabla_productos.delete(item)

            for producto in self.productos_seleccionados:
                self.tabla_productos.insert('', 'end', values=(producto['nombre'], producto['cantidad']))

    def registrar_venta(self):
        """
        Registra los productos seleccionados como una venta y cierra la ventana emergente.
        """
        try:
            cliente = self.cliente.get().strip()
            metodo_pago_desc = self.metodo_pago.get()

            if not cliente:
                raise ValueError("Debe ingresar el nombre del cliente.")
            if not metodo_pago_desc:
                raise ValueError("Debe seleccionar un método de pago.")
            if not self.productos_seleccionados:
                raise ValueError("Debe agregar al menos un producto.")

            metodo_pago_id = self.metodos_pago.get(metodo_pago_desc)

            from Model.ventas_dao import Venta, registrar_venta

            for producto in self.productos_seleccionados:
                nueva_venta = Venta(
                    producto_id=producto['producto_id'],
                    cantidad=producto['cantidad'],
                    cliente=cliente,
                    metodo_pago_id=metodo_pago_id
                )
                registrar_venta(nueva_venta)

            messagebox.showinfo("Éxito", "La venta se registró correctamente.")
            self.productos_seleccionados = []
            if self.ventana_productos:
                self.ventana_productos.destroy()
                self.ventana_productos = None
            self.tabla_ventas()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def tabla_ventas(self):
        for widget in self.winfo_children():
            if isinstance(widget, ttk.Treeview) or isinstance(widget, ttk.Scrollbar):
                widget.destroy()

        style = ttk.Style()
        style.configure("Treeview", borderwidth=1, relief="solid", rowheight=30, font=('Arial', 12))
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'), height=30)
        style.map("Treeview", background=[("selected", "#0078d7")], foreground=[("selected", "white")])

        self.Lista_Ventas = listar_ventas()
        self.tabla = ttk.Treeview(
            self, columns=('Producto', 'Cantidad', 'Cliente', 'Método de Pago', 'Fecha', 'Total Vendido'), style="Treeview"
        )
        self.tabla.grid(row=5, column=0, columnspan=2, sticky='nsew', padx=(10, 0))

        self.tabla.heading('#0', text='ID', anchor='center')
        self.tabla.heading('#1', text='Producto', anchor='center')
        self.tabla.heading('#2', text='Cantidad', anchor='center')
        self.tabla.heading('#3', text='Cliente', anchor='center')
        self.tabla.heading('#4', text='Método de Pago', anchor='center')
        self.tabla.heading('#5', text='Fecha', anchor='center')
        self.tabla.heading('#6', text='Total Vendido', anchor='center')

        self.tabla.column('#0', width=50, anchor='center')
        self.tabla.column('#1', width=150, anchor='center')
        self.tabla.column('#2', width=100, anchor='center')
        self.tabla.column('#3', width=150, anchor='center')
        self.tabla.column('#4', width=150, anchor='center')
        self.tabla.column('#5', width=150, anchor='center')
        self.tabla.column('#6', width=150, anchor='center')

        for v in self.Lista_Ventas:
            fecha_formateada = v[5].strftime("%d/%m/%Y")
            total_vendido = f"${v[6]:,.0f}".replace(',', '.')
            self.tabla.insert('', 'end', text=v[0], values=(v[1], v[2], v[3], v[4], fecha_formateada, total_vendido))

        self.scroll = ttk.Scrollbar(self, orient='vertical', command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=self.scroll.set)
        self.scroll.grid(row=5, column=2, sticky='ns', padx=(0, 10))

        self.boton_eliminar_venta = tk.Button(self, text="Eliminar Venta", command=self.eliminar_venta)
        self.boton_eliminar_venta.config(
            width=20, font=('Arial', 12, 'bold'), fg='#fcf9f3', bg='#e30b3c', cursor='hand2'
        )
        self.boton_eliminar_venta.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def eliminar_venta(self):
        try:
            venta_id = self.tabla.item(self.tabla.selection())['text']
            if not venta_id:
                raise ValueError("Debe seleccionar una venta para eliminar.")

            confirmacion = messagebox.askyesno("Confirmación", "¿Está seguro de eliminar esta venta?")
            if not confirmacion:
                return

            eliminar_venta(venta_id)
            self.tabla_ventas()
            messagebox.showinfo("Éxito", "La venta se eliminó correctamente.")
        except IndexError:
            messagebox.showerror("Error", "Debe seleccionar una venta para eliminar.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")