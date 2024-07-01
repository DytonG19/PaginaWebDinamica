from flask import Flask, request, jsonify, redirect,url_for,make_response
from configuracion import configuracion
import requests
from OperacionsBD import *
app=Flask(__name__)
logged_user = ""
id = ""  
data = {}

@app.route('/')
def main():
    return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def login():
    global logged_user
    data = request.get_json()

    if data is None:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400
    username = data.get('username')
    password = data.get('password')
    logged = realizar_consulta(username, password)
    if logged is not None:
        logged_user = username
        return redirect(url_for('home')) 
    else:
        return jsonify({'message': 'Datos recibos con éxito'}), 400

@app.route('/home', methods=['GET', 'POST'])
def home():
    global logged_user
    username = logged_user
    if request.method == 'GET':
        resultado = Encontrar_Menu(username)
        sub = Encontrar_SubMenu(username)
        data = {'menu': resultado, 'submenu': sub}
        return jsonify(data)
    elif request.method == 'POST':
        data = request.form.get('Regresar')
        if data == 'Regresar':
            return redirect(url_for('login'))
    
@app.route('/Administrar',  methods=['GET', 'POST'])
def Auditoria():
    resultados = ConsultarA()
    if request.method == 'GET':
        data = {'resultados':resultados}
        return jsonify(data)
    elif request.method == 'POST':
        data = request.form.get('Regresar')
        if data == 'Regresar':
            return redirect(url_for('home'))
    
@app.route('/AgregarM', methods=['POST'])
def AgregarM():
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400
    Nombre = data.get('Nombre')
    Descripcion = data.get('Descripcion')
    Precio = data.get('Precio')
    Categoria = data.get('Cat')
    logged_user = data.get('logged_user')
    resultado = AgregarMerc(Nombre,Descripcion,float(Precio),Categoria)
    if resultado == 'exito':
        ms = "se agrego un producto Nombre: " + Nombre  + " Descripcion: " + Descripcion + " Precio: Q" + Precio + "Categoria: "+ Categoria
        AuditoriaOr(logged_user, ms)
    return jsonify({'message': 'Datos recibidos con éxito'})

@app.route('/EditarM',  methods=['GET', 'POST'])
def EditarM():
    resultados = ComsultaMerc()
    if request.method == 'GET':
        data = {'resultados':resultados}
        return jsonify(data)

@app.route('/EditarProductos', methods=['GET', 'POST'])
def EditarProductos():
    if request.method == 'POST':
        global id
        data = request.get_json()
        id = data.get('id')
        return 'exito'
    
@app.route('/EditarProductosAPI', methods=['GET', 'POST'])
def EditarProductosAPI():
    global data
    global id
    if request.method == 'GET':
            bus = ObtenerDatos(int(id),'productos')
            data = {'bus': bus}
            return jsonify(data)
    else:
        data1 = request.get_json()
        if data1 is None:
            return jsonify({'error': 'No se recibieron datos válidos'}), 400
        Nombre = data1.get('Nombre')
        Descripcion = data1.get('Descripcion')
        Precio = data1.get('Precio')
        Categoria = data1.get('Cat')
        idd = data1.get('id')
        bus1 = data.get('bus')
        logged_user = data1.get('logged_user')
        ms = f"Edito los productos Valores Anteriores: Nombre Anterior: {bus1[1]} Descripcion Anterior: {bus1[2]} Precio Anterior: Q{bus1[3]} Categoria Anterior: {bus1[4]} Nuevos Valores: Nombre: {Nombre} Descripcion: {Descripcion} Precio: Q{Precio} Categoria: {Categoria}"
        resultados = ActualizarMer(Nombre,Descripcion,float(Precio),Categoria,int(idd))
        if resultados == 'exito':
            AuditoriaOr(logged_user, ms)
            return jsonify({'error': 'Comunicacion exitosa'})
        
