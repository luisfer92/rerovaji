

# -- coding: utf-8 --


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelos import Trabajador,Horario,Usuario,Rol,Control_acceso,Ajuste,Sugerencia,Tema
from passlib.hash import pbkdf2_sha256
import time
import calendar

# conexion
engine = create_engine('sqlite:///100M.db', echo=False)
# sesion
Session = sessionmaker(bind=engine)
session = Session()

#__________________________________MIGRACIONES___________________________________________________

def migrarTrabajador(trabajador):
	session.add(trabajador)
	session.commit()

def migrarHorario(horario):
	session.add(horario)
	session.commit()

def migrarUsuario(usuario):
	session.add(usuario)
	session.commit()
def migrarRol(admin,encargado,trabajador):
	r=Rol(admin,encargado,trabajador)
	session.add(r)
	session.commit()

#_________________________________TRABAJADORES____________________________________________________



def _generarTrabajador(datos):
	return Trabajador(datos["nombre"],datos["apellido"],datos["dni"],datos["telefono"],datos["contrato"],datos["local"])

def getTrabajadores(local):
	return session.query(Trabajador).filter(Trabajador.local==local).all()

def getTrabajadorByID(id_trabajador):
	return session.query(Trabajador).filter(Trabajador.id==id_trabajador).first()

def addTrabajador(datos):#diccionario de datos
	print ("se va a generar un trabajador con los siguientes datos "+str(datos))
	t=_generarTrabajador(datos)
	session.add(t)
	session.commit()

def removeTrabajador(id_trabajador):
	t=getTrabajadorByID(id_trabajador)
		
	usuario=session.query(Usuario).filter(Usuario.id_trabajador==t.id).first()
	if usuario:
		session.delete(usuario)
		session.commit()

	horarios=session.query(Horario).filter(Horario.id_trabajador==t.id).all()
	if (len(horarios)>0):
		for h in horarios:
			session.delete(h)
			session.commit()
	session.delete(t)
	session.commit()

def setTrabajador(datos):#datos a cambiar debe contener almenos dos elementos el id del trabajador y un dato a cambiar 
	if "id_trabajador" in datos and len(datos)>1:
		
		tr=getTrabajadorByID(datos["id_trabajador"])
		posibles={"nombre":tr.nombre,"apellido":tr.apellido,"dni":tr.dni,"telefono":tr.telefono,"contrato":tr.contrato,"local":tr.local}
		print ("el trabajador a modificar es ->"+str(tr))
		for cambio in posibles:
			if cambio in datos:
				posibles[cambio]=datos[cambio]
		cambiado=_generarTrabajador(posibles)
		tr.nombre=cambiado.nombre
		tr.apellido=cambiado.apellido
		tr.dni=cambiado.dni
		tr.telefono=cambiado.telefono
		tr.contrato=cambiado.contrato
		tr.local=cambiado.local
		session.commit()
		print(tr)



#___________________________________HORARIOS________________________________________________________
def getHoras(datos):
	semana=["lunes","martes","miercoles","jueves","viernes","sabado","domingo"]
	horas=0
	for dia in semana:
		if "/" in datos[dia]:
			
			turno1,turno2=datos[dia].split("/")
			inicio1,fin1=turno1.split("-")
			inicio2,fin2=turno2.split("-")

			inicio1=int(inicio1.split(":")[0])
			inicio2=int(inicio2.split(":")[0])
			if fin2.upper()!="CIERRE":
				fin1=int(fin1.split(":")[0])
				fin2=int(fin2.split(":")[0])
			else:
				fin1=int(fin1.split(":")[0])
				fin2=0

			if fin1==0:
				fin1=24
			if fin2==0:
				fin2=24

			horas=horas+(fin1-inicio1)+(fin2-inicio2)
			
		else:
			separacion=datos[dia].split("-")
			print("posible petada +"+str(separacion))
			if len(separacion)>1:# cuando es 0 es dia libre
				inicio=separacion[0]
				fin=separacion[1]

				if fin.upper()=="CIERRE":
					fin="24:00"

				min_ini=int(inicio.split(":")[1])
				min_fin=int(fin.split(":")[1])
				inicio=int(inicio.split(":")[0])				
				fin=int(fin.split(":")[0])
				if fin==0:
					fin=24
				horas=horas+(fin-inicio)
				if min_ini==30:
					horas=horas-0.5
				if min_fin==30:
					print("media hora al final")
					horas=horas+0.5
		
	print ("el trabajador tiene -> %d horas esta semana"%(horas))
	return horas

