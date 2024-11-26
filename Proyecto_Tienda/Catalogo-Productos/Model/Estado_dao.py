from .conexion_db import ConexionDB

def crear_tabla_estados():
    conexion = ConexionDB()
    cursor = conexion.cursor
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Estados')
        BEGIN
            CREATE TABLE Estados (
                id INT PRIMARY KEY IDENTITY(1,1),
                nombre NVARCHAR(50) NOT NULL
            )
            INSERT INTO Estados (nombre) VALUES ('Pendiente'), ('Pagado'), ('Cancelado')
        END
    ''')
    conexion.cerrar()