import controladorBaseDatos as BD
from flask import session
import time 
def nameByID(id_trabajador):
	nombre="NO ASIGNADO"
	if id_trabajador!=0:
		nombre=BD.getTrabajadorByID(id_trabajador).nombre
	return nombre

def rolName(id_rol):
	return BD.getNombreRol(id_rol)

def localName(id_local):
	local="ALCAZABILLA"
	if session["local"]==2:
		local="PACIFICO"
	return local

def isEntrada(id_trabajador):
	fecha=time.strftime("%d/%m/%Y")
	print(fecha)
	c=BD.getControles(id_trabajador,fecha,session["local"])#por si tiene partidos
	print (c)
	if len(c)==1 and c[0].entrada!="" and c[0].salida=="":
		return c[0].entrada
	elif len(c)>1 and c[1].entrada!="" and c[1].salida=="":
		return c[1].entrada 

	return ""

def isSalida(id_trabajador):
	fecha=time.strftime("%d/%m/%Y")
	print(fecha)
	c=BD.getControles(id_trabajador,fecha,session["local"])#por si tiene partidos
	print (c)
	if len(c)==1 and c[0].salida!="" and c[0].entrada!="":
		return c[0].salida
	elif len(c)>1 and c[1].salida!="" and c[1].entrada!="":
		return c[1].salida 

	return ""

