import tkinter as tk
from tkinter import ttk

def barra_menu(root):
    barra_menu = tk.Menu(root)
    root.config(menu = barra_menu, width=300, height=300)

    menu_inicio = tk.Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label='Inicio', menu= menu_inicio)

    menu_inicio.add_command(label='Crear registro en DB')
    menu_inicio.add_command(label='Eliminar registro en DB')
    menu_inicio.add_command(label='Salir', command = root.destroy)

    barra_menu.add_cascade(label='Consultas')
    barra_menu.add_cascade(label='Configuracion')

class Frame(tk.Frame):
    def  __init__(self, root = None):
        super().__init__(root)
        self.root = root
        self.pack()
        self.config(width=480, height=320)

        self.campos_productos()
        self.desabilitar_campos()
        self.tabla_productos()

    def campos_productos(self):
        #Labels de cada campo
        self.label_nombre=tk.Label(self, text = 'Nombre:')
        self.label_nombre.config(font = ('Arial', 12, 'bold'))
        self.label_nombre.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.label_precio=tk.Label(self, text = 'Precio:')
        self.label_precio.config(font = ('Arial', 12, 'bold'))
        self.label_precio.grid(row = 1, column = 0, padx = 10, pady = 10)

        self.label_cantidad=tk.Label(self, text = 'Cantidad:')
        self.label_cantidad.config(font = ('Arial', 12, 'bold'))
        self.label_cantidad.grid(row = 2, column = 0, padx = 10, pady = 10)

        #Entrys de cada campo
        self.mi_nombre = tk.StringVar()
        self.entry_nombre = tk.Entry(self, textvariable=self.mi_nombre)
        self.entry_nombre.config(width = 50, font = ('Arial', 12))
        self.entry_nombre.grid(row = 0, column = 1, padx = 10, pady = 10, columnspan = 2)

        self.mi_precio = tk.StringVar()
        self.entry_precio = tk.Entry(self, textvariable=self.mi_precio)
        self.entry_precio.config(width = 50, font = ('Arial', 12))
        self.entry_precio.grid(row = 1, column = 1, padx = 10, pady = 10, columnspan = 2)

        self.mi_cantidad = tk.StringVar()
        self.entry_cantidad = tk.Entry(self, textvariable=self.mi_cantidad)
        self.entry_cantidad.config(width = 50, font = ('Arial', 12))
        self.entry_cantidad.grid(row = 2, column = 1, padx = 10, pady = 10, columnspan = 2)

        #Botones
        self.boton_nuevo = tk.Button(self, text = "Nuevo",  command = self.habilitar_campos)
        self.boton_nuevo.config(width = 20, font = ('Arial', 12, 'bold'), fg = '#fcf9f3', bg = '#35ae0b', cursor =  'hand2', activebackground= '#38a512')
        self.boton_nuevo.grid(row = 3, column = 0, padx = 10, pady = 10)

        self.boton_guardar = tk.Button(self, text = "Guardar", command = self.guardar_datos)
        self.boton_guardar.config(width = 20, font = ('Arial', 12, 'bold'), fg = '#fcf9f3', bg = '#1461d2', cursor =  'hand2', activebackground= '#125cc8')
        self.boton_guardar.grid(row = 3, column = 1, padx = 10, pady = 10)

        self.boton_cancelar = tk.Button(self, text = "Cancelar", command = self.desabilitar_campos)
        self.boton_cancelar.config(width = 20, font = ('Arial', 12, 'bold'), fg = '#fcf9f3', bg = '#e30b3c', cursor =  'hand2', activebackground= '#d40e3b')
        self.boton_cancelar.grid(row = 3, column = 2, padx = 10, pady = 10)

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
        self.mi_nombre.set('')
        self.mi_precio.set('')
        self.mi_cantidad.set('')

        self.entry_nombre.config(state='disabled')
        self.entry_precio.config(state='disabled')
        self.entry_cantidad.config(state='disabled')

        self.boton_guardar.config(state='disabled')
        self.boton_cancelar.config(state='disabled')

    def guardar_datos(self):

        self.desabilitar_campos()

    def tabla_productos(self):

        self.tabla = ttk.Treeview(self,
        column = ('Nombre', 'Precio', 'Cantidad'))
        self.tabla.grid(row=4, column=0, columnspan=4)

        self.tabla.heading('#0', text='ID')
        self.tabla.heading('#1', text='NOMBRE')
        self.tabla.heading('#2', text='PRECIO')
        self.tabla.heading('#3', text='CANTIDAD')

        self.tabla.insert('',0,text='1', values= ('Arina Pan', '$12000', '20'))

        #Boton Editar
        self.boton_editar = tk.Button(self, text = "Editar")
        self.boton_editar.config(width = 20, font = ('Arial', 12, 'bold'), fg = '#fcf9f3', bg = '#35ae0b', cursor =  'hand2', activebackground= '#38a512')
        self.boton_editar.grid(row = 5, column = 0, padx = 10, pady = 10)

        #Boton Eliminar
        self.boton_eliminar = tk.Button(self, text = "Eliminar")
        self.boton_eliminar.config(width = 20, font = ('Arial', 12, 'bold'), fg = '#fcf9f3', bg = '#e30b3c', cursor =  'hand2', activebackground= '#d40e3b')
        self.boton_eliminar.grid(row = 5, column = 1, padx = 10, pady = 10)





