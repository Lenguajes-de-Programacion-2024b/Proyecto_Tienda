from .conexion_db import ConexionDB
from datetime import datetime

def crear_tabla_reservas():
    conexion = ConexionDB()
    cursor = conexion.cursor

    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Reservas')
        BEGIN
            CREATE TABLE Reservas (
                id INT PRIMARY KEY IDENTITY(1,1),
                cliente VARCHAR(100),
                producto_id INT,
                cantidad INT,
                fecha DATE,
                FOREIGN KEY (producto_id) REFERENCES Productos(id)
            )
        END
    ''')
    conexion.cerrar()

class Reserva:
    def __init__(self, cliente, producto_id, cantidad, fecha):
        self.id = None
        self.cliente = cliente
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.fecha = fecha

    def __str__(self):
        return f'Reserva[{self.cliente}, {self.producto_id}, {self.cantidad}, {self.fecha}]'

def guardar_reserva(reserva):
    conexion = ConexionDB()
    sql = "INSERT INTO Reservas (cliente, producto_id, cantidad, fecha) VALUES (?, ?, ?, ?)"
    conexion.cursor.execute(sql, (reserva.cliente, reserva.producto_id, reserva.cantidad, reserva.fecha))
    conexion.cerrar()

def listar_reservas():
    conexion = ConexionDB()
    sql = "SELECT R.id, R.cliente, P.nombre, R.cantidad, R.fecha FROM Reservas R JOIN Productos P ON R.producto_id = P.id"
    conexion.cursor.execute(sql)
    reservas = conexion.cursor.fetchall()
    conexion.cerrar()
    return reservas

def editar_reserva(reserva, id):
    conexion = ConexionDB()
    sql = "UPDATE Reservas SET cliente = ?, producto_id = ?, cantidad = ?, fecha = ? WHERE id = ?"
    conexion.cursor.execute(sql, (reserva.cliente, reserva.producto_id, reserva.cantidad, reserva.fecha, id))
    conexion.cerrar()

def eliminar_reserva(id):
    conexion = ConexionDB()
    sql = "DELETE FROM Reservas WHERE id = ?"
    conexion.cursor.execute(sql, (id,))
    conexion.cerrar()