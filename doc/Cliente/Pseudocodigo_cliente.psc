Algoritmo cliente
	Definir nombre, respuesta, correo Como Cadena
	Escribir 'Ingrese el nombre:'
	Leer nombre
	Escribir '¿Desea ingresar el correo electrónico? (si/no):'
	Leer respuesta
	Si respuesta='si' Entonces
		Escribir 'Ingrese el correo electrónico del cliente:'
		Leer correo
		Escribir ''
		Escribir 'Clientes: '
		Escribir 'Nombre: ', nombre
		Escribir 'Correo electrónico: ', correo
	SiNo
		Escribir ''
		Escribir 'Clientes:'
		Escribir 'Nombre: ', nombre
	FinSi
FinAlgoritmo
