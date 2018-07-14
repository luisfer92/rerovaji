from bs4 import BeautifulSoup
import requests
import time



class Dia(object):
	"""docstring for Dia"""
	def __init__(self, fecha,maximo,minimo,lluvia,viento):
		super(Dia, self).__init__()
		self.fecha=fecha
		self.maximo=maximo
		self.minimo=minimo
		self.lluvia=lluvia
		self.viento=viento


	def __str__(self):
		return("Dia:"+self.fecha+",Tº max:"+self.maximo+",Tº min:"+self.minimo+",LLuvia:"+self.lluvia+",Viento:"+self.viento)

	def __eq__(self,dia):
		return (dia.fecha==self.fecha)
		
		
		


class Tiempo(object):
	"""docstring for Tiempo"""
	def __init__(self):
		super(Tiempo, self).__init__()
		self.semana=self.getDias()
		

	def getDias(self):
		r  = requests.get("https://www.eltiempo.es/malaga.html")
		data = r.text
		soup = BeautifulSoup(data,"lxml")
		cuadro=soup.findAll("div", class_= "m_table_weather_day_wrapper")[0]
		columnas=cuadro.findAll("div")
		posible=[]
		semana=[]
		flag_hora=False
		for c in columnas:
			aux=(c.text.strip()).split(" ")
			for p in aux:
				x=(p.split("\n"))
				for y in x:
					if(y!=""):
						if(y.find(":"))==-1:
							posible.append(y)
						else:
							if not flag_hora:
								flag_hora=True
							else:
								if len(posible)>1:
									dia=self.crearDia(posible)
									existe=False
									for d in semana:
										if d==dia:
											existe=True
											break
									if not existe:
										semana.append(dia)
									else:
										existe=False
									
								posible=[]
		return (semana)

	def get_tiempo(self,inicio,fin):
		index_ini=0
		index_fin=0
		for dia in self.semana:
			if dia.fecha==inicio:
				index_ini=int(self.semana.index(dia))			
			elif dia.fecha==fin:
				index_fin=int(self.semana.index(dia))+1
		
		return (self.semana[index_ini:index_fin])		


	def crearDia(self,datos):

		tam=len(datos)
		actual=(time.strftime("%d/%m/%Y")).split("/")
		dia=datos[2]
		if(len(dia))==1:
			dia="0"+dia

		fecha=dia+"/"+actual[1]+"/"+actual[2]
		maximo=datos[4]+"C"
		minimo=datos[5]+"C"
		lluvia=""
		viento=""
		if(tam==15):			
			lluvia=datos[10]+"mm"
			viento=datos[13]+"km/h"
		else:
			lluvia=datos[7]+"mm"
			viento=datos[10]+"km/h"
		d=Dia(fecha,maximo,minimo,lluvia,viento)
		
		return (d)


if __name__ ==("__main__"):
	print("Recopilando info")
	t=Tiempo()
	print(t.semana)
	print(t.get_tiempo("04/06/2018","10/06/2018"))
else:
	print("Tiempo importado")
		





