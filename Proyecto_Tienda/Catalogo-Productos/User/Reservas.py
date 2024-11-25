import tkinter as tk
from tkinter import ttk
from Model.reserva_dao import Reserva, guardar_reserva, listar_reservas, editar_reserva, eliminar_reserva
from datetime import datetime

class ReservasFrame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.pack(fill='both', expand=True)
        self.id = None
        self.campos_reservas()
        self.desabilitar_campos()
        self.tabla_reservas()

    def campos_reservas(self):
        self.label_cliente = tk.Label(self, text='Cliente:')
        self.label_cliente.config(font=('Arial', 12, 'bold'))
        self.label_cliente.grid(row=0, column=0, padx=10, pady=10)

        self.label_producto = tk.Label(self, text='Producto ID:')
        self.label_producto.config(font=('Arial', 12, 'bold'))
        self.label_producto.grid(row=1, column=0, padx=10, pady=10)

        self.label_cantidad = tk.Label(self, text='Cantidad:')
        self.label_cantidad.config(font=('Arial', 12, 'bold'))
        self.label_cantidad.grid(row=2, column=0, padx=10, pady=10)

        self.label_fecha = tk.Label(self, text='Fecha (YYYY-MM-DD):')
        self.label_fecha.config(font=('Arial', 12, 'bold'))
        self.label_fecha.grid(row=3, column=0, padx=10, pady=10)

        self.mi_cliente = tk.StringVar()
        self.entry_cliente = tk.Entry(self, textvariable=self.mi_cliente)
        self.entry_cliente.config(width=50, font=('Arial', 12))
        self.entry_cliente.grid(row=0, column=1, padx=10, pady=10)

        self.mi_producto_id = tk.StringVar()
        self.entry_producto = tk.Entry(self, textvariable=self.mi_producto_id)
        self.entry_producto.config(width=50, font=('Arial', 12))
        self.entry_producto.grid(row=1, column=1, padx=10, pady=10)

        self.mi_cantidad = tk.StringVar()
        self.entry_cantidad = tk.Entry(self, textvariable=self.mi_cantidad)
        self.entry_cantidad.config(width=50, font=('Arial', 12))
        self.entry_cantidad.grid(row=2, column=1, padx=10, pady=10)

        self.mi_fecha = tk.StringVar()
        self.entry_fecha = tk.Entry(self, textvariable=self.mi_fecha)
        self.entry_fecha.config(width=50, font=('Arial', 12))
        self.entry_fecha.grid(row=3, column=1, padx=10, pady=10)

        self.boton_nuevo = tk.Button(self, text="Nuevo", command=self.habilitar_campos)
        self.boton_nuevo.config(width=20, font=('Arial', 12, 'bold'), fg='#fcf9f3', bg='#35ae0b', cursor='hand2', activebackground='#38a512')
        self.boton_nuevo.grid(row=4, column=0, padx=10, pady=10)

        self.boton_guardar = tk.Button(self, text="Guardar", command=self.guardar_datos)
        self.boton_guardar.config(width=20, font=('Arial', 12, 'bold'), fg='#fcf9f3', bg='#1461d2', cursor='hand2', activebackground='#125cc8')
        self.boton_guardar.grid(row=4, column=1, padx=10, pady=10)

        self.boton_cancelar = tk.Button(self, text="Cancelar", command=self.desabilitar_campos)
        self.boton_cancelar.config(width=20, font=('Arial', 12, 'bold'), fg='#fcf9f3', bg='#e30b3c', cursor='hand2', activebackground='#d40e3b')
        self.boton_cancelar.grid(row=4, column=2, padx=10, pady=10)

    def habilitar_campos(self):
        self.mi_cliente.set('')
        self.mi_producto_id.set('')
        self.mi_cantidad.set('')
        self.mi_fecha.set('')
        self.entry_cliente.config(state='normal')
        self.entry_producto.config(state='normal')
        self.entry_cantidad.config(state='normal')
        self.entry_fecha.config(state='normal')
        self.boton_guardar.config(state='normal')
        self.boton_cancelar.config(state='normal')

    def desabilitar_campos(self):
        self.id = None
        self.mi_cliente.set('')
        self.mi_producto_id.set('')
        self.mi_cantidad.set('')
        self.mi_fecha.set('')
        self.entry_cliente.config(state='disabled')
        self.entry_producto.config(state='disabled')
        self.entry_cantidad.config(state='disabled')
        self.entry_fecha.config(state='disabled')
        self.boton_guardar.config(state='disabled')
        self.boton_cancelar.config(state='disabled')

    def guardar_datos(self):
        reserva = Reserva(
            self.mi_cliente.get(),
            self.mi_producto_id.get(),
            self.mi_cantidad.get(),
            self.mi_fecha.get()
        )
        if self.id is None:
            guardar_reserva(reserva)
        else:
            editar_reserva(reserva, self.id)
        self.tabla_reservas()
        self.desabilitar_campos()

    def tabla_reservas(self):
        # Destruir tabla previa para evitar duplicados
        for widget in self.winfo_children():
            if isinstance(widget, ttk.Treeview):
                widget.destroy()

        self.lista_reservas = listar_reservas()
        self.tabla = ttk.Treeview(
            self, columns=('Cliente', 'Producto', 'Cantidad', 'Fecha')
        )
        self.tabla.grid(row=5, column=0, columnspan=3, sticky='nsew')

        self.tabla.heading('#0', text='ID', anchor='center')
        self.tabla.heading('#1', text='Cliente', anchor='center')
        self.tabla.heading('#2', text='Producto', anchor='center')
        self.tabla.heading('#3', text='Cantidad', anchor='center')
        self.tabla.heading('#4', text='Fecha', anchor='center')

        self.tabla.column('#0', width=50, anchor='center')
        self.tabla.column('#1', width=150, anchor='center')
        self.tabla.column('#2', width=150, anchor='center')
        self.tabla.column('#3', width=100, anchor='center')
        self.tabla.column('#4', width=100, anchor='center')

        for r in self.lista_reservas:
            self.tabla.insert('', 'end', text=r[0], values=(r[1], r[2], r[3], r[4]))

        # Scrollbar
        self.scroll = ttk.Scrollbar(self, orient='vertical', command=self.tabla.yview)
        self.scroll.grid(row=5, column=3, sticky='ns')
        self.tabla.configure(yscroll=self.scroll.set)