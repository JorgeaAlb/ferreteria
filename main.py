from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)
DATA_FILE = 'base_datos.json'

def cargar_datos():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return {"inventario": [], "clientes": [], "proveedores": [], "facturas": []}

def guardar_datos(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Ruta de inicio
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
    if request.method == "POST":
        cliente_id = request.form["cliente"]
        productos_ids = request.form.getlist("productos")  # Obtener todos los productos seleccionados
        cantidad_dict = {}  # Un diccionario para almacenar las cantidades de cada producto seleccionado

        # Buscar el cliente
        cliente = next(cliente for cliente in data['clientes'] if cliente["id"] == int(cliente_id))

        # Buscar los productos seleccionados y sus cantidades
        productos_seleccionados = []
        total = 0
        for producto_id in productos_ids:
            cantidad = int(request.form.get(f"cantidad_{producto_id}", 1))  # Obtener la cantidad seleccionada
            producto = next(p for p in data['inventario'] if p["id"] == int(producto_id))

            # Verificar que la cantidad no exceda el inventario
            if cantidad <= producto["cantidad"]:
                productos_seleccionados.append({
                    "producto": producto["nombre"],
                    "cantidad": cantidad,
                    "precio": producto["precio"]
                })
                total += float(producto["precio"]) * cantidad
                # Restar la cantidad vendida del inventario
                producto["cantidad"] -= cantidad
            else:
                # Si la cantidad es mayor que el inventario, agregar un mensaje de error
                return render_template("facturacion.html", clientes=data['clientes'], inventario=data['inventario'], facturas=data['facturas'], error="No hay suficiente inventario para uno de los productos seleccionados.")

        # Crear la factura
        factura = {
            "id": len(data['facturas']) + 1,  # Asigna un ID único a la factura
            "cliente": cliente["nombre"],
            "productos": productos_seleccionados,
            "total": total
        }
        data['facturas'].append(factura)
        guardar_datos(data)

    return render_template("facturacion.html", clientes=data['clientes'], inventario=data['inventario'], facturas=data['facturas'])

# Ruta para eliminar factura
@app.route('/facturacion/eliminar/<int:factura_id>', methods=['POST'])
def eliminar_factura(factura_id):
    data = cargar_datos()
    data['facturas'] = [factura for factura in data['facturas'] if factura['id'] != factura_id]
    guardar_datos(data)
    return redirect(url_for('facturacion'))


# Correr en la ip 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
