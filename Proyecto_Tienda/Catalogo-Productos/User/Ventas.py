import tkinter as tk
from tkinter import ttk, messagebox
from Model.ventas_dao import Venta, registrar_venta, listar_ventas, listar, eliminar_venta


class VentasFrame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.pack(fill='both', expand=True)
        self.campos_ventas()
        self.tabla_ventas()

    def campos_ventas(self):
        self.label_producto = tk.Label(self, text='Producto:')
        self.label_producto.config(font=('Arial', 12, 'bold'))
        self.label_producto.grid(row=0, column=0, padx=10, pady=10)

        self.producto_id = tk.StringVar()
        self.combobox_producto = ttk.Combobox(self, textvariable=self.producto_id, state="readonly")
        self.actualizar_productos()
        self.combobox_producto.grid(row=0, column=1, padx=10, pady=10)

        self.label_cantidad = tk.Label(self, text='Cantidad:')
        self.label_cantidad.config(font=('Arial', 12, 'bold'))
        self.label_cantidad.grid(row=1, column=0, padx=10, pady=10)

        self.cantidad_venta = tk.StringVar()
        self.entry_cantidad = tk.Entry(self, textvariable=self.cantidad_venta)
        self.entry_cantidad.config(width=50, font=('Arial', 12))
        self.entry_cantidad.grid(row=1, column=1, padx=10, pady=10)

        self.boton_registrar_venta = tk.Button(self, text="Registrar Venta", command=self.registrar_venta)
        self.boton_registrar_venta.config(width=20, font=('Arial', 12, 'bold'), fg='#fcf9f3', bg='#1461d2', cursor='hand2')
        self.boton_registrar_venta.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def actualizar_productos(self):
        productos = listar()
        self.combobox_producto['values'] = [f"{p[0]} - {p[1]}" for p in productos]

    def registrar_venta(self):
        try:
            producto_id_texto = self.producto_id.get()
            cantidad = int(self.cantidad_venta.get())

            if not producto_id_texto:
                raise ValueError("Debe seleccionar un producto.")
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a 0.")

            producto_id = int(producto_id_texto.split(" - ")[0])

            nueva_venta = Venta(producto_id, cantidad)
            registrar_venta(nueva_venta)

            self.tabla_ventas()
            self.cantidad_venta.set('')
            self.producto_id.set('')
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def tabla_ventas(self):
        for widget in self.winfo_children():
            if isinstance(widget, ttk.Treeview):
                widget.destroy()

        self.Lista_Ventas = listar_ventas()
        self.tabla = ttk.Treeview(self, columns=('Producto', 'Cantidad', 'Fecha', 'Total Vendido'))
        self.tabla.grid(row=3, column=0, columnspan=2, sticky='nsew')

        self.tabla.heading('#0', text='ID')
        self.tabla.heading('#1', text='Producto')
        self.tabla.heading('#2', text='Cantidad')
        self.tabla.heading('#3', text='Fecha')
        self.tabla.heading('#4', text='Total Vendido')

        for v in self.Lista_Ventas:
            fecha_formateada = v[3].strftime("%d/%m/%y %H:%M")
            self.tabla.insert('', 'end', text=v[0], values=(v[1], v[2], fecha_formateada, f"${v[4]:.2f}"))

        self.scroll = ttk.Scrollbar(self, orient='vertical', command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=self.scroll.set)
        self.scroll.grid(row=3, column=2, sticky='ns')

        # Boton Eliminar, ahora abajo de la tabla
        self.boton_eliminar_venta = tk.Button(self, text="Eliminar Venta", command=self.eliminar_venta)
        self.boton_eliminar_venta.config(width=20, font=('Arial', 12, 'bold'), fg='#fcf9f3', bg='#e30b3c', cursor='hand2')
        self.boton_eliminar_venta.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Espacio adicional para ajustar la interfaz
        self.final_frame = tk.Frame(self)
        self.final_frame.grid(row=5, column=0, columnspan=3, pady=10)
        
    def eliminar_venta(self):
        try:
            # Obtener la venta seleccionada en la tabla
            venta_id = self.tabla.item(self.tabla.selection())['text']

            if not venta_id:
                raise ValueError("Debe seleccionar una venta para eliminar.")

            # Confirmar eliminación
            confirmacion = messagebox.askyesno("Confirmación", "¿Está seguro de eliminar esta venta?")
            if not confirmacion:
                return

            # Llamar a la función del modelo para eliminar
            eliminar_venta(venta_id)

            # Actualizar la tabla de ventas
            self.tabla_ventas()
            messagebox.showinfo("Éxito", "La venta se eliminó correctamente.")
        except IndexError:
            messagebox.showerror("Error", "Debe seleccionar una venta para eliminar.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")