Algoritmo facturacion
	Definir nombre, categoria, producto Como Cadena
	Definir precio, cantidad, total Como Entero
	Escribir 'Facturacion:'
	Escribir 'Ingrese su nombre:'
	Leer nombre
	Escribir 'Ingrese el producto a facturar:'
	Leer producto
	Escribir 'Precio de ', producto, ':'
	Leer precio
	Escribir 'Cantidad de ', producto, ' comprado:'
	Leer cantidad
	total <- precio*cantidad
	Escribir ''
	Escribir 'Factura:'
	Escribir 'Nombre del cliente: ', nombre
	Escribir 'Producto comprado: ', producto
	Escribir 'Precio de ', producto, ': ', precio
	Escribir 'Cantidad comprada: ', cantidad
	Escribir 'Total: $', total
FinAlgoritmo
