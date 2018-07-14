from flask import Flask, render_template,request,flash,jsonify,redirect,url_for,session
from forms import nuevoTrabajador,loginForm,registerForm
from tiempo import Dia,Tiempo
import controladorBaseDatos as BD

import os
from utils.decoradores import rol_required,login_required
import time
from utils.filtros import nameByID,rolName,localName,isEntrada,isSalida
app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))





app.jinja_env.filters["nameByID"]=nameByID
app.jinja_env.filters["rolName"]=rolName
app.jinja_env.filters["localName"]=localName
app.jinja_env.filters["isEntrada"]=isEntrada
app.jinja_env.filters["isSalida"]=isSalida

@app.route("/switch",methods=["POST"])
@rol_required("ADMIN")
def switchLocal():
	if "inicio" in session and "fin" in session:
		session.pop("inicio")
		session.pop("fin")
	if "imagen" in session:
		session.pop("imagen")
	print("el local de la session es %s"%(localName(session["local"])))
	if session["local"]==1:
		session["local"]=2
		print("por eso cambio el local a ...%s"%(localName(session["local"])))
	else:
		session["local"]=1
	return ""

@app.route("/")
@login_required("")
def main():
	
	trabajador=BD.getTrabajadorByID(BD.getUsuarioByCorreo(session["user"]).id_trabajador)
	firmas=None
	if trabajador:

		firmas=BD.getParteFirmasMensual(trabajador.id,time.strftime("%d/%m/%Y"),trabajador.local)

	else:
		return render_template("no_autorizado.html")

	if session["rol"]=="ADMIN":
		
		return render_template("index-admin.html",firmas=firmas,trabajador=trabajador)
	elif session["rol"]=="TRABAJADOR":
		return render_template("index-trabajador.html",firmas=firmas,trabajador=trabajador)
	elif session["rol"]=="ENCARGADO":
		return render_template("index-encargado.html")
	else:
		return render_template("no_autorizado.html")

@app.route("/user/register",methods=["GET","POST"])
def register():
	if request.method=="POST":
		form = request.form
		if form["nombre"] and form["email"] and form["password"]:
			session["user"]=form["email"]
			session["password"]=form["password"]
			session["rol"]="NO AUTORIZADO"
			BD.addUsuario(form["nombre"],form["email"],form["password"])
			return redirect(url_for("main"))
		
	form=registerForm()
	return render_template("/usuarios/registro.html",form=form)
	
@app.route("/user/login", methods=["GET","POST"])
def login():
	if request.method=="POST":
		form = request.form
		if BD.checkPassword(form["email"],form["password"]):
			session["user"]=form["email"]
			session["password"]=form["password"]
			session["rol"]=BD.getRol(session["user"])
			session["local"]=1#POR DEFECTO ALCAZABILLA
			print("EL ROL DEL TRABAJADOR %s es %s"%(session["user"],session["rol"]))
			return redirect(url_for("main"))
		else:
			print("entramos por post pero no tienes acceso los datos recividos son user:%s y pass:%s "%(form["email"],form["password"]))
	form=loginForm()
	session["local"]=1
	return render_template("/usuarios/login.html",form=form)

@app.route("/user/logout")
@login_required("")
def logout():
	session.pop("user")
	session.pop("password")
	if "rol" in session:
		session.pop("rol")
	return (redirect(url_for("main")))

@app.route("/user/permisos",methods=["GET","POST"])
@rol_required("ADMIN")
def asignar_permiso():
	if request.method=="POST":

		json=request.json
		print("me llega este json -> "+str(json))
		if "rol" in json:
			BD.setRol(json["correo"],json["rol"])
			return jsonify(status="ok")
		elif "trabajador_id" in json:
			BD.setTrabajadorID(json["correo"],json["trabajador_id"])
	usuarios=BD.getUsuarios()
	trabajadores=BD.getTrabajadores(session["local"])
	return render_template("/usuarios/permisos.html",usuarios=usuarios,trabajadores=trabajadores)

@app.route("/user/eliminar", methods=["GET","POST"])
@rol_required("ADMIN")
def eliminar_usuario():
	if request.method=="POST":
		json=request.json
		for ID in json["ids"]:
			BD.removeUsuario(ID)
			return jsonify(status="ok")
		print("me llega esto papasito"+str(json))


	usuarios=BD.getUsuarios()
	return render_template("/usuarios/eliminar_usuario.html",usuarios=usuarios)





	


#___________________________________USERS___________________________________________________________#

