from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

# ---------------------------- CLASES ---------------------------- #
# Clase de la base de datos 
# Lo que se hace aqui es para leer y escribir datos en el archivo JSON
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

# Clase del producto 
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
    
#Clase del Cliente
class Cliente:
    def __init__(self, id, nombre, correo):
        self.id = id
        self.nombre = nombre
        self.correo = correo

    def to_dict(self):
        return vars(self)

# Clase del proveedor
class Proveedor:
    def __init__(self, id, nombre, correo):
        self.id = id
        self.nombre = nombre
        self.correo = correo

    def to_dict(self):
        return vars(self)

# Clase de la Factura
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
#Esta pagina va a ser la primera al abrirla en el navegador
@app.route('/')
def inicio():
    return render_template('index.html')


# ---------------------------- INVENTARIO ---------------------------- #
#Esta parte es para agregar cosas a la base de datos desde el formulario
@app.route('/inventario', methods=['GET', 'POST'])
def inventario():
    if request.method == 'POST':
        nuevo_producto = Producto(
            #Lo del +1 es para cuando ya registro una vez y quieres poner otro producto no de error
            id=len(base_datos.datos['inventario']) + 1,
            nombre=request.form['nombre'],
            categoria=request.form['categoria'],
            precio=float(request.form['precio']),
            cantidad=int(request.form['cantidad']),
            unidad=request.form['unidad']
        )
        #Convierte el producto a diccionario para almacenarlo en la estructura de datos
        base_datos.datos['inventario'].append(nuevo_producto.to_dict())
        base_datos.guardar_datos()

    return render_template('inventario.html', inventario=base_datos.datos['inventario'])

#Esta parte es para borrar los productos de la base de datos
@app.route('/inventario/borrar/<int:producto_id>', methods=['POST'])
def borrar_producto(producto_id):
    base_datos.datos['inventario'] = [
        #Incluye en la nueva lista solo los productos cuyo id no sea igual al producto_id que se desea borrar.
        #El producto con el id que coincide con producto_id se borra.
        prod for prod in base_datos.datos['inventario'] if prod['id'] != producto_id]
    base_datos.guardar_datos()
    return redirect(url_for('inventario'))

#Esta parte es para que poder editar el producto ya creado
@app.route('/inventario/editar/<int:producto_id>', methods=['GET', 'POST'])
def editar_producto(producto_id):
    #EL identidicador empieza con el valor 1 y cada producto nuevo se le agrega 1 y se va sumando para cambiar de id
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

#Esta parte es para borrar los clientes 
@app.route('/clientes/borrar/<int:cliente_id>', methods=['POST'])
def borrar_cliente(cliente_id):
    #Recorre cada cliente (cli) en la lista actual.
    #Incluye en la nueva lista solo a los clientes que no tienen el mismo id que el cliente_id.
    base_datos.datos['clientes'] = [cli for cli in base_datos.datos['clientes'] if cli['id'] != cliente_id]
    base_datos.guardar_datos()
    return redirect(url_for('clientes'))



# ---------------------------- PROVEEDORES ---------------------------- #
# GET: Muestra la lista de proveedores.
# POST: Agrega un nuevo proveedor (y opcionalmente un producto).
@app.route('/proveedores', methods=['GET', 'POST'])
def proveedores():
    if request.method == 'POST':
        nuevo_proveedor = {
            #Igual que en inventario se va sumando 1 al id de provedores 
            "id": len(base_datos.datos['proveedores']) + 1,
            "nombre": request.form['nombre'],
            "correo": request.form['correo']
        }
        #Para gurdar el nuevo proveedor
        base_datos.datos['proveedores'].append(nuevo_proveedor)

        #Esto es para el formulario salga si se pone la opcion que "si"
        if request.form.get('agregar_productos') == 'si':
            nuevo_producto = Producto(
                id=len(base_datos.datos['inventario']) + 1,
                nombre=request.form['producto_nombre'],
                categoria=request.form['categoria'],
                precio=float(request.form['precio']),
                cantidad=int(request.form['cantidad']),
                unidad=request.form['unidad']
            )
            # Y aqui se guardarian los nuevos datos ingresados en el invenario
            base_datos.datos['inventario'].append(nuevo_producto.to_dict())
        base_datos.guardar_datos()
        return redirect(url_for('proveedores'))
    return render_template('proveedores.html', proveedores=base_datos.datos['proveedores'])