def getHorarios():
	return session.query(Horario).all()



def getHorarioByID(id_horario):
	return session.query(Horario).filter(Horario.id==id_horario).first()

def getHorarioByDate(fecha,local):
	return session.query(Horario).filter(Horario.inicio==fecha).filter(Horario.local==local).all()

def getHorarioByTrabajadorID(id_trabajador,fecha):
	return session.query(Horario).filter(Horario.id_trabajador==id_trabajador).filter(Horario.inicio==fecha).first()

def setHorario(datos):#id trabajador y cada dia(s) de la semana a modificar [{"id":"","lunes":,"martes":}]
	if "id" in datos:

		h=getHorarioByID(datos["id"])
		posibles={"id_trabajador":h.id_trabajador,"lunes":h.lunes,
		"martes":h.martes,"miercoles":h.miercoles,"jueves":h.jueves,
		"viernes":h.viernes,"sabado":h.sabado,"domingo":h.domingo}

		for cambio in posibles:
			if cambio in datos:
				posibles[cambio]=datos[cambio]
		h.id_trabajador=posibles["id_trabajador"]
		h.lunes=posibles["lunes"]
		h.martes=posibles["martes"]
		h.miercoles=posibles["miercoles"]
		h.jueves=posibles["jueves"]
		h.viernes=posibles["viernes"]
		h.sabado=posibles["sabado"]
		h.domingo=posibles["domingo"]
		h.horas=getHoras(posibles)
		session.commit()
		



def addHorario(datos,local):#semana del trabajador =datos
	
	print ("la fecha del horario es -...."+datos['inicio'])

	if not (getHorarioByTrabajadorID(datos["id_trabajador"],datos["inicio"])):
		h=Horario(datos["id_trabajador"],datos["inicio"],datos["fin"],
			datos["lunes"],datos["martes"],datos["miercoles"],datos["jueves"],
			datos["viernes"],datos["sabado"],datos["domingo"],getHoras(datos),local)
		session.add(h)
		session.commit()
	else:
		print("El horario ya existe no lo voy a crear")
		
	

def removeHorariosByDate(fechaInicio,local):
	horarios=session.query(Horario).filter(Horario.inicio==fechaInicio).filter(Horario.local==local).all()
	for h in horarios:
		session.delete(h)
		session.commit()

def removeHorarioByID(id_horario):
	h=session.query(Horario).filter(Horario.id==id_horario).first()
	session.delete(h)
	session.commit()

def getFechasHorarios(local):
	horarios=session.query(Horario).filter(Horario.local==local).all()
	ant=None
	resultado=[]
	for h in horarios:
		if ant!=h.inicio:
			ant=h.inicio
			resultado.append(h)

	return resultado


#______________________________________________USUARIOS_____________________________________________
def addUsuario(nombre,correo,password,id_trabajador=0,rol=0):
	user=Usuario(nombre,correo,password,id_trabajador,rol)
	session.add(user)
	session.commit()

def removeUsuario(id_usuario):
	user=getUsuarioByID(id_usuario)
	session.delete(user)
	session.commit()

def getUsuarios():
	return session.query(Usuario).all()

def getUsuarioByID(id_usuario):
	user=session.query(Usuario).filter(Usuario.id==id_usuario).first()
	return(user)

def getUsuarioByCorreo(correo):
	user=session.query(Usuario).filter(Usuario.correo==correo).first()
	return(user)

def getUsuarioByTrabajadorID(id_trabajador):
	user=session.query(Usuario).filter(Usuario.id_trabajador==id_trabajador).first()
	return (user)