@app.route("/trabajador/nuevo" ,methods=['GET','POST'])
def nuevo_trabajador():
	form=nuevoTrabajador()
	
	if request.method=='POST':
		f=request.form
		if form.validate_on_submit():
			BD.addTrabajador(f)
			flash("Trabajador agregado")
			
		else:
			errores=form.errors.items()
			for e in errores:
				flash("error en formulario ->"+str(e[0])+":"+str(e[1]))
			
		

	return render_template("/trabajadores/nuevo_trabajador.html",form=form)

@app.route("/trabajador/modificar")
@rol_required("ADMIN")
def modificar_trabajador():
	plantilla=BD.getTrabajadores(session["local"])
	return render_template("/trabajadores/modificar_trabajador.html",plantilla=plantilla)

@app.route("/trabajador/modificar/<id_trabajador>",methods=['GET','POST'])
def modificar(id_trabajador):
	trabajador=BD.getTrabajadorByID(id_trabajador)
	if request.method=="POST":
		print("entro a modificar el trabajador ->"+str(request.json))

		json=request.json
		datos={"id_trabajador":id_trabajador}
		posibles=["nombre","apellido","dni","telefono","contrato"]
		for p in posibles:
			if json[p]!="":
				datos[p]=json[p]

		BD.setTrabajador(datos)
		return jsonify(status="ok")
	
	return render_template("/trabajadores/modificar_ficha.html",trabajador=trabajador)


@app.route("/trabajador/borrar", methods=['GET','POST'])
@rol_required("ADMIN")
def borrar_trabajador():
	plantilla=BD.getTrabajadores(session["local"])
	if request.method=='POST':

		if "ids" in request.json:

			ids=request.json['ids']

			for i in ids:
				print(i)
				BD.removeTrabajador(i)
			return jsonify(status="ok")
		else:
			return jsonify(status="fail")
	return render_template("/trabajadores/borrar_trabajador.html",plantilla=plantilla)

@app.route("/trabajador/extras", methods=["GET"])
def horas_extra():
	mensual={}
	fecha=time.strftime("%d/%m/%Y")
	for trabajador in BD.getTrabajadores(session["local"]):
		parte_trabajador=BD.getParteFirmasMensual(trabajador.id,fecha,session["local"])
		total=0
		extras=0
		for firma in parte_trabajador:
			h_entrada,min_entrada=firma.entrada.split(":")
			h_salida,min_salida=firma.salida.split(":")

			if h_salida=="00":
				h_salida=24
			total=total+(int(h_salida)-int(h_entrada))
			print("El trabajador %s ha hecho %s horas el dia %s"%(trabajador.nombre,str(total),firma.fecha))
			if int(min_salida)>=30:
				total=total+0.5

			if int(min_entrada)>=30:
				total=total-0.5
		
		print ("Las horas de %s son %s"%(trabajador.nombre,str(total)))
		if total>trabajador.contrato:
			extras=total-trabajador.contrato
		mensual[str(trabajador.nombre)]={"trabajador":trabajador,"total":total,"extras":extras}


	return render_template("/trabajadores/horas_extra.html",extras=mensual)


#_____________________________________________________rutas horario__________________________________________



@app.route("/horario/nuevo", methods=['GET','POST'])
@rol_required("ADMIN")
def nuevo_horario():
	if request.method=="POST":
		json=request.json
		session['inicio']=str(json["inicio"])
		session['fin']=str(json["fin"])

		plantilla=BD.getTrabajadores(session["local"])
		datos={"id_trabajador":"","inicio":session["inicio"],"fin":session["fin"],
		"lunes":"","martes":"","miercoles":"","jueves":"","viernes":"","sabado":"","domingo":""}
		for trabajador in plantilla:
			datos["id_trabajador"]=trabajador.id
			BD.addHorario(datos,session["local"])
		
		return jsonify(status="ok",url=(url_for("modificar_horario")))
	return render_template("/horarios/nuevo_horario.html")

