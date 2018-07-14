
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelos import Trabajador,Horario,Usuario,Rol,Usuario,Control_acceso,Ajuste
from passlib.hash import pbkdf2_sha256
import controladorBaseDatos as BD
import modelos

# conexion

base_origen='sqlite:///100M-antiguo.db'

engine = create_engine(base_origen, echo=False)

Session = sessionmaker(bind=engine)
session = Session()

def migrar_ajustes():
	try:
		ajustes=session.query(Ajuste).filter().all()

		for a in ajustes:
			BD.addAjuste(a.clave,a.valor)
			print("Migrando (ajuste):"+str(a))
	except:
		print("No existe la tabla de ajustes o hay otro problema")
	


def migrar_trabajadores():
	trabajadores=session.query(Trabajador).all()
	for t in trabajadores:
		datos={"nombre":t.nombre,"apellido":t.apellido,"dni":t.dni,"telefono":t.telefono,"contrato":t.contrato,"local":t.local}
		print("Migrando (trabajador):"+str(datos))
		BD.addTrabajador(datos)

	print("Trabajadores migrados")
def migrar_horarios():
	horarios=session.query(Horario).all()
	for h in horarios:
		semana={}
		semana["id_trabajador"]=h.id_trabajador
		semana["inicio"]=h.inicio
		semana["fin"]=h.fin
		semana["lunes"]=h.lunes
		semana["martes"]=h.martes
		semana["miercoles"]=h.miercoles
		semana["jueves"]=h.jueves
		semana["viernes"]=h.viernes
		semana["sabado"]=h.sabado
		semana["domingo"]=h.domingo
		
		print("Migrando (horario):"+str(h))
		BD.addHorario(semana,h.local)

	print("Horarios migrados")


def migrar_usuarios():
	usuarios=session.query(Usuario).all()
	for u in usuarios:	
		BD.addUsuario(u.nombre,u.correo,u.password,u.id_trabajador,u.rol)
		print("Migrando (usuario):"+str(u))

	print("Usuarios migrados")

def migrar_roles():
	roles=session.query(Rol).all()
	for r in roles:
		BD.migrarRol(r.admin,r.encargado,r.trabajador)
		print("Migrando (rol)"+str(r))
	print("Roles migrados")


def migrar_firmas():
	firmas=session.query(Control_acceso).all()
	for f in firmas:
		print("Migrando (firma)"+str(f))
		BD.generateControl(f.id_trabajador,f.entrada,f.salida,f.fecha,f.local)
	print("Firmas migradas")

def super_user():

	BD.addUsuario("luisfer","luisfer_rey@yahoo.es","galletita",id_trabajador=1,rol=1)

def migracion(datos=None):

	if not datos:
		modelos.crear_base()
		migrar_ajustes()
		migrar_trabajadores()
		#migrar_usuarios()
		migrar_horarios()
		migrar_roles()
		super_user()
		migrar_firmas()	

if __name__=="__main__":
	migracion()