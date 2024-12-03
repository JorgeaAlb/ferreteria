# Sistema de Gestión de Ferretería

![](/app/frontend/static/inicio.png) 

<br> 

# 1. Descripción del problema.

### • Diseñar un sistema para representar productos, categorías, proveedores y clientes. 
### • Implementar funciones para agregar productos al inventario, gestionar las compras a proveedores, registrar las ventas a clientes y generar reportes de stock. 
### • Considerar la posibilidad de diferentes tipos de productos, con atributos específicos como medidas, materiales y unidades de medida. Este sistema de gestión de ferretería está diseñado para facilitar la administración de inventario, clientes, proveedores y facturación. 

<br> 

# 2. Definición de la solución.
### • Un Sistema de Gestión de Ferretería: Este sistema de gestión de ferretería está diseñado para facilitar la administración de inventario, clientes, proveedores y facturación.

<br> 

# 3. Diseño de la solucion.

## "Pseint"
### Inventario:

![](/doc/Inventario/pseint_inventario.png) 

<br>

## "Diagrama de Inventario"
### Diagrama de flujo:

![](/doc/Inventario/Diagrama%20de%20inventario.png) 

<br>

## "Pseint"
### Cliente:

![](/doc/Cliente/pseint_cliente.png) 

<br>

## "Diagrama de Cliente"
### Diagrama de flujo:

![](/doc/Cliente/diagrama_cliente.png)

<br>

## "Pseint"
### Proveedores:

![](/doc/Proveedores/pseint_proveedores.png) 

<br>

## "Diagrama de Proveedores"
### Diagrama de flujo:

![](/doc/Proveedores/diagrama_proveedores.png) 

<br>

## "Pseint"
### Facturacion

![](/doc/Facturacion/pseint_facturacion.png) 

<br>

## "Diagrama de Facturacion"
### Diagrama de flujo:

![](/doc/Facturacion/diagrama_facturacion.png) 

<br>
<br>

# 4. Desarrollo de la solución:
### Clases en Python:

![](/app/frontend/static/clases_python.png) 

<br>

### Formulario en HTMl:

![](/app/frontend/static/formulario_html.png) 

<br>

### Facturacion en HTML:

![](/app/frontend/static/facturacion_html.png) 

<br>

### JavaScript:

![](/app/frontend/static/javascript.png) 

<br>
<br>

# 5. Depuración y pruebas:
### Pseint.
### Prueba 1 de Inventario:
 
![](/doc/Inventario/Prueba%20de%20inventario.png) 

<br>

### HTML.
### Prueba 2 de Inventario:

![](/doc/Inventario/Prueba_python.png) 

<br>

## Pseint.
### Prueba 1 de Cliente:

![](/doc/Cliente/Prueba_cliente.png) 

<br>

## HTML.
### Prueba 2 de Cliente:

![](/doc/Cliente/prueba_python_cliente.png) 

<br>

## Pseint.
### Prueba 1 de Proveedores:

![](/doc/Proveedores/prueba_proveedor.png) 

<br>

## HTML.
### Prueba 2 de Proveedores:

![](/doc/Proveedores/prueba_python_proveedores.png) 

<br>

## Pseint.
### Prueba 1 de Facturacion:

![](/doc/Facturacion/prueba_facturacion.png) 

<br>

## HTML.
### Prueba 2 de Facturacion:

![](/doc/Facturacion//prueba_python_facturacion.png) 

<br>
<br>

# 6. Documentación:
## **Inventario:**
### • En la pestaña de **Inventario** se pide que ingrese los datos del producto por ejemplo, Su nombre, su categoria, su precio, la cantidad a agregar y la unidad de medida del producto.

### • Despues se mostrara los productos que hay en el inventario.

<br>

## **Clientes:**
### • En la segunda pestaña que es la opcion de **Clientes** se pide que se ingrese el nombre del cliente y si quiere poner su correo electronico siendo este opcional.

### • Se guardara y se mostrara en la parte inferior.

<br>

## **Proveedores:**
### • En la tercer parte del menu que es **Proveedores** se pide el nombre y correo(opcional) del proveedor y hay una opcion que es si quiere el proveedor agregar productos al inventario si se pone la opcion que **"Si"** pedira los mismos datos que en la parte de inventario y si se pone que **"No"** nomas se guardara el nombre y si ingreso el correo. 
### • Y se mostrara en la parte de abajo los proveedores guardados 

<br>

## **Facturacion:**
### • En la ultima opcion del menu que es **Facturacion** se pide que se escoga un cliente si hay mas de **1** y que escoga un producto de los de **inventario** para que haga la factura.

### • Se creara la factura con los datos del cliente, del producto y su total.
### • Y en las facturas creadas se pondra la fecha y hora de la creacion de la **factura.**