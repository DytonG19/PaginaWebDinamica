from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import pandas as pd
from openpyxl import Workbook
import jinja2
import pdfkit
from datetime import datetime
import os
from flask.helpers import send_from_directory
from config import config
import json
import requests

app = Flask(__name__)

logged_user = ""
id = ""

other_app_url = 'http://127.0.0.1:5000'

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    global logged_user
    if request.method == 'POST':
        user = request.form['username']
        contra = request.form['password']
        data = {
            'username': user,
            'password': contra
        }
        api_url = f'{other_app_url}/login'  
        response = requests.post(api_url, json=data)
        if response.status_code == 200:
            logged_user = user
            return redirect(url_for("home"))
        elif response.status_code == 400:
            flash('Usuario o Contraseña Incorrecta', 'error')
        else:
            return render_template('auth/login.html')
    return render_template('auth/login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        api_url = f'{other_app_url}/home'
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            resultado = data.get('menu')
            sub = data.get('submenu')
            diccionario = {
            "op1": [],
            "op2": [],
            "op3": [],
            }

            for item in sub:
                partes = item.split(' ')
                numero = int(partes[0])
                texto1 = partes[1]
                texto2 = partes[2]

                enlace = f'<a href="{texto2}">{texto1}</a>'

                if numero == 1 or numero == 4 or numero == 7 or numero == 10:
                  diccionario["op1"].append(enlace)
                elif numero == 2 or numero == 5 or numero == 8 or numero == 11:
                 diccionario["op2"].append(enlace)
                elif numero == 3 or numero == 6 or numero == 9 or numero == 12:
                 diccionario["op3"].append(enlace)

            diccionario['numero'] = len(sub)
            Op = {'opcions':resultado,
             'numero_op': len(resultado)}

            return render_template('home.html',  nombre=logged_user, Op = Op , diccionario = diccionario )
        else:
            return "Error al obtener datos de la otra aplicación", 500
    elif request.method == 'POST':
        api_url = f'{other_app_url}/home'
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            resultado = data.get('menu')
            sub = data.get('submenu')
            diccionario = {
            "op1": [],
            "op2": [],
            "op3": [],
            }

            for item in sub:
                partes = item.split(' ')
                numero = int(partes[0])
                texto1 = partes[1]
                texto2 = partes[2]

                enlace = f'<a href="{texto2}">{texto1}</a>'

                if numero == 1 or numero == 4 or numero == 7 or numero == 10:
                  diccionario["op1"].append(enlace)
                elif numero == 2 or numero == 5 or numero == 8 or numero == 11:
                 diccionario["op2"].append(enlace)
                elif numero == 3 or numero == 6 or numero == 9 or numero == 12:
                 diccionario["op3"].append(enlace)

            diccionario['numero'] = len(sub)
            Op = {'opcions':resultado,
             'numero_op': len(resultado)}

            return render_template('home.html',  nombre=logged_user, Op = Op , diccionario = diccionario )
        else:
            return "Error al obtener datos de la otra aplicación", 500
     
@app.route('/Administrar', methods=['GET', 'POST'])
def Auditoria():
    titulo = 'Auditoria'
    if request.method == 'GET':
        api_url = f'{other_app_url}/Administrar'
        response = requests.get(api_url)
        if response.status_code == 200:
             data = response.json()
             resultados = data.get('resultados')
             if resultados:
                html_table = "<table>"
                html_table += "<tr><th>ID</th><th>Usuario</th><th>Fecha y hora</th><th>Accion</th></tr>"
                for row in resultados:
                    html_table += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>"
                html_table += "</table>"
             else:
                html_table = 'Error'
             return render_template('Auditoria.html',html_table=html_table,titulo=titulo)

@app.route('/AgregarM', methods =  ['GET', 'POST'])
def AgregarM():
    global logged_user
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Descripcion = request.form['Descripcion']
        Precio = request.form['Precio']
        Cat = request.form['Categoria']
        data = {'Nombre':Nombre,'Descripcion':Descripcion,'Precio':Precio,'Cat':Cat,'logged_user':logged_user}
        api_url = f'{other_app_url}/AgregarM'  
        response = requests.post(api_url, json=data)
        if response.status_code == 200:
            return render_template('AgregarM.html')
        elif response.status_code == 400:
            return 'Error'
        else:
            return render_template('AgregarM.html')
    else:
        return render_template('AgregarM.html')
    

@app.route('/EditarM', methods=['GET', 'POST'])
def EditarM():
    global id
    global logged_user
    if request.method == 'GET':
        api_url = f'{other_app_url}/EditarM'
        response = requests.get(api_url)
        if response.status_code == 200:
             data = response.json()
             resultados = data.get('resultados')
             if resultados:
                html_table = "<table>"
                html_table += "<tr><th>ID</th><th>Nombre</th><th>Descripción</th><th>Precio</th><th>Acciones</th></tr>"
                for row in resultados:
                    html_table += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>"
                    html_table += f"<form action='/EditarM' method='POST'>"
                    html_table += f"<button class='btn btn-outline-secondary' type='submit' name='editar' value='{row[0]}' data-id='{row[0]}'>Editar</button>"
                    html_table += f"</form>"
                    html_table += f"<form action='/EditarM' method='POST'>"
                    html_table += f"<button class='btn btn-outline-danger' type='submit' name='eliminar' value='{row[0]}' data-id='{row[0]}'>Eliminar</button>"
                    html_table += f"</form></td></tr>"
                html_table += "</table>"
                return render_template('EditarM.html', html_table=html_table)
    elif request.method == 'POST':
        if 'editar' in request.form:
            id = request.form['editar']
            return redirect(url_for('EditarProductos'))
        elif 'eliminar' in request.form:
            id = request.form['eliminar']
            data = {'id':id,'logged_user':logged_user}
            api_url = f'{other_app_url}/EliminarProducto'  
            response = requests.post(api_url, json=data)
            if response.status_code == 200:
                return redirect(url_for('home'))

        
@app.route('/EditarProductos', methods=['GET', 'POST'])
def EditarProductos():
    global id
    global logged_user
    idp = id
    if request.method == 'POST':
        id = request.form.get('id')
    
    api_url = f'{other_app_url}/EditarProductos'
    data = {'id': str(id)}  
    response = requests.post(api_url, json=data)
    
    api_url1 = f'{other_app_url}/EditarProductosAPI'
    response1 = requests.get(api_url1)
    
    if response1.status_code == 200:
        data1 = response1.json()
        bus = data1.get('bus')
        datos = {
            'Nombre': bus[1],
            'Des': bus[2],
            'precio': bus[3],
            'Categoria': bus[4]
        }
        return render_template('EditarProductos.html', datos=datos)
    
    if request.method == 'POST':
        datos = {
            'Nombre': '',
            'Des': '',
            'precio': '',
            'Categoria': ''
        }
        Nombre = request.form['NombreE']
        Descripcion = request.form['Descripcion']
        Precio = request.form['Precio']
        Cat = request.form['Categoria']
        data1 = {
            'Nombre': Nombre,
            'Descripcion': Descripcion,
            'Precio': Precio,
            'Cat': Cat,
            'logged_user': logged_user,
            'id':idp
        }
        api_url1 = f'{other_app_url}/EditarProductosAPI'
        response = requests.post(api_url1, json=data1)
        if response.status_code == 200:
            return render_template('EditarProductos.html', datos=datos)
    
        return render_template('EditarProductos.html', datos=datos)
    
@app.route('/ReporteVentas', methods=['GET','POST'])
def ReportesVentas():
    titulo = 'Reporte'
    if request.method == 'GET':
        api_url = f'{other_app_url}/ReportesVentas'
        response = requests.get(api_url)
        if response.status_code == 200:
             data = response.json()
             resultados = data.get('resultados')
             if resultados:
                html_table = "<table>"
                html_table += "</th><ttr><th>ID<h>Nombre</th><th>Descripcion</th><th>Precio</th><th>Categoria</th></tr>"
                for row in resultados:
                    html_table += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>"
                html_table += "</table>"
             else:
                html_table = 'Error'
             return render_template('Reportes.html',html_table=html_table,titulo=titulo)
    elif request.method == 'POST':
        op = request.form['boton']
        data = {'op':op}
        api_url = f'{other_app_url}/ReportesVentas'  
        response = requests.post(api_url, json=data)
        if response.status_code == 200:
            con = response.json()
            if con:
                html_table = "<table>"
            if op == '1' or op == '3':
                html_table += "<tr><th>Fecha por mes</th><th>Producto</th><th>Cantidad vendida</th></tr>"
                encabezado = ["Fecha", "Producto", "Cantidad Vendida"]
            elif op == '2' or op == '4':
                html_table += "<tr><th>Categorias</th><th>Producto</th><th>Cantidad vendida</th></tr>"
                encabezado = ["Categoria", "Producto", "Cantidad Vendida"]
            for row in con:
                html_table += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
            html_table += "</table>"
            df = pd.DataFrame(con[1:], columns=con[0])
            excel_file = "reporte_excel.xlsx"
            workbook = Workbook()
            worksheet = workbook.active
            worksheet.append(encabezado)
            for row in df.values.tolist():
                worksheet.append(row)
            workbook.save(excel_file)
        else:
            html_table = 'Error'
        return render_template('Reportes.html', html_table=html_table)
    else:
        return render_template('Reportes.html', html_table=html_table)
    return render_template('Reportes.html',html_table=html_table)
            
@app.route('/descargar_excel')
def descargar_excel():
    global logged_user
    data = {'logged_user':logged_user}
    api_url = f'{other_app_url}/GenerarInforme'  
    requests.post(api_url, json=data) 
    return send_file("reporte_excel.xlsx", as_attachment=True)

pdf_directory = os.path.join(app.root_path, 'static')

@app.route('/VerPedidos', methods=['GET', 'POST'])
def VerPedidos():
    global logged_user
    data = {'logged_user': logged_user}
    api_url = f'{other_app_url}/Verpedido'  
    response = requests.post(api_url, json=data)
    if response.status_code == 200:
        resultados = response.json()
        if resultados:
            html_table = "<table>"
            html_table += "<tr><th>ID</th><th>Fecha del pedido</th><th>Estado</th><th>Acciones</th></tr>"
            for row in resultados:
                html_table += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>"
                html_table += f"<form action='/VerPedidos' method='POST'>"
                html_table += f"<button class='btn btn-outline-secondary' type='submit' name='Imprimir' value='{row[0]}' data-id='{row[0]}'>Imprimir Factura</button>"
                html_table += f"</form></td></tr>"
            html_table += "</table>"
            if request.method == 'POST' and 'Imprimir' in request.form:
                id = request.form['Imprimir']
                data = {'id':id}
                api_url = f'{other_app_url}/Descargarfac'  
                response = requests.post(api_url, json=data)
                if response.status_code == 200:
                    con = response.json()
                    for item in con:
                        date_str = item[1]
                        fecha = date_str
                    context = {'client_name': logged_user,'today_date':fecha}

                    template_loader = jinja2.FileSystemLoader('templates')
                    template_env = jinja2.Environment(loader=template_loader)

                    html_template = 'factura.html'
                    template = template_env.get_template(html_template)
                    output_text = template.render(context)

                    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
                    output_pdf = os.path.join(pdf_directory, 'factura.pdf')
                    pdfkit.from_string(output_text, output_pdf, configuration=config, css=['static/css/factura.css'])
                    pdf_filename = 'factura.pdf'
                    pdf_path = os.path.join('static', pdf_filename)
                    html_table += f'<a href="{pdf_path}" download>Descargar Factura</a>'
                    return render_template('Pedidos.html', html_table=html_table)
    return render_template('Pedidos.html', html_table=html_table)

@app.route('/static/<filename>')
def serve_pdf(filename):
    return send_from_directory(pdf_directory, filename)

@app.route('/CancelarPedidos', methods=['GET','POST'])
def CancelarPedidos():
    titulo = 'Pedidos'
    global logged_user
    data = {'logged_user': logged_user}
    api_url = f'{other_app_url}/Cancelarpedido'  
    response = requests.post(api_url, json=data)
    if response.status_code == 200:
        resultados = response.json()
        if resultados:
            html_table = "<table>"
            html_table += "<tr><th>ID</th><th>Fewcha del pedido</th><th>Estado</th><th>Acciones</th></tr>"
            for row in resultados:
                html_table += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>"
                html_table += f"<form action='/CancelarPedidos' method='POST'>"
                html_table += f"<button class='btn btn-outline-danger' type='submit' name='Cancelar' value='{row[0]}' data-id='{row[0]}'>Cancelar Pedidos</button>"
                html_table += f"</form></td></tr>"
            html_table += "</table>"
            if request.method == 'POST' and 'Cancelar' in request.form:
                id = request.form['Cancelar']
                data = {'id':id}
                api_url = f'{other_app_url}/EliminarPedido'  
                response = requests.post(api_url, json=data)
                if response.status_code == 200:
                    return redirect(url_for('home'))
                else:
                    return ('error')
            else:
                return render_template('Auditoria.html', titulo=titulo, html_table=html_table)
    else:
        return render_template('Auditoria.html', titulo=titulo)

productos = [] 
@app.route('/MercaderiaC', methods=['GET', 'POST'])
def AgergarPedidos():
    titulo = "Agregar"
    global logged_user
    html_table = ""

    if request.method == 'GET':
        api_url = f'{other_app_url}/ConsultarMerc'
        response = requests.get(api_url)
        if response.status_code == 200:
            resultados = response.json()
            if resultados:
                html_table = "<table>"
                html_table += "<tr><th>ID</th><th>Nombre</th><th>Descripción</th><th>Precio</th><th>Acciones</th></tr>"
                for row in resultados:
                    html_table += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>"
                    html_table += f"<form action='/MercaderiaC' method='POST'>"
                    html_table += f"<button class='btn btn-success' type='submit' name='Agregar' value='{row[0]}' data-id='{row[0]}'>Agregar</button>"
                    html_table += f"</form></td></tr>"
                html_table += "</table>"
                html_table += f"<form action='/MercaderiaC' method='POST'>"
                html_table += f"<button class='btn btn-success' type='submit' name='Pedido'>Hacer Pedido</button>"
                html_table += f"</form>"

    if request.method == 'POST':
        if 'Agregar' in request.form:
            idp = request.form['Agregar']
            productos.append(idp)
            print(productos)
            return redirect(url_for('AgergarPedidos'))

        elif 'Pedido' in request.form:
            data = {'logged_user': logged_user, 'productos':productos}
            api_url = f'{other_app_url}/ConsultarMerc'
            response = requests.post(api_url, json=data)
            return redirect(url_for('home'))

        elif 'Regresar' in request.form:
            productos.clear()

    return render_template('Auditoria.html', titulo=titulo, html_table=html_table)

@app.route('/Pedidos', methods=['GET', 'POST'])
def ValidarPedido():
    titulo = 'Validar Pedido'
    api_url = f'{other_app_url}/PedidosV'
    response = requests.get(api_url)
    if response.status_code == 200:
        resultados = response.json()
        if resultados:
            html_table = "<table>"
            html_table += "<tr><th>ID</th><th>Fecha del pedido</th><th>Estado</th><th>Acciones</th></tr>"
            for row in resultados:
                html_table += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>"
                html_table += f"<form action='/Pedidos' method='POST'>"
                html_table += f"<button class='btn btn-outline-success' type='submit' name='Aceptar'>Validar Compra</button>"
                html_table += f"</form>"
                html_table += f"<form action='/Verficardatos' method='POST'>"
                html_table += f"<button class='btn btn-outline-warning' type='submit' name='Verificar'>Verficar Datos</button>"
                html_table += f"</form>"
                html_table += f"<form action='/Pedidos' method='POST'>"
                html_table += f"<button class='btn btn-outline-danger' type='submit' name='Anular'>Anular Compra</button>"
                html_table += f"</form></td></tr>"
            html_table += "</table>"
            if request.method == 'POST':
                if 'Aceptar' in request.form:
                    id = request.form['Aceptar']
                elif 'Anular' in request.form:
                    id = request.form['Anular']
                    data = {'id':id}
                    api_url = f'{other_app_url}/EliminarPedido'  
                    response = requests.post(api_url, json=data)
                    if response.status_code == 200:
                        return redirect(url_for('home'))
                    else:
                        return ('error')
            else:
                return render_template('Auditoria.html', titulo=titulo, html_table=html_table)
        return render_template('Auditoria.html',titulo=titulo,html_table=html_table)
    else:
        return('No hay datos')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(port=5001)