import pyodbc

class ConexionDB:
    def __init__(self):
        # Configuración de la conexión
        self.dsn = (
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=(localdb)\\server;'
            'DATABASE=DB_Python;'
            'UID=sa;'
            'PWD=Rambo#12345;'
        )
        # Estableciendo la conexión y creando el cursor
        self.conexion = pyodbc.connect(self.dsn)
        self.cursor = self.conexion.cursor()

    def cerrar(self):
        # Guardar y cerrar la conexión
        self.conexion.commit()
        self.conexion.close()