#Esto es para borrar un proveedor
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
        # Intenta obtener el cliente_id del formulario.     
        cliente_id = request.form.get("cliente_id")
        if not cliente_id:
            # Si no se selecciona un cliente, devuelve un mensaje de error.
            return "Debe seleccionar un cliente", 400

        # Busca el cliente correspondiente en la lista de clientes usando su id.
        cliente = next((c for c in data["clientes"] if c["id"] == int(cliente_id)), None)
        if not cliente:
           # Si el cliente no se encuentra devuelve un mensaje de error
            return "Cliente no encontrado", 404

        # Lista de ids de productos seleccionados en el formulario.
        productos_seleccionados = request.form.getlist("productos")
        productos = []
        #Variable que almacena el monto total del producto
        total = 0

        #Itera por cada producto seleccionado.
        for producto_id in productos_seleccionados:
            #Construir la clave del campo que contiene la cantidad seleccionada de un producto
            #Ejemplo: Si el producto_id es 3, entonces cantidad_key será "cantidad_3".
            cantidad_key = f"cantidad_{producto_id}"
            #La cantidad seleccionada se convierte a entero con int() para usarla al calcular
            cantidad = int(request.form.get(cantidad_key, 0))
            
            #Busca el producto en el inventario por su id.
            #Se usan dos validaciones para marcar el producto en la factura
            #1) Existe en el inventario.
            #2) La cantidad seleccionada es mayor a 0 y no excede el inventario disponible
            producto = next((p for p in data["inventario"] if p["id"] == int(producto_id)), None)
            if producto and cantidad > 0 and cantidad <= producto["cantidad"]:
                #Se añade a la lista productos con nombre, cantidad y precio.
                productos.append({
                    "producto": producto["nombre"],
                    "cantidad": cantidad,
                    "precio": producto["precio"]
                })
                #Hace el calculo del total multiplicando cantidad por el precio del producto
                total += cantidad * producto["precio"]
                #Y se resta la cantidad del inventario
                producto["cantidad"] -= cantidad
        #Si no se seleciona nada muestra un mensaje de error.
        if not productos:
            return "Debe seleccionar al menos un producto válido", 400

        #Para crear la nueva factura
        #Se suma un "1" al tamaño actual de la lista de facturas 
        nueva_factura = {
            "id": len(data["facturas"]) + 1,
            "cliente": cliente["nombre"],
            "productos": productos,
            "total": total,
            "fecha_hora": datetime.now().strftime("%I:%M %p, %d-%m-%Y")
        }
        #Se añade la nueva lista a la base de datos
        data["facturas"].append(nueva_factura)
        base_datos.guardar_datos()

        return redirect(url_for("facturacion"))

    #Muestra los datos de la factura
    return render_template(
        "facturacion.html",
        clientes=data["clientes"],
        inventario=data["inventario"],
        facturas=data["facturas"]
    )

#Esta parte es para eliminar la factura creada 
@app.route('/facturacion/eliminar/<int:factura_id>', methods=['POST'])
def eliminar_factura(factura_id):
    data = base_datos.datos
    # Filtra las facturas eliminando aquella cuyo 'id' coincida con el 'factura_id' proporcionado.
        # - Recorre todas las facturas en data['facturas'].
            # - Excluye la factura que tenga el 'id' igual al 'factura_id'.
                # - La lista resultante reemplaza la lista original de facturas.
                    # Este paso elimina la factura con el ID especificado de la base de datos.
    data['facturas'] = [factura for factura in data['facturas'] if factura['id'] != factura_id]
    base_datos.guardar_datos()
    return redirect(url_for('facturacion'))


# ---------------------------- EJECUCIÓN ---------------------------- #
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