def removeUsuario(id_usuario):
	user=getUsuarioByID(id_usuario)
	session.delete(user)
	session.commit()

def setTrabajadorID(correo,id_trabajador):
	user=getUsuarioByCorreo(correo)
	user.id_trabajador=id_trabajador
	session.commit()


def setRol(correo,rol):
	user=getUsuarioByCorreo(correo)
	user.rol=rol
	session.commit()

def getNombreRol(rol):
	x="NO AUTORIZADO"
	if rol==1:
		x="ADMIN"
	elif rol==2:
		x="ENCARGADO"
	elif rol==3:
		x="TRABAJADOR"
	return x

def getRol(correo):
	user=getUsuarioByCorreo(correo)
	
	return getNombreRol(user.rol)



def setUsuarioTrabajadorID(id_usuario,id_trabajador):
	user=getUsuarioByID(id_usuario)
	user.id_trabajador=id_trabajador
	session.commit()

def checkPassword(correo,password):
	user=getUsuarioByCorreo(correo)
	if user:
		return (pbkdf2_sha256.verify(password, user.password))
	return False

#________________________CONTROL_ACCESO_________________________

def getParteFirmasMensual(id_trabajador,inicio,local):
	#print("empezamos a buscar desde la fecha "+str(inicio))
	parte=[]
	inicio=inicio.split("/")
	mes=inicio[1]
	year=inicio[2]
	rango=calendar.monthrange(int(year),int(mes))
	#print("calendario ajustado para -"+str(rango))
	for dia in range(1,rango[1]):
		if((dia)<10):
			dia="0"+str(dia)
		fecha="%s/%s/%s"%(str(dia),mes,year)
		#print("Buscando las firmas de %s para el dia (%s)"%(getTrabajadorByID(id_trabajador).nombre,fecha))
		c_acceso=getControles(id_trabajador,fecha,local)
		#print("encuentro to esta mierda "+str(c_acceso))
		for c in c_acceso:
			if c_acceso:
				parte.append(c)
	return parte


def getPartefirmasHoy(local):
	fecha=time.strftime("%d/%m/%Y")
	return(session.query(Control_acceso).filter(Control_acceso.local==local).filter(Control_acceso.fecha==fecha).all())


def addEntrada(id_trabajador,local):
	c_acceso=Control_acceso(id_trabajador,"entrada","salida","fecha",local)
	session.add(c_acceso)
	session.commit()

def addSalida(id_trabajador):

	fecha=time.strftime("%d/%m/%Y")
	fini=fecha
	salida=time.strftime("%H:%M")
	c_acceso=getControl(id_trabajador,fecha)
	if not c_acceso:
		print("probando un dia menos")
		f=fecha.split("/")
		dia=str(int(f[0])-1)
		if (len(dia)==1):
			dia="0"+str(dia)
		mes=f[1]
		year=f[2]
		fecha="%s/%s/%s"%(dia,mes,year)
		print(fecha)
		c_acceso=getControl(id_trabajador,fecha)
		if not c_acceso:
			print("probando un mes menos")
			mes=str(int(mes)-1)
			if len(mes)==1:
				mes="0"+mes
			dia=str(calendar.monthrange(int(year),int(mes))[1])
			fecha="%s/%s/%s"%(dia,mes,year)
			print(fecha)
			c_acceso=getControl(id_trabajador,fecha)
			if not c_acceso:
				print("probando noche vieja")
				year=str(int(year)-1)
				if(len(year)==1):
					year="0"+year
				mes="12"
				dia="31"
				fecha="%s/%s/%s"%(dia,mes,year)
				print(fecha)
				c_acceso=getControl(id_trabajador,fecha)

	if c_acceso:
		print ("salida (%s) alamcenada en BD ->%s"%(salida,str(c_acceso)))
		c_acceso.salida=salida
		session.commit()
	else:
		print("ERROR en cierre (%s) de %s"%(fini,getTrabajadorByID(id_trabajador).nombre))
	


