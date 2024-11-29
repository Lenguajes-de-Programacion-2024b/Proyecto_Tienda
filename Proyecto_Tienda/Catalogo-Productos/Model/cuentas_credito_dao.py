from .conexion_db import ConexionDB

def crear_tabla_Cuentas():
    conexion = ConexionDB()
    cursor = conexion.cursor

    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'CuentasCredito')
        BEGIN
           CREATE TABLE CuentasCredito (
            id INT PRIMARY KEY IDENTITY(1,1),
            cliente NVARCHAR(100) NOT NULL,
            deuda DECIMAL(10, 2) NOT NULL,
            saldo DECIMAL(10, 2) NOT NULL DEFAULT 0,
            estado NVARCHAR(20) NOT NULL DEFAULT 'Pendiente',
            fecha_creacion DATETIME DEFAULT GETDATE()
        )
        END
    ''')

    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'PagosCredito')
        BEGIN
            CREATE TABLE PagosCredito (
            id INT PRIMARY KEY IDENTITY(1,1),
            cuenta_id INT NOT NULL,
            monto DECIMAL(10, 2) NOT NULL,
            fecha DATETIME DEFAULT GETDATE(),
            FOREIGN KEY (cuenta_id) REFERENCES CuentasCredito(id)
        )
        END
    ''')

    conexion.cerrar()


def crear_cuenta_credito(cliente, deuda):
    """
    Crea una nueva cuenta de crédito para un cliente.
    """
    conexion = ConexionDB()
    cursor = conexion.cursor

    try:
        sql = "INSERT INTO CuentasCredito (cliente, deuda, saldo) OUTPUT INSERTED.id VALUES (?, ?, ?)"
        cursor.execute(sql, (cliente, deuda, 0))
        cuenta_id = cursor.fetchone()[0]
        conexion.commit()
        return cuenta_id
    except Exception as e:
        conexion.rollback()
        raise e
    finally:
        conexion.cerrar()


def listar_cuentas_credito():
    """
    Devuelve una lista de todas las cuentas de crédito.
    """
    conexion = ConexionDB()
    cursor = conexion.cursor

    try:
        sql = "SELECT id, cliente, deuda, saldo, estado, FORMAT(fecha_creacion, 'dd/MM/yyyy') AS fecha_creacion FROM CuentasCredito"
        cursor.execute(sql)
        cuentas = cursor.fetchall()
        return cuentas
    finally:
        conexion.cerrar()


def registrar_pago(cuenta_id, monto):
    """
    Registra un pago realizado por el cliente en su cuenta de crédito.
    """
    conexion = ConexionDB()
    cursor = conexion.cursor

    try:
        # Registrar el pago en la tabla PagosCredito
        sql_pago = "INSERT INTO PagosCredito (cuenta_id, monto) VALUES (?, ?)"
        cursor.execute(sql_pago, (cuenta_id, monto))

        # Actualizar el saldo en la cuenta de crédito
        sql_actualizar_saldo = "UPDATE CuentasCredito SET saldo = saldo + ? WHERE id = ?"
        cursor.execute(sql_actualizar_saldo, (monto, cuenta_id))

        # Verificar si la deuda está saldada
        sql_check_estado = '''
            UPDATE CuentasCredito
            SET estado = CASE
                WHEN saldo >= deuda THEN 'Completado'
                ELSE 'Pendiente'
            END
            WHERE id = ?
        '''
        cursor.execute(sql_check_estado, (cuenta_id,))

        conexion.commit()
    except Exception as e:
        conexion.rollback()
        raise e
    finally:
        conexion.cerrar()


def obtener_detalles_cuenta(cuenta_id):
    """
    Devuelve los detalles de una cuenta de crédito específica y sus pagos.
    """
    conexion = ConexionDB()
    cursor = conexion.cursor

    try:
        sql_cuenta = "SELECT id, cliente, deuda, saldo, estado, FORMAT(fecha_creacion, 'dd/MM/yyyy') AS fecha_creacion FROM CuentasCredito WHERE id = ?"
        cursor.execute(sql_cuenta, (cuenta_id,))
        cuenta = cursor.fetchone()

        sql_pagos = "SELECT id, monto, FORMAT(fecha, 'dd/MM/yyyy') AS fecha FROM PagosCredito WHERE cuenta_id = ?"
        cursor.execute(sql_pagos, (cuenta_id,))
        pagos = cursor.fetchall()

        return cuenta, pagos
    finally:
        conexion.cerrar()

def listar_cuentas_pendientes():
    """
    Devuelve una lista de cuentas de crédito con estado 'Pendiente'.
    """
    conexion = ConexionDB()
    cursor = conexion.cursor

    try:
        sql = """
        SELECT id, cliente, deuda, saldo, estado, FORMAT(fecha_creacion, 'dd/MM/yyyy') AS fecha_creacion 
        FROM CuentasCredito 
        WHERE estado = 'Pendiente'
        """
        cursor.execute(sql)
        cuentas_pendientes = cursor.fetchall()
        return cuentas_pendientes
    finally:
        conexion.cerrar()