@app.route('/EliminarProducto', methods=['POST'])
def EliminarP():
    global id
    data = request.get_json()
    id = data.get('id')
    user = data.get('logged_user')
    if data is None:
        return jsonify({'error': 'No se recibieron datos válidos'}), 400
    else:
        row = ObtenerDatos(int(id),'productos')
        resultado = EliminarMerc(int(id),'Productos')
        if resultado == 'exito':
            ms = f'Elimino un Producto con el ID: {row[0]}, Nombre: {row[1]}, Descripcion: {row[2]}, Precio: Q{row[3]}'
            AuditoriaOr(user, ms)
        return jsonify({'exito':'Se recibio el id'})
    
@app.route('/ReportesVentas', methods=['POST','GET'])
def ReporteVEntas():
    resultados = Consultas('Productos')
    if request.method == 'GET':
        data = {'resultados':resultados}
        return jsonify(data)
    elif request.method == 'POST':
        data = request.get_json()
        op = data.get('op')
        resultado = ConsultarP(int(op))
        if resultado is not None:
            return jsonify(resultado)
        else:
            return jsonify({'error': 'No se recibieron datos válidos'}), 400

@app.route('/GenerarInforme', methods=['POST'])
def Generarinforme():
    data = request.get_json()
    user = data.get('logged_user')
    ms = 'Creo un Informe de ventas'
    AuditoriaOr(user, ms)
    response_data = {'message': 'Informe generado exitosamente'}
    response = make_response(jsonify(response_data), 200) 
    return response

@app.route('/Verpedido', methods=['POST'])
def Verpedidos():
        data = request.get_json()
        logged_user = data.get('logged_user')
        resultados = ConsultasPedidos('Pedidos',logged_user)
        if resultados is not None:
            return jsonify(resultados),200
        
@app.route('/Descargarfac', methods=['POST'])
def DescargarFac():
    data = request.get_json()
    id = data.get('id')
    con = ConsultaFac(int(id))
    if con is not None:
        return jsonify(con),200

@app.route ('/Cancelarpedido', methods = ['POST'])
def cancelarPedido():
    if request.method == 'POST':
        data = request.get_json()
        logged_user = data.get('logged_user')
        resultados = ConsultasPedidos('PedidosP',logged_user)
        if resultados is not None:
            return jsonify(resultados),200
        else:
            return jsonify({'error': 'No se recibieron datos válidos'}), 400
        
@app.route ('/EliminarPedido' ,methods=['POST'])
def EliminarPedido():
    data = request.get_json()
    id = data.get('id')
    resultado = EliminarMerc(int(id),'Pedidos')
    if resultado == 'exito':
        return jsonify({'Exito': 'Se elimino el pedido'}), 200
    else:
         return jsonify({'Error': 'No elimino el pedido'}), 400


productos = []        
@app.route('/ConsultarMerc', methods=['GET', 'POST'])
def Agregar():
    global productos  
    if request.method == 'GET':
        resultados = ComsultaMerc()
        if resultados is not None:
            return jsonify(resultados)
        else:
            return jsonify({'Error': 'No se encontraron resultados'}), 400

    elif request.method == 'POST':
        data = request.get_json()
        productos = data.get('productos')
        logged_user = data.get('logged_user')
        resultados = GenerarPedido(logged_user,productos)
        if resultados == 'Éxito':
            return jsonify({'Exito': 'Se creó el pedido'}), 200
        else:
            return jsonify({'Error': 'No se encontraron resultados'}), 400

@app.route('/PedidosV', methods=['POST','GET'])
def PedidosG():
    if request.method == 'GET':
        resultados = Consultas('ValidarP')
        if resultados is not None:
            data = {'resultados':resultados}
            return jsonify(data)
        else:
            return jsonify({'Error': 'No se encontraron resultados'}), 400



if __name__=='__main__':
    app.config.from_object(configuracion['development'])
    app.run(port=5000)