def modificarEntrada(id_trabajador,fecha,hora):
	c_acceso=getControl(id_trabajador,fecha)
	c_acceso.entrada=hora
	session.commit()

def modificarSalida(id_trabajador,fecha,salida):
	c_acceso=getControl(id_trabajador,fecha)
	c_acceso.salida=salida
	session.commit()

def setFirma(id_firma,entrada,salida,fecha):
	c_acceso=session.query(Control_acceso).filter(Control_acceso.id==id_firma).first()
	c_acceso.entrada=entrada
	c_acceso.salida=salida
	c_acceso.fecha=fecha
	session.commit()

def generateControl(id_trabajador,entrada,salida,fecha,local):
	c_acceso=Control_acceso(id_trabajador,entrada,salida,fecha,local)
	session.add(c_acceso)
	session.commit()

def getControl(id_trabajador,fecha):
	c=session.query(Control_acceso).filter(Control_acceso.id_trabajador==id_trabajador).filter(Control_acceso.fecha==fecha).all()
	if c:
		return c[-1]
	return c

def getControles(id_trabajador,fecha,local):
	c=session.query(Control_acceso).filter(Control_acceso.id_trabajador==id_trabajador).filter(Control_acceso.fecha==fecha).filter(Control_acceso.local==local).all()
	return c


#__________________________________________ AJUSTES_______________________________________________________-


def getAjuste(id_ajuste):
	return(session.query(Ajuste).filter().first())

def getAjustes():
	return (session.query(Ajuste).filter().all())

def getAjusteByClave(clave):
	return (session.query(Ajuste).filter(Ajuste.clave==clave).first())

def setAjuste(id_ajuste, clave,valor):
	ajuste=getAjuste(id_ajuste)
	ajuste.clave=str(clave).upper()
	ajuste.valor=str(valor)

def setClaveAjuste(id_ajuste,clave):
	ajuste=getAjuste(id_ajuste)
	ajuste.clave=str(clave).upper()
	session.commit()

def setValorAjuste(id_ajuste,valor):
	ajuste=getAjuste(id_ajuste)
	ajuste.valor=str(valor)
	session.commit()

def removeAjuste(id_ajuste):
	ajuste=getAjuste(id_ajuste)
	if ajuste:
		session.delete(ajuste)
		session.commit()

def addAjuste(clave,valor):
	ajuste=Ajuste(clave,valor)
	session.add(ajuste)
	session.commit()



#___________________________________________TEMAS_________________________________

def addTema(tema):
	t=Tema(tema)
	session.add(t)
	session.commit()

def getTema(id_tema):
	return (session.query(Tema).filter(Tema.id==id_tema).first())

def getTemas():
	return(session.query(Tema).all())

def setTema(id_tema,tema):
	t=getTema(id_tema)
	t.tema=tema
	session.commit()

def removeTema(id_tema):
	t=getTema(id_tema)
	session.delete(t)
	session.commit()	

#___________________________________________ SUGERENCIAS___________________________

def addSugerencia(id_usuario,id_tema,texto):
	s=Sugerencia(id_usuario,id_tema,texto)
	session.add(s)
	session.commit()

def getSugerencia(id_sugerencia):
	return session.query(Sugerencia).filter(Sugerencia.id==id_sugerencia).first()

def getSugerencias():
	return session.query(Sugerencia).all()

def setTextoSugerencia(id_sugerencia,texto):
	s=getSugerencia(id_sugerencia)
	s.texto=texto
	session.commit()

def setTemaSugerecia(id_sugerencia,id_tema):
	s=getSugerencia(id_sugerencia)
	s.id_tema=id_tema
	session.commit()

def setStatus(id_sugerencia,status):
	s=getSugerencia(id_sugerencia)
	s.status=status
	session.commit()

def removeSugerencia(id_sugerencia):
	s=getSugerencia(id_sugerencia)
	session.delete(s)
	session.commit()

if __name__=="__main__":
	pass
	
else:
	print("Controlador de base de datos importado")