Algoritmo proveedores
	Definir proveedor, respuesta1, respuesta2, correo, inventario Como Cadena
	Definir nombre, categoria, precio, cantidad Como Cadena
	correo <- ''
	Escribir ''
	Escribir 'Proveedores:'
	Escribir 'Ingrese el nombre del proveedor:'
	Leer proveedor
	Escribir '¿Desea ingresar el correo electrónico? (si/no):'
	Leer respuesta1
	Si respuesta1='si' Entonces
		Escribir 'Ingrese el correo electrónico del proveedor:'
		Leer correo
	FinSi
	Escribir ''
	Escribir 'Quieres agregar productos al inventario? (si/no)'
	Leer respuesta2
	Si respuesta2='si' Entonces
		Escribir 'Nombre del objeto:'
		Leer nombre
		Escribir 'Categoría de '+nombre+':'
		Leer categoria
		Escribir 'Precio de '+nombre+':'
		Leer precio
		Escribir 'Cantidad de '+nombre+':'
		Leer cantidad
		Escribir ''
		Escribir 'Proveedores:'
		Escribir 'Nombre del proveedor: ', proveedor
		Escribir 'Correo electrónico: ', correo
		Escribir ''
		Escribir 'Inventario: '
		Escribir 'Nombre: '+nombre
		Escribir 'Categoria: '+categoria
		Escribir 'Precio: $'+precio
		Escribir 'Cantidad: '+cantidad
	FinSi
FinAlgoritmo
