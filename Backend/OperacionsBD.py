from ConectDB import *
import datetime

def realizar_consulta(User, Pass):
    conexion = Conectar()
    if conexion:
        with conexion.cursor() as cursor:
            sql_usuario = "SELECT UsuarioID, Nombre, CONTRASEÑA FROM Proyecto_SCHEMA.USUARIOS WHERE CUENTA = ?"
            cursor.execute(sql_usuario, (User,))
            resultado_usuario = cursor.fetchone()

            if resultado_usuario:
                usuario_id, nombre, contraseña_bd = resultado_usuario
                sql_contraseña = "SELECT CONTRASEÑA FROM Proyecto_SCHEMA.USUARIOS WHERE UsuarioID = ?"
                cursor.execute(sql_contraseña, (usuario_id,))
                contraseña = cursor.fetchone()[0]

                if contraseña == Pass:
                    return {
                        "UsuarioID": usuario_id,
                        "Nombre": nombre,
                        "CONTRASEÑA": contraseña_bd
                    }
                else:
                    return None
            else:
                return None
            
def Encontrar_Menu(User):
    conexion = Conectar()
    if conexion:
        with conexion.cursor() as cursor:
            sql = """SELECT U.USUARIOID AS IDUSUARIO, M.MENUPADRE
FROM Proyecto_SCHEMA.USUARIOS U
INNER JOIN Proyecto_SCHEMA.PERFILES P ON U.PERFILID = P.IDPERFIL
INNER JOIN Proyecto_SCHEMA.MENUS M ON P.IDPERFIL = M.IDPERFIL
WHERE U.CUENTA = ? ;"""
            cursor.execute(sql, (User,))
            resultado = cursor.fetchall()
            if resultado:
                menus = []
                for row in resultado:
                    menus.append(row[1])
                return menus
                cursor.close()
            else:
                return None
    else:
        return None

def Encontrar_SubMenu(User):
    conexion = Conectar()
    if conexion:
        with conexion.cursor() as cursor:
            sql = """SELECT M.IDMENU, SM.NOMBRE,SM.ENLACE
FROM Proyecto_SCHEMA.USUARIOS U
INNER JOIN Proyecto_SCHEMA.PERFILES P ON U.PERFILID = P.IDPERFIL
INNER JOIN Proyecto_SCHEMA.MENUS M ON P.IDPERFIL = M.IDPERFIL
INNER JOIN Proyecto_SCHEMA.SUBMENUS SM ON M.IDMENU = SM.IDMENU
WHERE U.CUENTA = ?;"""
            cursor.execute(sql, (User,))
            resultado = cursor.fetchall()
            if resultado:
                resultados = []
                for row in resultado:
                    resultados.append(f'{row[0]} {row[1]} {row[2]}')
                return resultados
                cursor.close()
            else:
                return None
    else:
        return None
##-------------------sql oracle---------------------------
def AuditoriaOr(user,accion):
    conexion = ConectarOracle()
    if isinstance(conexion, cx_Oracle.Connection):
        try:
            cursor = conexion.cursor()

            fecha_actual = datetime.datetime.now()

            sql = """
                INSERT INTO COMPRASBD.AUDITORIA (USUARIO, FECHA, ACCION)
                VALUES (:1, :2, :3)
            """
            cursor.execute(sql, (user, fecha_actual, accion))
            conexion.commit()
            return('exito')
        except cx_Oracle.Error as ex:
            print(ex)
            conexion.rollback()
            return "Error en el registro de auditoría"
        finally:
            cursor.close()
    else:
        return None
    
def ConsultarA():
    conexion = ConectarOracle()
    if isinstance(conexion, cx_Oracle.Connection):
        try:
            cursor = conexion.cursor()
            sql = """SELECT * FROM (SELECT * FROM COMPRASBD.AUDITORIA ORDER BY FECHA  DESC)
                     WHERE ROWNUM <= 50"""
            cursor.execute(sql)
            resultado = cursor.fetchall()
            if resultado:
                resultados = []
                for row in resultado:
                    resultados.append(row)
                return resultados
            else:
                return None

        except cx_Oracle.Error as ex:
            conexion.rollback()
            return ex
        finally:
             cursor.close()
    else:
        return None
    
def AgregarMerc(nombre,des,pre,cat):
    conexion = ConectarOracle()
    if isinstance(conexion, cx_Oracle.Connection):
        try:
            cursor = conexion.cursor()
            sql = """
                INSERT INTO COMPRASBD.PRODUCTOS (NOMBRE, DESCRIPCION, PRECIO, CATEGORIA) 
                VALUES (:1, :2, :3,:4)
            """
            cursor.execute(sql, (nombre,des,pre,cat))
            conexion.commit()
            return('exito')
        except cx_Oracle.Error as ex:
            print(ex)
            conexion.rollback()
            return "Error en el registro de auditoría"
        finally:
            cursor.close()
    else:
        return None
    
