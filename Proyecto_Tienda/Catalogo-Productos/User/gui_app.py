import tkinter as tk
from Model.producto_dao import crear_tabla
from Model.ventas_dao import crear_tabla_ventas
from User.Productos import ProductosFrame
from User.Ventas import VentasFrame

def barra_menu(root):
    barra_menu = tk.Menu(root)
    root.config(menu=barra_menu)

    menu_inicio = tk.Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label='Inicio', menu=menu_inicio)

    menu_inicio.add_command(label='Crear registro en DB', command=crear_tabla)
    menu_inicio.add_command(label='Eliminar registro en DB', command = crear_tabla_ventas )
    menu_inicio.add_command(label='Abrir Productos', command=lambda: abrir_productos(root))
    menu_inicio.add_command(label='Abrir ventas', command=lambda: abrir_ventas(root))
    menu_inicio.add_command(label='Salir', command=root.quit)

    barra_menu.add_cascade(label='Consultas')
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

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Programa Tienda")
    barra_menu(root)
    abrir_productos(root)
    root.mainloop()