@app.route("/horario/modificar/", methods=['POST','GET'])
@rol_required("ADMIN")
def modificar_horario():

	if 'inicio' and 'fin' in session:
		if request.method=="POST":
			json=request.json
			posibles=["lunes","martes","miercoles","jueves","viernes","sabado","domingo"]

			
			for turno in json["horario"]:
				print("me llega esto ->"+str(turno))
				if len(turno)>0:#quito los elementos vacios
					datos={"id":turno["id"]}
					for dia in posibles:#quito los dias vacios
						if turno[dia]!="":
							datos[dia]=turno[dia]
					if len(datos)>1:#quito los dias sin modificaciones
						print (str(datos))
						BD.setHorario(datos)

			#saveH.guardarImagen(session['inicio'],session["local"])
			session.pop("inicio")
			session.pop("fin")

			return jsonify(status="ok")
		
		horario=BD.getHorarioByDate(session['inicio'],session["local"])
		tiempo=Tiempo().get_tiempo(session['inicio'],session['fin'])
		print(tiempo)
		return(render_template("/horarios/modificar_horario.html",horario=horario,inicio=session['inicio'],fin=session['fin'],tiempo=tiempo))
	elif 'imagen' in session:
		return(redirect(url_for("mostrar_horario")))
	else:
		horarios=BD.getFechasHorarios(session["local"])
		if request.method=="POST":
			json=request.json
			session["inicio"]=json['inicio']
			session["fin"]=json["fin"]

			return jsonify(status="ok")
			
		return(render_template("/horarios/lista_horarios.html",horarios=horarios))

@app.route("/horario/borrar",methods=["POST"])
def borrar_horario():
	fecha=request.json['id_horario']
	BD.removeHorariosByDate(fecha,session["local"])
	return jsonify(status="ok")

@app.route("/horario/salir")
def salir_sin_guardar():
	session.pop("inicio")
	session.pop("fin")
	return (redirect(url_for("modificar_horario")))

	


@app.route("/horario/get_horas",methods=['POST'])
def getHoras():
	json=request.json
	id_horario=json['turno']['id']
	json['turno'].pop('id')
	horas=BD.getHoras(json['turno'])
	limite=(BD.getTrabajadorByID(BD.getHorarioByID(id_horario).id_trabajador).contrato<horas)
	
	

	print (json)
	return jsonify(status="ok",id_horario=id_horario,horas=horas,limite=limite)


@app.route("/horario/enviar",methods=["POST"])
@rol_required("ADMIN")
def enviar_horario():
	if request.method=="POST":
		json=request.json
		
		if session["local"]==1:
			print("Hola")
		
			id_ajuste=BD.getAjusteByClave("ALCAZABILLA_HORARIO_ACTUAL").id
			BD.setValorAjuste(id_ajuste,json["inicio"])



		session['inicio']=json['inicio']
		return jsonify(status="ok",)

@app.route("/horaio/image")
@login_required("")
def mostrar_horario():
	inicio=None
	if session["local"]==1:
		inicio=BD.getAjusteByClave("ALCAZABILLA_HORARIO_ACTUAL").valor
	else:
		inicio=BD.getAjusteByClave("PACIFICO_HORARIO_ACTUAL").valor

	horario=BD.getHorarioByDate(inicio,session["local"])
	return(render_template("/horarios/mostrarHorario.html",horario=horario))

#__________________________________________GRAFICOS_______________________________
@app.route("/graficos/dia",methods=["POST","GET"])
def graficar_dia():
	if request.method=="POST":
		json=request.json
		keys,values=personas_hora(json["horas"])
		session["keys"]=keys
		session["values"]=values

		session["dia"]=json["dia"]
		
		#dia={"dia":json["dia"],"horas"}
		return jsonify(status="ok")
	keys=session["keys"]
	values=session["values"]
	dia=session["dia"]
	#session.pop("ph")
	#session.pop("dia")
	return(render_template("/horarios/graficos.html",keys=keys,values=values,dia=dia))


def is_in_intervalo(intervalo,valor):
	if intervalo.upper()!="LIBRE":
		if intervalo=="":
			return(False)
		elif "/" in intervalo:
			a=intervalo.split("/")[0]
			b=intervalo.split("/")[1]
			
			return (is_in_intervalo(a,valor) or is_in_intervalo(b,valor))
		else:
			
			inicio=intervalo.split("-")[0]
			fin=intervalo.split("-")[1]
			if fin.upper()=="CIERRE":
				fin="24:00"
			else:
				pass
			min_ini=int(inicio.split(":")[1])
			min_fin=int(fin.split(":")[1])
			inicio=int(inicio.split(":")[0])
			fin=int(fin.split(":")[0])
			if min_ini==30:
				inicio=inicio+0.5
			if min_fin==30:
				fin=fin+0.5
		return(valor>=float(inicio) and valor<float(fin))
	else:
		return (False)

