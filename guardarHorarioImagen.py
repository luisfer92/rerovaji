import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import six
from modelos import Horario,Trabajador
import controladorBaseDatos as BD
import os

df = pd.DataFrame()
date=None
meses=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
def recuperarHorario(fecha,local):
	ruta="./static/horarios"
	
	if not os.path.exists(ruta):
		ruta=None
	else:
		mes=meses[int(fecha.split("/")[1])-1]
		dia=fecha.split("/")[0]
		ruta=ruta+"/"+mes
		if not os.path.exists(ruta):
			ruta=None
		ruta=ruta+"/Semana_del_"+dia+"_"+str(local)+".png"

	return ruta
    	



def guardarImagen(fecha,local):
	global date
	date=fecha
	horarios=BD.getHorarioByDate(fecha,local)
	nombres=[]
	lunes=[]
	martes=[]
	miercoles=[]
	jueves=[]
	viernes=[]
	sabado=[]
	domingo=[]
	for h in horarios:
		nombres.append(BD.getTrabajadorByID(h.id_trabajador).nombre)
		lunes.append(h.lunes)
		martes.append(h.martes)
		miercoles.append(h.miercoles)
		jueves.append(h.jueves)
		viernes.append(h.viernes)
		sabado.append(h.sabado)
		domingo.append(h.domingo)
	print(nombres)

	df['Nombre'] = nombres
	df['Lunes'] = lunes
	df['Martes'] = martes
	df['Miercoles'] = miercoles
	df['Jueves'] = jueves
	df['Viernes'] = viernes
	df['Sabado'] = sabado
	df['Domingo'] = domingo

	print(len(nombres))

	generaTabla(local, df, header_columns=0, col_width=2.0)

def generaTabla(local,data, col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):

    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(True)
    

    for k, cell in  six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])

    ruta="./static/horarios"
    if not os.path.exists(ruta):
    	print("no existe")
    else:
    	mes=meses[int(date.split("/")[1])-1]
    	dia=date.split("/")[0]
    	ruta=ruta+"/"+mes
    	if not os.path.exists(ruta):
    		os.mkdir(ruta)
    		print("Ha que crear la ruta para guardar en su mes "+mes)
    	
    	ruta=ruta+"/Semana_del_"+dia+"_"+str(local)+".png"
    	ax.figure.savefig(ruta, bbox_inches='tight')



if __name__=="__main__":
	guardarImagen("30/04/2018")