def ComsultaMerc():
    conexion = ConectarOracle()
    if isinstance(conexion, cx_Oracle.Connection):
        try:
            cursor = conexion.cursor()
            sql = """SELECT * FROM COMPRASBD.PRODUCTOS ORDER BY IDPRODUCTO DESC"""
            cursor.execute(sql)
            resultado = cursor.fetchall()
            if resultado:
                resultados = []
                for row in resultado:
                    resultados.append(row)
                return resultados
            else:
                return None

        except cx_Oracle.Error as ex:
            conexion.rollback()
            return ex
        finally:
            cursor.close()
    else:
        return None
    
def EliminarMerc(Id,tabla):
    conexion = ConectarOracle()
    if isinstance(conexion, cx_Oracle.Connection):
        try:
            cursor = conexion.cursor()
            if tabla == 'Productos':
                sql = """DELETE FROM COMPRASBD.PRODUCTOS WHERE IDPRODUCTO = :1"""
                cursor.execute(sql, (Id,))
            elif tabla == 'Pedidos':
                sql_detalles = """DELETE FROM COMPRASBD.DETALLES_DEPEDIDOS WHERE ID_PEDIDO = :1"""
                cursor.execute(sql_detalles, (Id,))
                sql_pedido = """DELETE FROM COMPRASBD.PEDIDOS WHERE ID_PEDIDO = :1"""
                cursor.execute(sql_pedido, (Id,))
            else:
                exit
            conexion.commit()
            return ('exito')
        except cx_Oracle.Error as ex:
            print(ex)
            conexion.rollback()
            return "Error en el registro de auditoría"
        finally:
            cursor.close()
    else:
        return None
    
def ObtenerDatos(Id,operacion):
    conexion = ConectarOracle()
    if isinstance(conexion, cx_Oracle.Connection):
        try:
            cursor = conexion.cursor()
            if operacion == 'productos':
                sql = """SELECT * FROM COMPRASBD.PRODUCTOS WHERE IDPRODUCTO = :1 ORDER BY IDPRODUCTO DESC"""
            elif operacion == 'obtenerdt':
                sql = """SELECT * FROM COMPRASBD.PRODUCTOS WHERE IDPRODUCTO = :1"""
            else:
                exit
            cursor.execute(sql,(Id,))
            resultado = cursor.fetchall()
            if resultado:
                for row in resultado:
                    return row
            else:
                return None

        except cx_Oracle.Error as ex:
            conexion.rollback()
            return ex
        finally:
            cursor.close()
    else:
        return None
    
def ActualizarMer(nombre,des,pre,cat,Id):
    conexion = ConectarOracle()
    if isinstance(conexion, cx_Oracle.Connection):
        try:
            cursor = conexion.cursor()
            sql = """
                UPDATE COMPRASBD.PRODUCTOS SET NOMBRE = :1, DESCRIPCION = :2, PRECIO = :3, CATEGORIA = :4
  WHERE IDPRODUCTO = :5
            """
            cursor.execute(sql, (nombre,des,pre,cat,Id))
            conexion.commit()
            return('exito')
        except cx_Oracle.Error as ex:
            print(ex)
            conexion.rollback()
            return "Error en el registro de auditoría"
        finally:
            cursor.close()
    else:
        return None
    
def Consultas(tabla):
    conexion = ConectarOracle()
    if isinstance(conexion, cx_Oracle.Connection):
        try:
            cursor = conexion.cursor()
            if tabla == 'Productos':
                sql = """SELECT * FROM COMPRASBD.PRODUCTOS"""
            if tabla == 'ValidarP':
                sql = """SELECT ID_PEDIDO,FECHA_PEDIDO,ESTADO_PEDIDO FROM COMPRASBD.PEDIDOS WHERE ESTADO_PEDIDO = 'Pendiente' """
            else:
                exit
            cursor.execute(sql)
            resultado = cursor.fetchall()
            if resultado:
                resultados = []
                for row in resultado:
                    resultados.append(row)
                return resultados
            else:
                return None

        except cx_Oracle.Error as ex:
            conexion.rollback()
            return ex
        finally:
             cursor.close()
    else:
        return None
    