def personas_hora(horas):
	#personas cada media hora!!
	a=8#apertura por mercancia
	c=25#cierre
	personas_hora={}
	for h in range(a,c,1):#creeo el diccionario con las horas
		personas_hora[str(h)]=0
		h=h+0.5
		personas_hora[str(h)]=0
		

	for hora in personas_hora.keys():
		for intervalo in horas:
			
			if is_in_intervalo(intervalo,float(hora)):
				personas_hora[hora]=personas_hora[hora]+1
	personas_hora.pop("24.5")
	cierre=personas_hora["24"]
	personas_hora.pop("24")
	personas_hora["cierre"]=cierre
	keys=[]
	vals=[]
	for k in personas_hora.keys():
		v=None

		if "." in k:
			v=personas_hora[k]
			k=k.split(".")[0]+":30"

		else:
			v=personas_hora[k]
			if k!="cierre":
				k=k+":00"

		
		keys.append(k)
		vals.append(v)

	
	
	return(keys,vals)

#___________________PARTE FIRMAS_____________________

@app.route("/firmas/entrada/",methods=["POST"])
@rol_required("ADMIN")
def addEntrada():
	json=request.json
	correo=BD.getUsuarioByTrabajadorID(json["trabajador_id"]).correo
	if correo:
		if(BD.checkPassword(correo,json["password"])):
			BD.addEntrada(json["trabajador_id"],session["local"])
			print("CORRECTO")
			return jsonify(status="ok")
	else:
		return jsonify(status="error")


@app.route("/firmas/salida/",methods=["POST"])
@rol_required("ADMIN")
def addSalida():
	json=request.json
	correo=BD.getUsuarioByTrabajadorID(json["trabajador_id"]).correo
	if correo:
		if(BD.checkPassword(correo,json["password"])):
			BD.addSalida(json["trabajador_id"])
			print("CORRECTO")
			return jsonify(status="ok")
	else:
		return jsonify(status="error")

@app.route("/firmas/firmar")
@rol_required("ADMIN")
def firmar():
	trabajadores=BD.getTrabajadores(session["local"])
	firmas=BD.getPartefirmasHoy(session["local"])
	return render_template("/firmas/firmar.html",plantilla=trabajadores,firmas=firmas)

@app.route("/firmas/modificar", methods=["GET", "POST"])
def modificar_firma():

	if request.method=="POST":
		firmas_totales={}
		session["parte"]=request.json["inicio"]

		print(firmas_totales)

		return jsonify(firmas=firmas_totales)
	

	if "parte" in session:
		firmas=[]

		for t in BD.getTrabajadores(session["local"]):
			firmas.append(BD.getParteFirmasMensual(t.id,session["parte"],t.local))
			
		session.pop("parte")
		return render_template("/firmas/parte_mensual.html",parte=firmas)
	return render_template("/firmas/seleccionar_fecha_firmas.html")

@app.route("/firmas/modificar/post", methods=["POST"])
def modificar_firma_post():
	json=request.json["datos"]
	print(json)
	
	for parte in json:
		BD.setFirma(parte["id_parte"],parte["entrada"],parte["salida"],parte["fecha"])

	
	

	return jsonify(status="ok")


@app.route("/firmas/registro/mensual",methods=["GET","POST"])
@rol_required("ADMIN")
def registro_mensual():
	if request.method=="POST":
		return "POST"

	return None


#_______________________________________________Ajustes__________________________________

@app.route("/ajustes/all" , methods=["GET"])
def ajustes():
	ajustes=BD.getAjustes()
	return render_template("ajustes.html",ajustes=ajustes)

@app.route("/ajustes/crear", methods=["POST"])
def crear_ajuste():
	json=request.json
	BD.addAjuste(json["clave"],json["valor"])
	
	return jsonify(status="ok")		

@app.route("/ajustes/borrar", methods=["POST"])
def borrar_ajuste():
	json=request.json
	BD.removeAjuste(json["id_ajuste"])
	

	return jsonify(status="ok")

#______________________________________Sugerencias_______________

@app.route("/sugerencias/all", methods=["GET"])
def sugerencias():
	sugerencias=BD.getSugerencias()
	temas=BD.getTemas()
	return render_template("sugerencias.html",sugerencias=sugerencias,temas=temas)


@app.route("/sugerencias/crear", methods=["POST"])
def crear_sugerencia():
	json=reques.json
	id_usuario=BD.getUserByCorreo(session["user"])
	BD.addSugerencia(id_usuario,json["id_tema"],json["texto"])
		

if __name__=="__main__":
	host= '0.0.0.0'
	app.run(host=host, debug=True)
	#app.run()