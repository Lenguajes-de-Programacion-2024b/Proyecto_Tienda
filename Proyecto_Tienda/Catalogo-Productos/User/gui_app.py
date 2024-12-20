import tkinter as tk
from Model.producto_dao import crear_tabla
from Model.ventas_dao import crear_tabla_ventas
from Model.reserva_dao import crear_tabla_reservas
from Model.pagos_dao import crear_tabla_pagos
from Model.cuentas_credito_dao import crear_tabla_Cuentas
from User.Productos import ProductosFrame
from User.Ventas import VentasFrame
from User.informes_ventas import InformeVentas
from User.Reservas import ReservasFrame
from User.Pagos import PagosFrame
from User.Cuentas import CuentasCreditoFrame
from User.Topventas import mostrar_mas_vendidos_gui, mostrar_menos_vendidos_gui



def barra_menu(root):
    barra_menu = tk.Menu(root)
    root.config(menu=barra_menu)

    menu_inicio = tk.Menu(barra_menu, tearoff=0)
    menu_ventas = tk.Menu(barra_menu, tearoff=0)
    menu_reserva = tk.Menu(barra_menu, tearoff=0)
    menu_pagos = tk.Menu(barra_menu, tearoff=0)
    menu_consultas = tk.Menu(barra_menu, tearoff=0)
    menu_cuentas = tk.Menu(barra_menu, tearoff=0)
    
    barra_menu.add_cascade(label='Productos', menu=menu_inicio)
    menu_inicio.add_command(label='Crear tabla en DB', command=crear_tabla)
    menu_inicio.add_command(label='Abrir Productos', command=lambda: abrir_productos(root))

    barra_menu.add_cascade(label='Ventas', menu=menu_ventas)
    menu_ventas.add_command(label='Crear tabla en DB', command=crear_tabla_ventas )
    menu_ventas.add_command(label='Abrir ventas', command=lambda: abrir_ventas(root))
    menu_ventas.add_command(label='Informe ventas', command=lambda: Informe_ventas(root))

    barra_menu.add_cascade(label='Reservas', menu=menu_reserva)
    menu_reserva.add_command(label='Crear tabla reservas en DB', command=crear_tabla_reservas)
    menu_reserva.add_command(label='Abrir Reservas', command=lambda: abrir_reservas(root))

    barra_menu.add_cascade(label='Pagos', menu=menu_pagos)
    menu_pagos.add_command(label='Crear tabla reservas en DB', command=crear_tabla_pagos)
    menu_pagos.add_command(label='Abrir Pagos', command=lambda: abrir_pagos(root))

    barra_menu.add_cascade(label='Cuentas credito', menu=menu_cuentas)
    menu_cuentas.add_command(label='Crear tabla en DB', command=crear_tabla_Cuentas)
    menu_cuentas.add_command(label='Abrir Cuentas credito clientes', command=lambda: abrir_cuentas(root))

    barra_menu.add_cascade(label='Consultas', menu=menu_consultas)
    menu_consultas.add_command(label='Productos más vendidos', command=lambda: mostrar_mas_vendidos_gui(root))
    menu_consultas.add_command(label='Productos menos vendidos', command=lambda: mostrar_menos_vendidos_gui(root))

    barra_menu.add_cascade(label='Configuración')

def abrir_productos(root):
    # Eliminar todos los widgets previos en el contenedor principal, pero dejar el menú
    for widget in root.winfo_children():
        if isinstance(widget, tk.Menu):  # No eliminar el menú
            continue
        widget.destroy()

    # Crear el nuevo frame de productos
    ProductosFrame(root)

def abrir_ventas(root):
    for widget in root.winfo_children():
        if isinstance(widget, tk.Menu):  # No eliminar el menú
            continue
        widget.destroy()

    # Crear el nuevo frame de productos
    VentasFrame(root)

def Informe_ventas(root):
    for widget in root.winfo_children():
        if isinstance(widget, tk.Menu):  # No eliminar el menú
            continue
        widget.destroy()

    # Crear el nuevo frame de productos
    InformeVentas(root)

def abrir_reservas(root):
    for widget in root.winfo_children():
        if isinstance(widget, tk.Menu):  # No eliminar el menú
            continue
        widget.destroy()

    # Crear el nuevo frame de productos
    ReservasFrame(root)

def abrir_pagos(root):
    for widget in root.winfo_children():
        if isinstance(widget, tk.Menu):  # No eliminar el menú
            continue
        widget.destroy()

    # Crear el nuevo frame de productos
    PagosFrame(root)

def abrir_cuentas(root):
    for widget in root.winfo_children():
        if isinstance(widget, tk.Menu):  # No eliminar el menú
            continue
        widget.destroy()

    # Crear el nuevo frame de productos
    CuentasCreditoFrame(root)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Programa Tienda")
    barra_menu(root)
    abrir_productos(root)
    root.mainloop()