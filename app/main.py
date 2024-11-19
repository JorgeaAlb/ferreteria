from flask import Flask, render_template, request, redirect, url_for
import json
import os

# Ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')

app = Flask(
    __name__,
    static_folder=os.path.realpath('frontend/static'),
    # template_folder=os.path.join(FRONTEND_DIR, 'templates')
    template_folder=os.path.realpath('frontend/templates')
)

# Archivo de datos
DATA_FILE = os.path.realpath('backend/base_datos.json')

# Funciones para cargar y guardar datos
def cargar_datos():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return {"inventario": [], "clientes": [], "proveedores": [], "facturas": []}

def guardar_datos(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Rutas de la aplicación
@app.route('/')
def inicio():
    return render_template('index.html')

# ---------------------------- INVENTARIO ---------------------------- #
@app.route('/inventario', methods=['GET', 'POST'])
def inventario():
    data = cargar_datos()
    if request.method == 'POST':
        nuevo_producto = {
            "id": len(data['inventario']) + 1,
            "nombre": request.form['nombre'],
            "categoria": request.form['categoria'],
            "precio": float(request.form['precio']),
            "cantidad": int(request.form['cantidad']),
            "unidad": request.form['unidad']
        }
        data['inventario'].append(nuevo_producto)
        guardar_datos(data)
    return render_template('inventario.html', inventario=data['inventario'])

@app.route('/inventario/borrar/<int:producto_id>', methods=['POST'])
def borrar_producto(producto_id):
    data = cargar_datos()
    data['inventario'] = [prod for prod in data['inventario'] if prod['id'] != producto_id]
    guardar_datos(data)
    return redirect(url_for('inventario'))

@app.route('/inventario/editar/<int:producto_id>', methods=['GET', 'POST'])
def editar_producto(producto_id):
    data = cargar_datos()
    producto = next((prod for prod in data['inventario'] if prod['id'] == producto_id), None)
    if request.method == 'POST' and producto:
        producto['nombre'] = request.form['nombre']
        producto['categoria'] = request.form['categoria']
        producto['precio'] = float(request.form['precio'])
        producto['cantidad'] = int(request.form['cantidad'])
        producto['unidad'] = request.form['unidad']
        guardar_datos(data)
        return redirect(url_for('inventario'))
    return render_template('editar_producto.html', producto=producto)

# ---------------------------- CLIENTES ---------------------------- #
@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    data = cargar_datos()
    if request.method == 'POST':
        nuevo_cliente = {
            "id": len(data['clientes']) + 1,
            "nombre": request.form['nombre'],
            "correo": request.form['correo']
        }
        data['clientes'].append(nuevo_cliente)
        guardar_datos(data)
    return render_template('clientes.html', clientes=data['clientes'])

@app.route('/clientes/borrar/<int:cliente_id>', methods=['POST'])
def borrar_cliente(cliente_id):
    data = cargar_datos()
    data['clientes'] = [cli for cli in data['clientes'] if cli['id'] != cliente_id]
    guardar_datos(data)
    return redirect(url_for('clientes'))

# ---------------------------- PROVEEDORES ---------------------------- #
@app.route('/proveedores', methods=['GET', 'POST'])
def proveedores():
    data = cargar_datos()
    if request.method == 'POST':
        nuevo_proveedor = {
            "id": len(data['proveedores']) + 1,
            "nombre": request.form['nombre'],
            "correo": request.form['correo']
        }
        data['proveedores'].append(nuevo_proveedor)
        guardar_datos(data)
    return render_template('proveedores.html', proveedores=data['proveedores'])

@app.route('/proveedores/borrar/<int:proveedor_id>', methods=['POST'])
def borrar_proveedor(proveedor_id):
    data = cargar_datos()
    data['proveedores'] = [prov for prov in data['proveedores'] if prov['id'] != proveedor_id]
    guardar_datos(data)
    return redirect(url_for('proveedores'))

# ---------------------------- FACTURACIÓN ---------------------------- #
@app.route("/facturacion", methods=["GET", "POST"])
def facturacion():
    data = cargar_datos()
    return render_template("facturacion.html", clientes=data['clientes'], inventario=data['inventario'], facturas=data['facturas'])

# Correr en la IP 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
