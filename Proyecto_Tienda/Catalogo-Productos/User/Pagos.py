import tkinter as tk
from tkinter import ttk, messagebox
from Model.pagos_dao import Pago, registrar_pago, listar_pagos, listar_metodos_pago

class PagosFrame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.pack(fill='both', expand=True)
        self.metodos_pago = {}
        self.campos_pago()
        self.tabla_pagos()

    def campos_pago(self):
        # Labels estilizados
        self.label_reserva = tk.Label(self, text='ID de Reserva:')
        self.label_reserva.config(font=('Arial', 12, 'bold'))
        self.label_reserva.grid(row=0, column=0, padx=10, pady=10)

        self.reserva_id = tk.StringVar()
        self.combobox_reserva = ttk.Combobox(self, textvariable=self.reserva_id, state="readonly")
        self.combobox_reserva.config(font=('Arial', 12), width=25)  # Fuente consistente con el estilo
        self.actualizar_reservas_confirmadas()
        self.combobox_reserva.grid(row=0, column=1, padx=10, pady=10)

        self.label_metodo_pago = tk.Label(self, text='Método de Pago:')
        self.label_metodo_pago.config(font=('Arial', 12, 'bold'))
        self.label_metodo_pago.grid(row=1, column=0, padx=10, pady=10)

        self.metodo_pago = tk.StringVar()
        self.combobox_metodo_pago = ttk.Combobox(self, textvariable=self.metodo_pago, state="readonly")
        self.combobox_metodo_pago.config(font=('Arial', 12), width=25)  # Fuente consistente con el estilo
        self.actualizar_metodos_pago()
        self.combobox_metodo_pago.grid(row=1, column=1, padx=10, pady=10)

        self.label_medio_entrega = tk.Label(self, text='Medio de Entrega:')
        self.label_medio_entrega.config(font=('Arial', 12, 'bold'))
        self.label_medio_entrega.grid(row=2, column=0, padx=10, pady=10)

        self.medio_entrega = tk.StringVar()
        self.combobox_medio_entrega = ttk.Combobox(self, textvariable=self.medio_entrega, state="readonly")
        self.combobox_medio_entrega['values'] = ['Físico', 'Domicilio']
        self.combobox_medio_entrega.config(font=('Arial', 12), width=25)  # Fuente consistente con el estilo
        self.combobox_medio_entrega.grid(row=2, column=1, padx=10, pady=10)

        # Botones estilizados
        self.boton_registrar_pago = tk.Button(self, text="Registrar Pago", command=self.registrar_pago)
        self.boton_registrar_pago.config(width=20, font=('Arial', 12, 'bold'), fg='#fcf9f3', bg='#35ae0b', 
                                         cursor='hand2', activebackground='#38a512')
        self.boton_registrar_pago.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def actualizar_reservas_confirmadas(self):
        from Model.pagos_dao import listar_reservas_confirmadas
        reservas = listar_reservas_confirmadas()
        self.reservas_confirmadas = {f"{r[0]} - {r[1]}": r[0] for r in reservas}
        self.combobox_reserva['values'] = list(self.reservas_confirmadas.keys())

    def registrar_pago(self):
        try:
            reserva_desc = self.reserva_id.get()
            if not reserva_desc:
                raise ValueError("Debe seleccionar una reserva.")

            reserva_id = self.reservas_confirmadas.get(reserva_desc)  # Obtener el ID real de la reserva
            metodo_pago_desc = self.metodo_pago.get()
            medio_entrega = self.medio_entrega.get()

            if not metodo_pago_desc:
                raise ValueError("Debe seleccionar un método de pago.")
            if not medio_entrega:
                raise ValueError("Debe seleccionar un medio de entrega.")

            metodo_pago_id = self.metodos_pago.get(metodo_pago_desc)  # Obtener el ID del método de pago
            if not metodo_pago_id:
                raise ValueError("Método de pago seleccionado no válido.")

            # Validar si ya existe un pago para esta reserva
            from Model.pagos_dao import listar_pagos
            pagos = listar_pagos()
            for pago in pagos:
                if pago[1] == reserva_id:
                    raise ValueError("Ya existe un pago registrado para esta reserva.")

            # Definir estado y fecha de pago dependiendo del método
            if metodo_pago_desc == "Contra entrega":
                estado_pago = "Pendiente"
                fecha_pago = None
            else:
                estado_pago = "Pagado"
                from datetime import datetime
                fecha_pago = datetime.now()

            # Registrar el nuevo pago
            nuevo_pago = Pago(reserva_id, metodo_pago_id, medio_entrega, estado_pago, fecha_pago)
            registrar_pago(nuevo_pago)

            messagebox.showinfo("Éxito", "Pago registrado correctamente.")
            self.tabla_pagos()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def actualizar_metodos_pago(self):
        metodos = listar_metodos_pago()
        self.metodos_pago = {m[1]: m[0] for m in metodos}  # Diccionario {descripcion: id}
        self.combobox_metodo_pago['values'] = list(self.metodos_pago.keys())

    def actualizar_estado_pago(self):
        try:
            # Obtener el ID del pago seleccionado
            item_seleccionado = self.tabla.selection()[0]
            pago_id = self.tabla.item(item_seleccionado, 'text')

            if not pago_id:
                raise ValueError("Debe seleccionar un pago para actualizar.")

            # Llamar al modelo para actualizar el estado del pago
            from Model.pagos_dao import actualizar_estado_pago
            actualizar_estado_pago(pago_id)

            # Refrescar la tabla de pagos
            self.tabla_pagos()
            messagebox.showinfo("Éxito", "El estado del pago se actualizó a 'Pagado'. La venta se registró correctamente.")
        except IndexError:
            messagebox.showerror("Error", "Debe seleccionar un pago.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def tabla_pagos(self):
        # Eliminar widgets existentes si la tabla ya se creó
        for widget in self.winfo_children():
            if isinstance(widget, ttk.Treeview):
                widget.destroy()

        # Crear tabla
        self.tabla = ttk.Treeview(
            self, columns=('Reserva ID', 'Cliente', 'Método de Pago', 'Medio de Entrega', 'Estado de Pago', 'Fecha de Pago'), style="Treeview"
        )
        self.tabla.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Configurar encabezados de las columnas
        self.tabla.heading('#0', text='ID Pago', anchor='center')
        self.tabla.heading('#1', text='Reserva ID', anchor='center')
        self.tabla.heading('#2', text='Cliente', anchor='center')
        self.tabla.heading('#3', text='Método de Pago', anchor='center')
        self.tabla.heading('#4', text='Medio de Entrega', anchor='center')
        self.tabla.heading('#5', text='Estado de Pago', anchor='center')
        self.tabla.heading('#6', text='Fecha de Pago', anchor='center')

        # Configurar las columnas
        self.tabla.column('#0', width=80, anchor='center')
        self.tabla.column('#1', width=100, anchor='center')
        self.tabla.column('#2', width=150, anchor='center')
        self.tabla.column('#3', width=150, anchor='center')
        self.tabla.column('#4', width=150, anchor='center')
        self.tabla.column('#5', width=120, anchor='center')
        self.tabla.column('#6', width=150, anchor='center')

        # Poblar los datos
        pagos = listar_pagos()
        for pago in pagos:
            pago_id = pago[0]
            reserva_id = pago[1]
            cliente = pago[2]
            metodo_pago = pago[3]
            medio_entrega = pago[4]
            estado_pago = pago[5]
            fecha_pago = pago[6].strftime("%d/%m/%Y %H:%M") if pago[6] else "Sin confirmar"
            self.tabla.insert('', 'end', text=pago_id, values=(reserva_id, cliente, metodo_pago, medio_entrega, estado_pago, fecha_pago))

        # Botón para actualizar el estado del pago debajo de la tabla
        self.boton_actualizar_estado = tk.Button(self, text="Marcar como Pagado", command=self.actualizar_estado_pago)
        self.boton_actualizar_estado.config(width=20, font=('Arial', 12, 'bold'), fg='#fcf9f3', bg='#1461d2', 
                                            cursor='hand2', activebackground='#125cc8')
        self.boton_actualizar_estado.grid(row=5, column=0, columnspan=2, padx=10, pady=10)