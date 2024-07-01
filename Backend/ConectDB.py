import pyodbc
server='DYTON\SQLEXPRESS'
database ='OrdenesCompra'
usuario= 'ComprasCRUD'
contrasenya='Dylan1209'
def Conectar():
    try:
        Conexion = pyodbc.connect('DRIVER={SQL SERVER};SERVER='+server+';DATABASE='+database+';UID='+usuario+';PWD='+contrasenya)
        return Conexion
    except Exception as ex:
        print("Ocurrio un error", ex)
        return None
    
import cx_Oracle

def ConectarOracle():
    try:
        connection = cx_Oracle.connect(
            user='ComprasCRUD',
            password='Dyton1209',
            dsn='localhost:1521/XE',
            encoding='UTF-8'
        )
        return connection
    except cx_Oracle.Error as ex:
        return ex