import tkinter as tk
from User.gui_app import ProductosFrame, barra_menu


def main():
    root = tk.Tk()
    root.title('Programa Tienda')
    root.iconbitmap('img/cp-logo.ico')
    root.resizable(0,0)
    
    barra_menu(root)

    app = ProductosFrame(root = root)

    app.mainloop()

if __name__ == '__main__':
    main()