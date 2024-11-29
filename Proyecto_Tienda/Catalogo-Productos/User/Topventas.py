import tkinter as tk
from tkinter import ttk
from Model.Topvendidos import mostrar_mas_vendidos, mostrar_menos_vendidos

def mostrar_mas_vendidos_gui(root):
    
    productos_mas_vendidos = mostrar_mas_vendidos()

    
    ventana_mas_vendidos = tk.Toplevel(root)
    ventana_mas_vendidos.title("Productos más vendidos")
    ventana_mas_vendidos.geometry("500x400")  
    ventana_mas_vendidos.resizable(False, False)  
    ventana_mas_vendidos.config(bg="#f0f0f0")  

    
    frame = tk.Frame(ventana_mas_vendidos, bg="#f0f0f0")
    frame.pack(pady=20, padx=20)

    
    tree = ttk.Treeview(frame, columns=("Producto", "Cantidad Vendida"), show="headings")
    tree.heading("Producto", text="Producto")
    tree.heading("Cantidad Vendida", text="Cantidad Vendida")
    
    
    tree.column("Producto", width=250, anchor="w")
    tree.column("Cantidad Vendida", width=150, anchor="center")

    
    for producto in productos_mas_vendidos:
        tree.insert("", "end", values=(producto[0], producto[1]))

    tree.pack(fill="both", expand=True)

def mostrar_menos_vendidos_gui(root):
    
    productos_menos_vendidos = mostrar_menos_vendidos()

    
    ventana_menos_vendidos = tk.Toplevel(root)
    ventana_menos_vendidos.title("Productos menos vendidos")
    ventana_menos_vendidos.geometry("500x400")  
    ventana_menos_vendidos.resizable(False, False)  
    ventana_menos_vendidos.config(bg="#f0f0f0")  

    
    frame = tk.Frame(ventana_menos_vendidos, bg="#f0f0f0")
    frame.pack(pady=20, padx=20)

    
    tree = ttk.Treeview(frame, columns=("Producto", "Cantidad Vendida"), show="headings")
    tree.heading("Producto", text="Producto")
    tree.heading("Cantidad Vendida", text="Cantidad Vendida")
    
    
    tree.column("Producto", width=250, anchor="w")
    tree.column("Cantidad Vendida", width=150, anchor="center")

    
    for producto in productos_menos_vendidos:
        tree.insert("", "end", values=(producto[0], producto[1]))

    tree.pack(fill="both", expand=True)
