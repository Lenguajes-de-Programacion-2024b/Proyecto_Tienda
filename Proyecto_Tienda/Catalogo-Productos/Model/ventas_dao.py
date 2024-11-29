from .conexion_db import ConexionDB
from datetime import datetime, timedelta

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
            cliente NVARCHAR(100),
            metodo_pago_id INT,
            fecha DATETIME DEFAULT GETDATE(),
            total_vendido DECIMAL(10, 2),
            FOREIGN KEY (producto_id) REFERENCES Productos(id),
            FOREIGN KEY (metodo_pago_id) REFERENCES MetodosPago(id)
        )
        END
    ''')
    
    conexion.cerrar()

class Venta:
    def __init__(self, producto_id, cantidad, cliente, metodo_pago_id, total_vendido=None):
        self.id = None
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.cliente = cliente
        self.metodo_pago_id = metodo_pago_id
        self.total_vendido = total_vendido
        self.fecha = None

def registrar_venta(venta, descontar_inventario=True):
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

    if descontar_inventario:
        # Verificar si hay suficiente cantidad en el inventario
        consulta_cantidad = "SELECT cantidad FROM Productos WHERE id = ?"
        conexion.cursor.execute(consulta_cantidad, (venta.producto_id,))
        stock_disponible = conexion.cursor.fetchone()[0]

        if stock_disponible < venta.cantidad:
            conexion.cerrar()
            raise ValueError("No hay suficiente stock disponible.")

        # Actualizar el stock si es necesario
        sql_actualizar_stock = "UPDATE Productos SET cantidad = cantidad - ? WHERE id = ?"
        conexion.cursor.execute(sql_actualizar_stock, (venta.cantidad, venta.producto_id))

    # Registrar la venta con metodo_pago_id
    sql_venta = """
        INSERT INTO Ventas (producto_id, cantidad, cliente, metodo_pago_id, total_vendido) 
        VALUES (?, ?, ?, ?, ?)
    """
    conexion.cursor.execute(sql_venta, (venta.producto_id, venta.cantidad, venta.cliente, venta.metodo_pago_id, total_vendido))

    conexion.cerrar()

def registrar_venta_multiple(ventas):
    """
    Registra múltiples productos para una venta. 
    Cada producto se registra como una venta independiente.
    
    :param ventas: Lista de objetos Venta.
    """
    for venta in ventas:
        registrar_venta(venta)
    
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
        SELECT v.id, p.nombre, v.cantidad, v.cliente, m.descripcion AS metodo_pago, v.fecha, v.total_vendido
        FROM Ventas v
        INNER JOIN Productos p ON v.producto_id = p.id
        INNER JOIN MetodosPago m ON v.metodo_pago_id = m.id
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

def listar_ventas_por_rango(fecha_inicio, fecha_fin):
    conexion = ConexionDB()
    sql = '''
        SELECT v.id, p.nombre, v.cantidad, v.fecha, v.total_vendido
        FROM Ventas v
        INNER JOIN Productos p ON v.producto_id = p.id
        WHERE v.fecha BETWEEN ? AND ?
    '''
    conexion.cursor.execute(sql, (fecha_inicio, fecha_fin))
    ventas = conexion.cursor.fetchall()
    conexion.cerrar()
    return ventas

def obtener_rango(periodo, fecha=None):
    if periodo == "diario":
        if fecha:
            fecha_inicio = datetime.strptime(fecha, "%Y-%m-%d")
            fecha_fin = fecha_inicio + timedelta(days=1)
        else:
            raise ValueError("Se requiere una fecha para el informe diario.")
    elif periodo == "semanal":
        fecha_inicio = datetime.strptime(fecha, "%Y-%m-%d")
        fecha_fin = fecha_inicio + timedelta(days=7)
    elif periodo == "mensual":
        fecha_inicio = datetime.strptime(fecha, "%Y-%m-%d")
        fecha_fin = (fecha_inicio.replace(day=1) + timedelta(days=31)).replace(day=1)
    else:
        raise ValueError("Periodo no reconocido.")
    return fecha_inicio.strftime("%Y-%m-%d"), fecha_fin.strftime("%Y-%m-%d")

def listar_metodos_pago_para_ventas():
    conexion = ConexionDB()
    sql = "SELECT id, descripcion FROM MetodosPago WHERE descripcion != 'Contra entrega'"
    conexion.cursor.execute(sql)
    metodos = conexion.cursor.fetchall()
    conexion.cerrar()
    return metodos