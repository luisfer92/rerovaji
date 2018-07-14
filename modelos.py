# -- coding: utf-8 --

from sqlalchemy import (create_engine, Column, Date, Integer, ForeignKey,String, Table)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from passlib.hash import pbkdf2_sha256
import time
 


engine = create_engine('sqlite:///100M.db', echo=True)
Base = declarative_base()

class Tema(Base):
    __tablename__="tema"
    id=Column(Integer,primary_key=True)
    tema=Column(String,nullable=False)

    def __init__(self,tema):
        self.tema=tema

    def __repr__(self):
        return (self.tema)


class Sugerencia(Base):
    __tablename__="sugerencia"
    id=Column(Integer,primary_key=True)
    id_usuario=Column(Integer,nullable=False)
    id_tema=Column(Integer,nullable=False)    
    texto=Column(String,nullable=False)
    status=Column(Integer,nullable=False)
    

    def __init__(self,id_usuario,id_tema,texto):
        self.id_usuario=id_usuario
        self.id_tema=id_tema        
        self.texte=texto
        self.status=0

    def __repr__(self):
        return ("%d : %s"%(self.id_tema,self.texto))

class Ajuste(Base):
    __tablename__="ajuste"
    id=Column(Integer,primary_key=True)
    clave=Column(String,nullable=True)
    valor=Column(String(120), nullable=False)

    def __init__(self,clave,valor):
        self.clave=str(clave).upper()
        self.valor=str(valor)

    def __repr__(self):
        return ("[%s] : %s"%(self.clave,self.valor))




class Control_acceso(Base):
    __tablename__="control_acceso"
    id=Column(Integer,primary_key=True)
    id_trabajador=Column(Integer,nullable=True)
    entrada=Column(String(120), index=True, nullable=False)
    salida=Column(String(120), index=True, nullable=True)
    fecha=Column(String(120), index=True, nullable=False)
    local=Column(Integer,nullable=False)

    def __init__(self,id_trabajador,entrada,salida,fecha,local):
        self.id_trabajador=id_trabajador
        self.entrada=time.strftime("%H:%M")
        self.salida=""
        self.fecha=time.strftime("%d/%m/%Y")
        self.local=local

    def __repr__(self):
        return (str(self.entrada)+"-"+str(self.salida)+"--"+str(self.fecha))


class Usuario(Base):
    __tablename__='usuario'
    id=Column(Integer,primary_key=True)
    nombre = Column(String(120), index=True, nullable=False)
    correo=Column(String(120),index=True,nullable=False,unique=True)
    password=Column(String(120), index=True, nullable=False)
    id_trabajador=Column(Integer,nullable=True)
    rol=Column(Integer,nullable=False)

    def __init__(self,nombre,correo,password,id_trabajador,rol=4):
        self.nombre=nombre
        self.correo=correo
        self.password=pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
        self.id_trabajador=id_trabajador
        self.rol=rol

    def __repr__(self):
        return (self.nombre+" "+str(self.id_trabajador)+" "+str(self.rol))

class Rol(Base):
    __tablename__='rol'
    id=Column(Integer,primary_key=True)
    admin=Column(Integer,nullable=False)
    encargado=Column(Integer,nullable=False)
    trabajador=Column(Integer,nullable=False)

    def __init__(self,admin,encargado,trabajador):
        self.admin=admin
        self.encargado=encargado
        self.trabajador=trabajador

    def __repr__(self):
        return(str(self.id)+" admin["+str(self.admin)+"] encargado["+str(self.encargado)+"] trabajador["+str(self.trabajador)+"]")




class Trabajador(Base):
    __tablename__ = 'trabajador'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(120), index=True, nullable=False)
    apellido = Column(String(120), nullable=False)
    dni = Column(String(13))
    telefono=Column(String(13))
    contrato=Column(Integer,nullable=False)
    local=Column(Integer,nullable=False)

    def __init__(self, nombre,apellido,dni,telefono,contrato,local):
        self.nombre=nombre
        self.apellido=apellido
        self.dni=dni
        self.telefono=telefono
        self.contrato=contrato
        self.local=local

    def __repr__(self):
        return (self.nombre+" "+self.apellido)


class Horario(Base):
    __tablename__='horario'
    id = Column(Integer, primary_key=True)
    id_trabajador=Column(Integer,nullable=False)
    inicio=Column(String,nullable=False)
    fin=Column(String,nullable=False)
    lunes=Column(String(30))
    martes=Column(String(30))
    miercoles=Column(String(30))
    jueves=Column(String(30))
    viernes=Column(String(30))
    sabado=Column(String(30))
    domingo=Column(String(30))
    horas=Column(Integer)
    local=Column(Integer, nullable=False)

    def __init__(self,id_trabajador,inicio,fin,lunes,martes,miercoles,jueves,viernes,sabado,domingo,horas,local):
        self.id_trabajador=id_trabajador
        self.inicio=inicio
        self.fin=fin
        self.lunes=lunes
        self.martes=martes
        self.miercoles=miercoles
        self.jueves=jueves
        self.viernes=viernes
        self.sabado=sabado
        self.domingo=domingo
        self.horas=horas
        self.local=local
    
    def __repr__(self):
        return (str(self.id_trabajador)+"-("+str(self.inicio)+","+str(self.fin)+") en el local "+str(self.local))        

def crear_base():
    Base.metadata.create_all(engine)


if __name__=="__main__":
   pass
    #crear trabajador

else:
    print("Modelos de base de datos importados")