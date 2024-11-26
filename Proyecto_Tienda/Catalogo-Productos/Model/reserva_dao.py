from .conexion_db import ConexionDB
from datetime import datetime, timedelta

def crear_tabla_reservas():
    conexion = ConexionDB()
    cursor = conexion.cursor

    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Reservas')
        BEGIN
            CREATE TABLE Reservas (
                id INT PRIMARY KEY IDENTITY(1,1),
                producto_id INT,
                cantidad INT,
                cliente NVARCHAR(100),
                fecha_reserva DATETIME DEFAULT GETDATE(),
                estado_id INT DEFAULT 1,
                FOREIGN KEY (producto_id) REFERENCES Productos(id)
            )
        END
    ''')

    # Opcional: Crear tabla de estados si no existe
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'EstadosReservas')
        BEGIN
            CREATE TABLE EstadosReservas (
                id INT PRIMARY KEY,
                descripcion NVARCHAR(50)
            )
            INSERT INTO EstadosReservas (id, descripcion) VALUES
            (1, 'Pendiente'),
            (2, 'Confirmada'),
            (3, 'Cancelada')
        END
    ''')

    conexion.cerrar()

class Reserva:
    def __init__(self, producto_id, cantidad, cliente, estado_id=1):
        self.id = None
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.cliente = cliente
        self.fecha_reserva = None
        self.estado_id = estado_id

def registrar_reserva(reserva):
    conexion = ConexionDB()

    # Verificar si hay suficiente cantidad en el inventario
    consulta_cantidad = "SELECT cantidad FROM Productos WHERE id = ?"
    conexion.cursor.execute(consulta_cantidad, (reserva.producto_id,))
    stock_disponible = conexion.cursor.fetchone()[0]

    if stock_disponible >= reserva.cantidad:
        # Registrar la reserva
        sql_reserva = """
            INSERT INTO Reservas (producto_id, cantidad, cliente, estado_id) 
            VALUES (?, ?, ?, ?)
        """
        conexion.cursor.execute(sql_reserva, (reserva.producto_id, reserva.cantidad, reserva.cliente, reserva.estado_id))

        # Actualizar el stock del producto
        sql_actualizar_stock = "UPDATE Productos SET cantidad = cantidad - ? WHERE id = ?"
        conexion.cursor.execute(sql_actualizar_stock, (reserva.cantidad, reserva.producto_id))

        conexion.cerrar()
    else:
        conexion.cerrar()
        raise ValueError("No hay suficiente stock disponible para reservar.")
    
def listar():
    conexion = ConexionDB()
    sql = "SELECT id, nombre FROM Productos"  # Ajusta según los campos de tu tabla
    conexion.cursor.execute(sql)
    productos = conexion.cursor.fetchall()  # Devuelve una lista de tuplas [(id, nombre), ...]
    conexion.cerrar()
    return productos

def listar_reservas():
    conexion = ConexionDB()
    sql = '''
        SELECT r.id, p.nombre, r.cantidad, r.cliente, r.fecha_reserva, e.descripcion
        FROM Reservas r
        INNER JOIN Productos p ON r.producto_id = p.id
        INNER JOIN EstadosReservas e ON r.estado_id = e.id
    '''
    conexion.cursor.execute(sql)
    reservas = conexion.cursor.fetchall()
    conexion.cerrar()
    return reservas

def eliminar_reserva(id):
    conexion = ConexionDB()

    # Primero, obtenemos la reserva que estamos eliminando
    consulta_reserva = "SELECT producto_id, cantidad FROM Reservas WHERE id = ?"
    conexion.cursor.execute(consulta_reserva, (id,))
    reserva = conexion.cursor.fetchone()

    if reserva:
        producto_id = reserva[0]
        cantidad_reservada = reserva[1]

        # Ahora, eliminamos la reserva
        sql_eliminar = "DELETE FROM Reservas WHERE id = ?"
        conexion.cursor.execute(sql_eliminar, (id,))

        # Actualizamos el stock en la tabla Productos
        sql_actualizar_stock = "UPDATE Productos SET cantidad = cantidad + ? WHERE id = ?"
        conexion.cursor.execute(sql_actualizar_stock, (cantidad_reservada, producto_id))

    conexion.cerrar()

def actualizar_estado_reserva(id, nuevo_estado_id):
    conexion = ConexionDB()
    sql = "UPDATE Reservas SET estado_id = ? WHERE id = ?"
    conexion.cursor.execute(sql, (nuevo_estado_id, id))
    conexion.cerrar()

def listar_estados_reserva():
    conexion = ConexionDB()
    sql = "SELECT id, descripcion FROM EstadosReservas"
    conexion.cursor.execute(sql)
    estados = conexion.cursor.fetchall()
    conexion.cerrar()
    return estados