def ConsultarP(consulta):
    conexion = ConectarOracle()
    if isinstance(conexion, cx_Oracle.Connection):
        try:
            cursor = conexion.cursor()
            if consulta == 1:
                sql = """SELECT
                        TO_CHAR(pe.FECHA_PEDIDO, 'MM/YYYY') AS mes,
                        p.NOMBRE AS producto_mas_vendido,
                        COUNT(*) AS cantidad_vendida
                    FROM
                        COMPRASBD.PEDIDOS pe
                    JOIN
                        COMPRASBD.DETALLES_DEPEDIDOS d ON pe.ID_PEDIDO = d.ID_PEDIDO
                    JOIN
                        COMPRASBD.PRODUCTOS p ON d.ID_PRODUCTO = p.IDPRODUCTO
                    GROUP BY
                        TO_CHAR(pe.FECHA_PEDIDO, 'MM/YYYY'), p.NOMBRE
                    HAVING
                        COUNT(*) = (
                            SELECT MAX(contador)
                            FROM (
                                SELECT TO_CHAR(pe2.FECHA_PEDIDO, 'MM/YYYY') AS mes2,
                                       p2.NOMBRE AS producto_mas_vendido2,
                                       COUNT(*) AS contador
                                FROM COMPRASBD.PEDIDOS pe2
                                JOIN COMPRASBD.DETALLES_DEPEDIDOS d2 ON pe2.ID_PEDIDO = d2.ID_PEDIDO
                                JOIN COMPRASBD.PRODUCTOS p2 ON d2.ID_PRODUCTO = p2.IDPRODUCTO
                                GROUP BY TO_CHAR(pe2.FECHA_PEDIDO, 'MM/YYYY'), p2.NOMBRE
                            ) subquery
                            WHERE subquery.mes2 = TO_CHAR(pe.FECHA_PEDIDO, 'MM/YYYY')
                        )
                    ORDER BY
                        mes, cantidad_vendida DESC
                    """
            elif consulta == 2:
                sql = """
                    SELECT
                        p.CATEGORIA AS categoria,
                        p.NOMBRE AS producto_mas_vendido,
                        COUNT(*) AS cantidad_vendida
                    FROM
                        COMPRASBD.PEDIDOS pe
                    JOIN
                        COMPRASBD.DETALLES_DEPEDIDOS d ON pe.ID_PEDIDO = d.ID_PEDIDO
                    JOIN
                        COMPRASBD.PRODUCTOS p ON d.ID_PRODUCTO = p.IDPRODUCTO
                    GROUP BY
                        p.CATEGORIA, p.NOMBRE
                    HAVING
                        COUNT(*) = (
                            SELECT MAX(contador)
                            FROM (
                                SELECT p2.CATEGORIA AS categoria2,
                                       p2.NOMBRE AS producto_mas_vendido2,
                                       COUNT(*) AS contador
                                FROM COMPRASBD.PEDIDOS pe2
                                JOIN COMPRASBD.DETALLES_DEPEDIDOS d2 ON pe2.ID_PEDIDO = d2.ID_PEDIDO
                                JOIN COMPRASBD.PRODUCTOS p2 ON d2.ID_PRODUCTO = p2.IDPRODUCTO
                                GROUP BY p2.CATEGORIA, p2.NOMBRE
                            ) subquery
                            WHERE subquery.categoria2 = p.CATEGORIA
                        )
                    ORDER BY
                        categoria, cantidad_vendida DESC
                    """
            elif consulta == 3:
                    sql =        """ SELECT
                    TO_CHAR(pe.FECHA_PEDIDO, 'MM/YYYY') AS mes,
                    p.NOMBRE AS producto_menos_vendido,
                    COUNT(*) AS cantidad_vendida
                FROM
                    COMPRASBD.PEDIDOS pe
                JOIN
                    COMPRASBD.DETALLES_DEPEDIDOS d ON pe.ID_PEDIDO = d.ID_PEDIDO
                JOIN
                    COMPRASBD.PRODUCTOS p ON d.ID_PRODUCTO = p.IDPRODUCTO
                GROUP BY
                    TO_CHAR(pe.FECHA_PEDIDO, 'MM/YYYY'), p.NOMBRE
                HAVING
                    COUNT(*) = (
                        SELECT MIN(contador)
                        FROM (
                            SELECT TO_CHAR(pe2.FECHA_PEDIDO, 'MM/YYYY') AS mes2,
                                p2.NOMBRE AS producto_menos_vendido2,
                                COUNT(*) AS contador
                            FROM COMPRASBD.PEDIDOS pe2
                            JOIN COMPRASBD.DETALLES_DEPEDIDOS d2 ON pe2.ID_PEDIDO = d2.ID_PEDIDO
                            JOIN COMPRASBD.PRODUCTOS p2 ON d2.ID_PRODUCTO = p2.IDPRODUCTO
                            GROUP BY TO_CHAR(pe2.FECHA_PEDIDO, 'MM/YYYY'), p2.NOMBRE
                        ) subquery
                        WHERE subquery.mes2 = TO_CHAR(pe.FECHA_PEDIDO, 'MM/YYYY')
                    )
                ORDER BY
                    mes, cantidad_vendida ASC"""
            elif consulta == 4:
               sql = """ SELECT
                                categoria,
                                producto_menos_vendido,
                                cantidad_vendida
                            FROM (
                                SELECT
                                    p.CATEGORIA AS categoria,
                                    p.NOMBRE AS producto_menos_vendido,
                                    NVL(COUNT(d.ID_PEDIDO), 0) AS cantidad_vendida,
                                    RANK() OVER (PARTITION BY p.CATEGORIA ORDER BY COUNT(d.ID_PEDIDO)) AS ranking
                                FROM
                                    COMPRASBD.PRODUCTOS p
                                LEFT JOIN
                                    COMPRASBD.DETALLES_DEPEDIDOS d ON p.IDPRODUCTO = d.ID_PRODUCTO
                                GROUP BY
                                    p.CATEGORIA, p.NOMBRE
                            )
                            WHERE ranking = 1
                            ORDER BY
                                categoria, cantidad_vendida ASC
                            """
            else:
                exit
            cursor.execute(sql)
            resultado = cursor.fetchall()
            if resultado:
                resultados = []
                for row in resultado:
                    resultados.append(row)
                return resultados
            else:
                return None

        except cx_Oracle.Error as ex:
            conexion.rollback()
            return ex
        finally:
             cursor.close()
    else:
        return None
    
