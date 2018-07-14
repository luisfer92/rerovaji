import controladorBaseDatos as BD
import calendar
'''
def inicializar():
	
	datos_trabajador={"nombre":"luisfer","apellido":"Rey Romero","dni":"45311514L","telefono":"627084690","contrato":40,"local":1}
	print("Generando el trabajador -> "+str(datos_trabajador))
	BD.addTrabajador(datos_trabajador)
	print("Trabajador generado")
	

	print("Generando superUsuario")
	BD.addUsuario("luisfer","luisfer_rey@yahoo.es","galletita",id_trabajador=1,rol=1)
	print("Usuario generado")
	
	print("Generando roles :")
	BD.migrarRol(1,1,1)
	BD.migrarRol(0,1,1)
	BD.migrarRol(0,0,1)
	BD.migrarRol(0,0,0)
	print("Roles generados")
	


inicializar()
'''
BD.getParteFirmasRango("21/02/2017","22/02/2018",2)