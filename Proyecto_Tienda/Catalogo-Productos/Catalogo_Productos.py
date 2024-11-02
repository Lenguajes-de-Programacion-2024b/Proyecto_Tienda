import tkinter as tk
def main():
    root = tk.Tk()
    root.title('Programa Tienda')
    root.iconbitmap('img/cp-logo.ico')
    root.resizable(0,0)

    frame = tk.Frame(root)
    frame.pack()
    frame.config(width=480, height=320, bg='red')
    root.mainloop()

if __name__ == '__main__':
    main()