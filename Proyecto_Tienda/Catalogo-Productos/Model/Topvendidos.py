
from Model.conexion_db import ConexionDB


def mostrar_mas_vendidos():
    conexion = ConexionDB()
    sql = '''
        SELECT TOP 5 p.nombre, SUM(v.cantidad) AS total_vendido
        FROM Ventas v
        INNER JOIN Productos p ON v.producto_id = p.id
        GROUP BY p.nombre
        ORDER BY total_vendido DESC
    '''
    conexion.cursor.execute(sql)
    productos_mas_vendidos = conexion.cursor.fetchall()
    conexion.cerrar()
    return productos_mas_vendidos


def mostrar_menos_vendidos():
    conexion = ConexionDB()
    sql = '''
        SELECT TOP 5 p.nombre, SUM(v.cantidad) AS total_vendido
        FROM Ventas v
        INNER JOIN Productos p ON v.producto_id = p.id
        GROUP BY p.nombre
        ORDER BY total_vendido ASC
    '''
    conexion.cursor.execute(sql)
    productos_menos_vendidos = conexion.cursor.fetchall()
    conexion.cerrar()
    return productos_menos_vendidos
