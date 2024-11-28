from .conexion_db import ConexionDB
from Model.ventas_dao import Venta, registrar_venta


def crear_tabla_pagos():
    conexion = ConexionDB()
    cursor = conexion.cursor

    # Crear tabla de MetodosPago primero
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'MetodosPago')
        BEGIN
            CREATE TABLE MetodosPago (
                id INT PRIMARY KEY IDENTITY(1,1),
                descripcion NVARCHAR(50) NOT NULL
            )
            INSERT INTO MetodosPago (descripcion) VALUES
            ('Contra entrega'),
            ('Tarjeta'),
            ('Transferencia'),
            ('Efectivo')
        END
    ''')

    # Crear tabla de Pagos después
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Pagos')
        BEGIN
            CREATE TABLE Pagos (
                id INT PRIMARY KEY IDENTITY(1,1),
                reserva_id INT NOT NULL,
                metodo_pago_id INT NOT NULL,
                medio_entrega NVARCHAR(50) DEFAULT 'Físico',
                estado_pago NVARCHAR(50) DEFAULT 'Pendiente',
                fecha_pago DATETIME DEFAULT NULL,
                FOREIGN KEY (reserva_id) REFERENCES Reservas(id),
                FOREIGN KEY (metodo_pago_id) REFERENCES MetodosPago(id)
            )
        END
    ''')

    conexion.cerrar()

class Pago:
    def __init__(self, reserva_id, metodo_pago_id, medio_entrega='Físico', estado_pago='Pendiente', fecha_pago=None):
        self.id = None
        self.reserva_id = reserva_id
        self.metodo_pago_id = metodo_pago_id
        self.medio_entrega = medio_entrega
        self.estado_pago = estado_pago
        self.fecha_pago = fecha_pago

def registrar_pago(pago):
    conexion = ConexionDB()

    sql = """
        INSERT INTO Pagos (reserva_id, metodo_pago_id, medio_entrega, estado_pago, fecha_pago) 
        VALUES (?, ?, ?, ?, ?)
    """
    conexion.cursor.execute(
        sql, (pago.reserva_id, pago.metodo_pago_id, pago.medio_entrega, pago.estado_pago, pago.fecha_pago)
    )

    conexion.cerrar()

def listar_pagos():
    conexion = ConexionDB()
    sql = """
        SELECT p.id, r.id AS reserva_id, r.cliente, m.descripcion AS metodo_pago, p.medio_entrega, 
               p.estado_pago, p.fecha_pago
        FROM Pagos p
        INNER JOIN Reservas r ON p.reserva_id = r.id
        INNER JOIN MetodosPago m ON p.metodo_pago_id = m.id
    """
    conexion.cursor.execute(sql)
    pagos = conexion.cursor.fetchall()
    conexion.cerrar()
    return pagos

def listar_metodos_pago():
    conexion = ConexionDB()
    sql = "SELECT id, descripcion FROM MetodosPago"
    conexion.cursor.execute(sql)
    metodos = conexion.cursor.fetchall()
    conexion.cerrar()
    return metodos

def actualizar_estado_pago(pago_id):
    conexion = ConexionDB()
    cursor = conexion.cursor

    # Obtener la información del pago y reserva relacionada
    sql_pago_info = """
        SELECT p.reserva_id, p.metodo_pago_id, r.cliente, r.producto_id, r.cantidad
        FROM Pagos p
        INNER JOIN Reservas r ON p.reserva_id = r.id
        WHERE p.id = ?
    """
    cursor.execute(sql_pago_info, (pago_id,))
    pago_info = cursor.fetchone()

    if not pago_info:
        conexion.cerrar()
        raise ValueError("El pago no existe o no está relacionado con una reserva válida.")

    reserva_id, metodo_pago_id, cliente, producto_id, cantidad = pago_info

    # Actualizar el estado del pago a "Pagado" y registrar la fecha
    sql_actualizar_pago = """
        UPDATE Pagos 
        SET estado_pago = 'Pagado', fecha_pago = GETDATE() 
        WHERE id = ?
    """
    cursor.execute(sql_actualizar_pago, (pago_id,))

    # Registrar la venta asociada a este pago SIN descontar del inventario
    sql_precio_producto = "SELECT precio FROM Productos WHERE id = ?"
    cursor.execute(sql_precio_producto, (producto_id,))
    producto = cursor.fetchone()

    if not producto:
        conexion.cerrar()
        raise ValueError("El producto relacionado con esta reserva no existe.")

    precio_unitario = producto[0]
    total_vendido = precio_unitario * cantidad

    nueva_venta = Venta(
        producto_id=producto_id,
        cantidad=cantidad,
        cliente=cliente,
        metodo_pago_id=metodo_pago_id,
        total_vendido=total_vendido
    )
    registrar_venta(nueva_venta, descontar_inventario=False)  # No descontar del inventario

    conexion.cerrar()

def listar_reservas_confirmadas():
    conexion = ConexionDB()
    sql = """
        SELECT id, cliente 
        FROM Reservas 
        WHERE estado_id = 2  -- Suponemos que el estado "Confirmado" tiene el ID 2
    """
    conexion.cursor.execute(sql)
    reservas = conexion.cursor.fetchall()
    conexion.cerrar()
    return reservas