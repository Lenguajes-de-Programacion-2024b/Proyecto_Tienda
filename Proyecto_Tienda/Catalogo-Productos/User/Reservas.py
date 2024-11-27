import tkinter as tk
from tkinter import ttk, messagebox
from Model.reserva_dao import Reserva, registrar_reserva, listar_reservas, listar, eliminar_reserva, actualizar_estado_reserva, listar_estados_reserva

class ReservasFrame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.pack(fill='both', expand=True)
        self.campos_reserva()
        self.tabla_reservas()
        self.crear_menu_contextual()

    def campos_reserva(self):
        # Etiqueta y combobox para Producto
        self.label_producto = tk.Label(self, text='Producto:')
        self.label_producto.config(font=('Arial', 12, 'bold'))
        self.label_producto.grid(row=0, column=0, padx=10, pady=10)

        self.producto_id = tk.StringVar()

        self.combobox_producto = ttk.Combobox(self, textvariable=self.producto_id, state="readonly", font=('Arial', 12))
        self.actualizar_productos()
        self.combobox_producto.grid(row=0, column=1, padx=10, pady=10)

        # Etiqueta y entrada para Cantidad
        self.label_cantidad = tk.Label(self, text='Cantidad:')
        self.label_cantidad.config(font=('Arial', 12, 'bold'))
        self.label_cantidad.grid(row=1, column=0, padx=10, pady=10)

        self.cantidad_reserva = tk.StringVar()
        self.entry_cantidad = tk.Entry(self, textvariable=self.cantidad_reserva)
        self.entry_cantidad.config(width=50, font=('Arial', 12))
        self.entry_cantidad.grid(row=1, column=1, padx=10, pady=10)

        # Etiqueta y entrada para Cliente
        self.label_cliente = tk.Label(self, text='Cliente:')
        self.label_cliente.config(font=('Arial', 12, 'bold'))
        self.label_cliente.grid(row=2, column=0, padx=10, pady=10)

        self.cliente = tk.StringVar()
        self.entry_cliente = tk.Entry(self, textvariable=self.cliente)
        self.entry_cliente.config(width=50, font=('Arial', 12))
        self.entry_cliente.grid(row=2, column=1, padx=10, pady=10)

        # Botón para Registrar Reserva
        self.boton_registrar_reserva = tk.Button(self, text="Registrar Reserva", command=self.registrar_reserva)
        self.boton_registrar_reserva.config(width=20, font=('Arial', 12, 'bold'), fg='#fcf9f3', bg='#1461d2', cursor='hand2')
        self.boton_registrar_reserva.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def actualizar_productos(self):
        productos = listar()  # Asumiendo que 'listar' devuelve productos
        self.combobox_producto['values'] = [f"{p[0]} - {p[1]}" for p in productos]

    def registrar_reserva(self):
        try:
            producto_id_texto = self.producto_id.get()
            cantidad = int(self.cantidad_reserva.get())
            cliente = self.cliente.get().strip()

            if not producto_id_texto:
                raise ValueError("Debe seleccionar un producto.")
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a 0.")
            if not cliente:
                raise ValueError("Debe ingresar el nombre del cliente.")

            producto_id = int(producto_id_texto.split(" - ")[0])

            nueva_reserva = Reserva(producto_id, cantidad, cliente)
            registrar_reserva(nueva_reserva)

            # Refrescar la tabla y seleccionar automáticamente la nueva reserva
            self.tabla_reservas()  # Recargar datos en la tabla

            # Obtener el ID de la reserva recién creada
            lista_reservas = listar_reservas()
            nueva_reserva_id = lista_reservas[-1][0]  # Asumimos que el último elemento es la nueva reserva

            # Seleccionar automáticamente la nueva reserva en la tabla
            for item in self.tabla.get_children():
                if self.tabla.item(item)['text'] == nueva_reserva_id:
                    self.tabla.selection_set(item)
                    self.tabla.focus(item)
                    break

            # Limpiar los campos del formulario
            self.cantidad_reserva.set('')
            self.producto_id.set('')
            self.cliente.set('')
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def cambiar_estado_reserva(self, nuevo_estado_id):
        try:
            # Obtener la reserva seleccionada en la tabla
            reserva_id = self.tabla.item(self.tabla.selection())['text']

            if not reserva_id:
                raise ValueError("Debe seleccionar una reserva para cambiar su estado.")

            # Llamar a la función del modelo para actualizar el estado
            actualizar_estado_reserva(reserva_id, nuevo_estado_id)

            # Mensaje según el estado actualizado
            if nuevo_estado_id == 3:  # Estado Cancelado
                messagebox.showinfo("Reserva Cancelada", "La reserva fue cancelada y el stock se ha devuelto.")
            else:
                messagebox.showinfo("Estado Actualizado", "El estado de la reserva se actualizó correctamente.")

            # Refrescar la tabla de reservas
            self.refrescar_tabla()

        except IndexError:
            messagebox.showerror("Error", "Debe seleccionar una reserva para cambiar su estado.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def refrescar_tabla(self):
        """
        Refrescar la tabla sin bloquear nuevas interacciones.
        """
        # Limpiar la tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        # Recargar los datos en la tabla
        self.lista_reservas = listar_reservas()
        for r in self.lista_reservas:
            fecha_formateada = r[4].strftime("%d/%m/%Y")  # Formatear para mostrar solo la fecha
            self.tabla.insert('', 'end', text=r[0], values=(r[1], r[2], r[3], fecha_formateada, r[5]))

        # Liberar cualquier selección previa si existe
        if self.tabla.selection():
            self.tabla.selection_remove(self.tabla.selection())

        # Forzar la actualización de la interfaz
        self.update_idletasks()

    def tabla_reservas(self):
        # Destruir cualquier tabla previa para evitar duplicados
        for widget in self.winfo_children():
            if isinstance(widget, ttk.Treeview):
                widget.destroy()
            if isinstance(widget, ttk.Scrollbar):
                widget.destroy()

        # Crear el estilo para la tabla con bordes y centrado
        style = ttk.Style()
        style.configure(
            "Treeview",
            borderwidth=1,
            relief="solid",
            rowheight=30,  # Altura de las filas
            font=('Arial', 12),  # Fuente de los datos en la tabla
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
        self.lista_reservas = listar_reservas()
        self.tabla = ttk.Treeview(
            self, columns=('Producto', 'Cantidad', 'Cliente', 'Fecha Reserva', 'Estado'), style="Treeview"
        )
        self.tabla.grid(row=4, column=0, columnspan=2, sticky='nsew', padx=(10, 0))  # Espacio izquierdo

        # Encabezados de las columnas
        self.tabla.heading('#0', text='ID', anchor='center')
        self.tabla.heading('#1', text='Producto', anchor='center')
        self.tabla.heading('#2', text='Cantidad', anchor='center')
        self.tabla.heading('#3', text='Cliente', anchor='center')
        self.tabla.heading('#4', text='Fecha Reserva', anchor='center')
        self.tabla.heading('#5', text='Estado', anchor='center')

        # Configurar las columnas con más espacio y centrado
        self.tabla.column('#0', width=50, anchor='center')  # Columna ID
        self.tabla.column('#1', width=200, anchor='center')  # Producto
        self.tabla.column('#2', width=100, anchor='center')  # Cantidad
        self.tabla.column('#3', width=150, anchor='center')  # Cliente
        self.tabla.column('#4', width=150, anchor='center')  # Fecha Reserva
        self.tabla.column('#5', width=100, anchor='center')  # Estado

        # Insertar las filas con formato
        for r in self.lista_reservas:
            fecha_formateada = r[4].strftime("%d/%m/%Y")  # Formatear para mostrar solo la fecha
            self.tabla.insert('', 'end', text=r[0], values=(r[1], r[2], r[3], fecha_formateada, r[5]))

        # Agregar scroll vertical
        self.scroll = ttk.Scrollbar(self, orient='vertical', command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=self.scroll.set)
        self.scroll.grid(row=4, column=2, sticky='ns')

        # Botón Eliminar Reserva
        self.boton_eliminar_reserva = tk.Button(self, text="Eliminar Reserva", command=self.eliminar_reserva)
        self.boton_eliminar_reserva.config(
            width=20, font=('Arial', 12, 'bold'), fg='#fcf9f3', bg='#e30b3c', cursor='hand2'
        )
        self.boton_eliminar_reserva.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def eliminar_reserva(self):
        try:
            # Obtener la reserva seleccionada en la tabla
            reserva_id = self.tabla.item(self.tabla.selection())['text']

            if not reserva_id:
                raise ValueError("Debe seleccionar una reserva para eliminar.")

            # Confirmar eliminación
            confirmacion = messagebox.askyesno("Confirmación", "¿Está seguro de eliminar esta reserva?")
            if not confirmacion:
                return

            # Llamar a la función del modelo para eliminar
            eliminar_reserva(reserva_id)

            # Actualizar la tabla de reservas
            self.tabla_reservas()
            messagebox.showinfo("Éxito", "La reserva se eliminó correctamente.")
        except IndexError:
            messagebox.showerror("Error", "Debe seleccionar una reserva para eliminar.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
    
    def crear_menu_contextual(self):
        # Crear el menú
        self.menu_contextual = tk.Menu(self, tearoff=0)
        estados = listar_estados_reserva()  # Obtener los estados disponibles desde la base de datos

        # Añadir opciones para cada estado
        for estado in estados:
            self.menu_contextual.add_command(
                label=f"Cambiar a '{estado[1]}'",
                command=lambda estado_id=estado[0]: self.cambiar_estado_reserva(estado_id)
            )

        # Asociar evento de clic derecho en la tabla
        self.tabla.bind("<Button-3>", self.mostrar_menu_contextual)

    def mostrar_menu_contextual(self, event):
        try:
            # Seleccionar el elemento debajo del clic derecho
            item = self.tabla.identify_row(event.y)
            if item:
                self.tabla.selection_set(item)
                self.menu_contextual.post(event.x_root, event.y_root)
        finally:
            # Cerrar el menú contextual si no hay selección válida
            self.menu_contextual.grab_release()