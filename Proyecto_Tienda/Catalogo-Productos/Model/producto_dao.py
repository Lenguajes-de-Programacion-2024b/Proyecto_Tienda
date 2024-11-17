from .conexion_db import ConexionDB

def crear_tabla():
    conexion = ConexionDB()
    
    cursor = conexion.cursor 
    
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Productos')
        BEGIN
            CREATE TABLE productos (
                id INT PRIMARY KEY IDENTITY(1,1),
                nombre VARCHAR(100),
                precio DECIMAL(15, 2),
                cantidad INT
            )
        END
    ''')
    
    conexion.cerrar()

class Productos:
    def __init__(self, nombre, precio, cantidad):
        self.id = None
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    def __str__(self):
        return f'Productos[{self.nombre}, {self.precio}, {self.cantidad}]'
    
def guardar(producto):
    # Instanciar la conexión
    conexion = ConexionDB()  # Crear instancia de la conexión

    # SQL para insertar el producto
    sql = "INSERT INTO Productos (nombre, precio, cantidad) VALUES (?, ?, ?)"
    
    # Ejecutar la consulta con los parámetros
    conexion.cursor.execute(sql, (producto.nombre, producto.precio, producto.cantidad))
    
    # Guardar los cambios y cerrar la conexión
    conexion.cerrar()

def listar():
    conexion = ConexionDB()

    Lista_Productos = []
    sql = "SELECT*FROM  Productos"

    conexion.cursor.execute(sql)
    Lista_Productos = conexion.cursor.fetchall()
    conexion.cerrar()

    return Lista_Productos

def editar(producto, id):
    conexion = ConexionDB()

    sql = "UPDATE Productos SET nombre = ?, precio = ?, cantidad = ? WHERE id = ?"    
    conexion.cursor.execute(sql, (producto.nombre, producto.precio, producto.cantidad, id))
    conexion.cerrar()

def eliminar(id):
    conexion = ConexionDB()
    
    sql = "DELETE FROM Productos WHERE id = ?"
    conexion.cursor.execute(sql, (id,))
    conexion.cerrar()