def ConsultasPedidos(tabla,nombrec):
    conexion = ConectarOracle()
    if isinstance(conexion, cx_Oracle.Connection):
        try:
            cursor = conexion.cursor()
            if tabla == 'Pedidos':
                sql = """SELECT ID_PEDIDO,FECHA_PEDIDO,ESTADO_PEDIDO FROM COMPRASBD.PEDIDOS WHERE ESTADO_PEDIDO = 'Completado' AND NOMBRE_CLIENTE = :2"""
            elif tabla == 'PedidosP':
                sql = """SELECT ID_PEDIDO,FECHA_PEDIDO,ESTADO_PEDIDO FROM COMPRASBD.PEDIDOS WHERE ESTADO_PEDIDO = 'Pendiente' AND NOMBRE_CLIENTE = :2"""
            else:
                exit
            cursor.execute(sql,(nombrec,))
            resultado = cursor.fetchall()
            if resultado:
                resultados = []
                for row in resultado:
                    resultados.append(row)
                return resultados
            else:
                return None
        except cx_Oracle.Error as ex:
            conexion.rollback()
            return ex
        finally:
             cursor.close()
    else:
        return None
    
def GenerarPedido(usuario, productos):
    conexion = ConectarOracle()
    if isinstance(conexion, cx_Oracle.Connection):
        try:
            cursor = conexion.cursor()
            fecha_actual = datetime.datetime.now()

            cursor.execute(
                "INSERT INTO COMPRASBD.Pedidos (FECHA_PEDIDO, ESTADO_PEDIDO, NOMBRE_CLIENTE) VALUES (:1, 'Pendiente', :2) RETURNING ID_PEDIDO INTO :3",
                (fecha_actual, usuario, cursor.var(cx_Oracle.NUMBER))
            )
            conexion.commit()

            id_pedido = cursor.var(cx_Oracle.NUMBER)
            cursor.execute("SELECT ID_PEDIDO FROM COMPRASBD.Pedidos WHERE ROWNUM = 1 ORDER BY ID_PEDIDO DESC")
            row = cursor.fetchone()

            if row:
                id_pedido.setvalue(0, row[0])

                for item in productos:
                    cursor.execute("INSERT INTO COMPRASBD.DETALLES_DEPEDIDOS (ID_PEDIDO, ID_PRODUCTO) VALUES (:1, :2)",
                                   (id_pedido.getvalue(), item))
                conexion.commit()
                return 'Éxito'
            else:
                conexion.rollback()
                return 'Error al obtener el ID del pedido'
        except cx_Oracle.Error as ex:
            print(ex)
            conexion.rollback()
            return 'Error en la inserción'
        finally:
            cursor.close()
            conexion.close()
    else:
        return 'Error de conexión'


def ConsultaFac(id):
    conexion = ConectarOracle()
    if isinstance(conexion, cx_Oracle.Connection):
        try:
            cursor = conexion.cursor()
            sql = """SELECT p.id_pedido,p.fecha_pedido,d.id_producto FROM COMPRASBD.PEDIDOS P
JOIN COMPRASBD.detalles_depedidos D ON D.id_pedido = p.id_pedido
WHERE P.ID_PEDIDO = :1"""
            cursor.execute(sql,(id,))
            resultado = cursor.fetchall()
            if resultado:
                resultados = []
                for row in resultado:
                    resultados.append(row)
                return resultados
            else:
                return None

        except cx_Oracle.Error as ex:
            conexion.rollback()
            return ex
        finally:
             cursor.close()
    else:
        return None