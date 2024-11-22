from flask import Flask, render_template, request, redirect, url_for
import json
import os

# ---------------------------- CLASES ---------------------------- #

class BaseDatos:
    def __init__(self, archivo):
        self.archivo = archivo
        self.datos = self.cargar_datos()

    def cargar_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"inventario": [], "clientes": [], "proveedores": [], "facturas": []}

    def guardar_datos(self):
        with open(self.archivo, 'w') as file:
            json.dump(self.datos, file, indent=4)

class Producto:
    def __init__(self, id, nombre, categoria, precio, cantidad, unidad):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.cantidad = cantidad
        self.unidad = unidad

    def to_dict(self):
        return vars(self)

class Cliente:
    def __init__(self, id, nombre, correo):
        self.id = id
        self.nombre = nombre
        self.correo = correo

    def to_dict(self):
        return vars(self)

class Proveedor:
    def __init__(self, id, nombre, correo):
        self.id = id
        self.nombre = nombre
        self.correo = correo

    def to_dict(self):
        return vars(self)

class Factura:
    def __init__(self, id, cliente_id, productos, total):
        self.id = id
        self.cliente_id = cliente_id
        self.productos = productos
        self.total = total

    def to_dict(self):
        return vars(self)

# ---------------------------- CONFIGURACIÓN ---------------------------- #

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'backend', 'base_datos.json')
base_datos = BaseDatos(DATA_FILE)

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, 'frontend', 'static'),
    template_folder=os.path.join(BASE_DIR, 'frontend', 'templates')
)

# ---------------------------- RUTAS ---------------------------- #

@app.route('/')
def inicio():
    return render_template('index.html')

# ---------------------------- INVENTARIO ---------------------------- #
@app.route('/inventario', methods=['GET', 'POST'])
def inventario():
    if request.method == 'POST':
        nuevo_producto = Producto(
            id=len(base_datos.datos['inventario']) + 1,
            nombre=request.form['nombre'],
            categoria=request.form['categoria'],
            precio=float(request.form['precio']),
            cantidad=int(request.form['cantidad']),
            unidad=request.form['unidad']
        )
        base_datos.datos['inventario'].append(nuevo_producto.to_dict())
        base_datos.guardar_datos()

    return render_template('inventario.html', inventario=base_datos.datos['inventario'])

@app.route('/inventario/borrar/<int:producto_id>', methods=['POST'])
def borrar_producto(producto_id):
    base_datos.datos['inventario'] = [prod for prod in base_datos.datos['inventario'] if prod['id'] != producto_id]
    base_datos.guardar_datos()
    return redirect(url_for('inventario'))

@app.route('/inventario/editar/<int:producto_id>', methods=['GET', 'POST'])
def editar_producto(producto_id):
    producto = next((prod for prod in base_datos.datos['inventario'] if prod['id'] == producto_id), None)
    if request.method == 'POST' and producto:
        producto['nombre'] = request.form['nombre']
        producto['categoria'] = request.form['categoria']
        producto['precio'] = float(request.form['precio'])
        producto['cantidad'] = int(request.form['cantidad'])
        producto['unidad'] = request.form['unidad']
        base_datos.guardar_datos()
        return redirect(url_for('inventario'))
    return render_template('editar_producto.html', producto=producto)

# ---------------------------- CLIENTES ---------------------------- #
@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    if request.method == 'POST':
        nuevo_cliente = Cliente(
            id=len(base_datos.datos['clientes']) + 1,
            nombre=request.form['nombre'],
            correo=request.form['correo']
        )
        base_datos.datos['clientes'].append(nuevo_cliente.to_dict())
        base_datos.guardar_datos()

    return render_template('clientes.html', clientes=base_datos.datos['clientes'])

@app.route('/clientes/borrar/<int:cliente_id>', methods=['POST'])
def borrar_cliente(cliente_id):
    base_datos.datos['clientes'] = [cli for cli in base_datos.datos['clientes'] if cli['id'] != cliente_id]
    base_datos.guardar_datos()
    return redirect(url_for('clientes'))

# ---------------------------- PROVEEDORES ---------------------------- #
@app.route('/proveedores', methods=['GET', 'POST'])
def proveedores():
    if request.method == 'POST':
        nuevo_proveedor = {
            "id": len(base_datos.datos['proveedores']) + 1,
            "nombre": request.form['nombre'],
            "correo": request.form['correo']
        }
        base_datos.datos['proveedores'].append(nuevo_proveedor)

        if request.form.get('agregar_productos') == 'si':
            nuevo_producto = Producto(
                id=len(base_datos.datos['inventario']) + 1,
                nombre=request.form['producto_nombre'],
                categoria=request.form['categoria'],
                precio=float(request.form['precio']),
                cantidad=int(request.form['cantidad']),
                unidad=request.form['unidad']
            )
            base_datos.datos['inventario'].append(nuevo_producto.to_dict())

        base_datos.guardar_datos()

        return redirect(url_for('proveedores'))

    return render_template('proveedores.html', proveedores=base_datos.datos['proveedores'])


@app.route('/proveedores/borrar/<int:proveedor_id>', methods=['POST'])
def borrar_proveedor(proveedor_id):
    base_datos.datos['proveedores'] = [prov for prov in base_datos.datos['proveedores'] if prov['id'] != proveedor_id]
    base_datos.guardar_datos()
    return redirect(url_for('proveedores'))

# ---------------------------- FACTURACIÓN ---------------------------- #
@app.route("/facturacion", methods=["GET", "POST"])
def facturacion():
    data = base_datos.datos
    if request.method == "POST":
        cliente_id = request.form.get("cliente_id")
        if not cliente_id:
            return "Debe seleccionar un cliente", 400

        cliente = next((c for c in data["clientes"] if c["id"] == int(cliente_id)), None)
        if not cliente:
            return "Cliente no encontrado", 404

        productos_seleccionados = request.form.getlist("productos")
        productos = []
        total = 0

        for producto_id in productos_seleccionados:
            cantidad_key = f"cantidad_{producto_id}"
            cantidad = int(request.form.get(cantidad_key, 0))

            producto = next((p for p in data["inventario"] if p["id"] == int(producto_id)), None)
            if producto and cantidad > 0 and cantidad <= producto["cantidad"]:
                productos.append({
                    "producto": producto["nombre"],
                    "cantidad": cantidad,
                    "precio": producto["precio"]
                })
                total += cantidad * producto["precio"]

                producto["cantidad"] -= cantidad

        if not productos:
            return "Debe seleccionar al menos un producto válido", 400

        nueva_factura = {
            "id": len(data["facturas"]) + 1,
            "cliente": cliente["nombre"],
            "productos": productos,
            "total": total
        }
        data["facturas"].append(nueva_factura)
        base_datos.guardar_datos()

        return redirect(url_for("facturacion"))

    return render_template(
        "facturacion.html",
        clientes=data["clientes"],
        inventario=data["inventario"],
        facturas=data["facturas"]
    )

@app.route('/facturacion/eliminar/<int:factura_id>', methods=['POST'])
def eliminar_factura(factura_id):
    data = base_datos.datos
    data['facturas'] = [factura for factura in data['facturas'] if factura['id'] != factura_id]
    base_datos.guardar_datos()
    return redirect(url_for('facturacion'))


# ---------------------------- EJECUCIÓN ---------------------------- #
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
