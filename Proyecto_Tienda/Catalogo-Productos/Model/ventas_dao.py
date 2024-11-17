from .conexion_db import ConexionDB

def crear_tabla_ventas():
    conexion = ConexionDB()
    cursor = conexion.cursor
    
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Ventas')
        BEGIN
            CREATE TABLE Ventas (
                id INT PRIMARY KEY IDENTITY(1,1),
                producto_id INT,
                cantidad INT,
                fecha DATETIME DEFAULT GETDATE(),
                total_vendido DECIMAL(10, 2),
                FOREIGN KEY (producto_id) REFERENCES Productos(id)
            )
        END
    ''')
    
    conexion.cerrar()

class Venta:
    def __init__(self, producto_id, cantidad, total_vendido=None):
        self.id = None
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.total_vendido = total_vendido
        self.fecha = None

def registrar_venta(venta):
    conexion = ConexionDB()

    # Obtener el precio unitario del producto
    consulta_precio = "SELECT precio FROM Productos WHERE id = ?"
    conexion.cursor.execute(consulta_precio, (venta.producto_id,))
    producto = conexion.cursor.fetchone()

    if not producto:
        conexion.cerrar()
        raise ValueError("El producto no existe.")
    
    precio_unitario = producto[0]
    total_vendido = precio_unitario * venta.cantidad

    # Verificar si hay suficiente cantidad en el inventario
    consulta_cantidad = "SELECT cantidad FROM Productos WHERE id = ?"
    conexion.cursor.execute(consulta_cantidad, (venta.producto_id,))
    stock_disponible = conexion.cursor.fetchone()[0]

    if stock_disponible >= venta.cantidad:
        # Registrar la venta
        sql_venta = "INSERT INTO Ventas (producto_id, cantidad, total_vendido) VALUES (?, ?, ?)"
        conexion.cursor.execute(sql_venta, (venta.producto_id, venta.cantidad, total_vendido))

        # Actualizar el stock del producto
        sql_actualizar_stock = "UPDATE Productos SET cantidad = cantidad - ? WHERE id = ?"
        conexion.cursor.execute(sql_actualizar_stock, (venta.cantidad, venta.producto_id))

        conexion.cerrar()
    else:
        conexion.cerrar()
        raise ValueError("No hay suficiente stock disponible.")
    
def listar():
    conexion = ConexionDB()
    sql = "SELECT id, nombre FROM Productos"  # Ajusta según los campos de tu tabla
    conexion.cursor.execute(sql)
    productos = conexion.cursor.fetchall()  # Devuelve una lista de tuplas [(id, nombre), ...]
    conexion.cerrar()
    return productos

def listar_ventas():
    conexion = ConexionDB()
    sql = '''
        SELECT v.id, p.nombre, v.cantidad, v.fecha, v.total_vendido
        FROM Ventas v
        INNER JOIN Productos p ON v.producto_id = p.id
    '''
    conexion.cursor.execute(sql)
    ventas = conexion.cursor.fetchall()
    conexion.cerrar()
    return ventas


def eliminar_venta(id):
    conexion = ConexionDB()

    # Primero, obtenemos la venta que estamos eliminando
    consulta_venta = "SELECT producto_id, cantidad FROM Ventas WHERE id = ?"
    conexion.cursor.execute(consulta_venta, (id,))
    venta = conexion.cursor.fetchone()

    if venta:
        producto_id = venta[0]
        cantidad_vendida = venta[1]

        # Ahora, eliminamos la venta
        sql_eliminar = "DELETE FROM Ventas WHERE id = ?"
        conexion.cursor.execute(sql_eliminar, (id,))

        # Actualizamos el stock en la tabla Productos
        sql_actualizar_stock = "UPDATE Productos SET cantidad = cantidad + ? WHERE id = ?"
        conexion.cursor.execute(sql_actualizar_stock, (cantidad_vendida, producto_id))

    conexion.cerrar()