function c(texto){
	salida=null;
		switch(preCorrector(texto)) {
			case 0:
				return (texto);
    		case 1:
        		spl=texto.split(/[.]|[,]|[;]|[:]/)
        		if(spl.length==3){
        			console.log("sin barra sin cierre")
        			sub=[spl[1].substring(0,2),spl[1].substring(2)].join("-")
        			
        			salida=spl[0]+":"+sub+":"+spl[2]
        			console.log(salida)
        			
        		}else if (spl.length==2){
        			console.log("sin barra con cierre")
        			sub=[spl[1].substring(0,2),spl[1].substring(2)].join("-")
        			salida=spl[0]+":"+sub
        		}else{
        			console.log("No se que coño hacer con esto que me das")
        		}
        		break;
    		case 2:

        		console.log("puntuacion in correcta")
        		aux=texto.split("-")

				salida1=aux[0].split(/[.]|[,]|[;]|[:]/)
				salida2=aux[1].split(/[.]|[,]|[;]|[:]/)
				 	
				if((salida1.length+salida2.length)==4){
					salida1=salida1[0]+":"+salida1[1]
					salida2=salida2[0]+":"+salida2[1]
					console.log("porque te has liado con los signos de puntuacion :")
					salida=salida1+"-"+salida2
					console.log("lo he arregaldo asi -> "+salida)
				}else if (RegExp("cierre").test(texto)){
					salida=salida1[0]+":"+salida1[1]+"-"+salida2
				}

        		break;
        	case 3:
        		console.log("sin ceros de los minutos")

        		if(RegExp("^[0-9]+:-[0-9]+:[0-9]{2}|^[0-9]+:-cierre$").test(texto)){
        			aux=texto.split("-")
					salida1=aux[0]+"00"
					salida2=aux[1]

					salida=salida1+"-"+salida2
        		}else{
        			aux=texto.split("-")
					salida1=aux[0]
					salida2=aux[1]+"00"

					salida=salida1+"-"+salida2
        		}
        		break;
    		default:
    			console.log("El turno no se arreglarlo -> "+texto)
        		salida="ERROR"
		}
		return(salida)	
	
}


function corrector(texto){
	console.log(texto)
	turnos=String(texto).split("/")
	if(turnos.length>=2){
		console.log(turnos)
		salida=[String(c(turnos[0])),String(c(turnos[1]))].join("/")
		
		return(salida)
	}else{
		return(c(texto))
	}
	
	/*con el codigo del error me meto en un switch y lo arreglo volviendoselo a pasar al precorrector para que identifique mas posibles fallos hasta que este me diga que no tiene fallos o que no sabe como cojones arreglarlo	*/

	
}


function preCorrector(texto){
	correcto=RegExp("^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9][-]([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$");
	correcto_con_cierre=RegExp("^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9][-](cierre)$");
	libre=RegExp("^(libre)$|^(LIBRE)$")

	sin_barra=RegExp("^([0-9]+)[:.;,]([0-9]){4}[:.;,][0-9]{2}$")//17:0021:00
	sin_barra_con_cierre=RegExp("^([0-9]+)[:.;,]([0-9]){2}(cierre)$")//17:00cierre
	puntuacion_incorrecta=RegExp("^[0-9]+[:.;,]{1}[0-9]{2}-{1}[0-9]+[:.;,]{1}[0-9]{2}");//18.00-19;00
	puntuacion_incorrecta_con_cierre=RegExp("^[0-9]+[.;,]{1}[0-9]{2}-cierre$")//17.00-cierre	
	sin_minutos=RegExp("^([0-9]+):-([0-9]+):([0-9]){2}$|([0-9]+):([0-9]){2}-([0-9]+):$");//17:00-18: o 17:-18:00
	sin_minutos_con_cierre=RegExp("^([0-9]+):-cierre$");//17:-cierre

	if (correcto.test(texto) || correcto_con_cierre.test(texto) || libre.test(texto)){
		console.log("Turno correcto")
		console.log(texto)
		return (0)
	}else{
		if (sin_barra.test(texto) || sin_barra_con_cierre.test(texto)){
			console.log("sin barra (-))")	
			return (1)	
		}else{
			if(puntuacion_incorrecta.test(texto) || puntuacion_incorrecta_con_cierre.test(texto)){
				console.log("no tiene la puntuacion correcta")
				return (2)
			}
			if(sin_minutos.test(texto) || sin_minutos_con_cierre.test(texto)){
				console.log("no tiene los minuto puestos")
				return(3)
			}
		}

		return(4)//texto no corregible

	}
}

function corregir(elemento){
	var texto=($(elemento).val()!=""?$(elemento).val():$(elemento).attr("placeholder"));
	if (texto!=""){	
		nuevo=corrector(texto)
		console.log("El texto corregido es ->"+nuevo)

		if (texto.localeCompare(nuevo)!=0 && texto.localeCompare("")!=0){
			if (RegExp("ERROR").test(nuevo)){
				$(elemento).css("background-color", "#ff1a1a");
				$(elemento).val(texto); 
			}else{
				$(elemento).css("background-color", "#ffff66");
				$(elemento).val(nuevo); 
			}
			
		}else{
			$(elemento).css("background-color","white");
		}
	}
		
}