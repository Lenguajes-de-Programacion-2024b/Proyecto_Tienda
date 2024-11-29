import pyodbc

class ConexionDB:
    def __init__(self):
        # Configuración de la conexión
        self.dsn = (
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=SQL5112.site4now.net;'
            'DATABASE=db_aae65a_mvcsample;'
            'UID=db_aae65a_mvcsample_admin;'
            'PWD=Rambo#12345;'
        )
        # Estableciendo la conexión y creando el cursor
        self.conexion = pyodbc.connect(self.dsn)
        self.cursor = self.conexion.cursor()

    def cerrar(self):
        # Guardar y cerrar la conexión
        self.conexion.commit()
        self.conexion.close()

    def rollback(self):
        """
        Revierte los cambios realizados en la base de datos.
        """
        self.conexion.rollback()

    def commit(self):
        """
        Confirma los cambios realizados en la base de datos.
        """
        self.conexion.commit()