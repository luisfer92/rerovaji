var actual=null;
var semanal=false;
var graficar_dia_url=null;
var modificar_horario_url=null;
var getHoras_url=null;

$(document).ready(function(){
	graficar_dia_url=$(".graficar_dia").attr("data-url");
	modificar_horario_url=$(".modificar_horario").attr("data-url");
	getHoras_url=$(".getHoras").attr("data-url");

});

function recopilar(elemento){
	lunes=$(elemento).find("#lunes").val()
	martes=$(elemento).find("#martes").val()
	miercoles=$(elemento).find("#miercoles").val()
	jueves=$(elemento).find("#jueves").val()
	viernes=$(elemento).find("#viernes").val()
	sabado=$(elemento).find("#sabado").val()
	domingo=$(elemento).find("#domingo").val()
	turno={
			id:$(elemento).attr('id'),
			id_trabajador:$(elemento).attr('idTrabajador'),
			lunes:(lunes!=""?lunes:$(elemento).find("#lunes").attr("placeholder")),
			martes:(martes!=""?martes:$(elemento).find("#martes").attr("placeholder")),
			miercoles:(miercoles!=""?miercoles:$(elemento).find("#miercoles").attr("placeholder")),
			jueves:(jueves!=""?jueves:$(elemento).find("#jueves").attr("placeholder")),
			viernes:(viernes!=""?viernes:$(elemento).find("#viernes").attr("placeholder")),
			sabado:(sabado!=""?sabado:$(elemento).find("#sabado").attr("placeholder")),
			domingo:(domingo!=""?domingo:$(elemento).find("#domingo").attr("placeholder")),
		};
	return (turno)
}

function borrado(elemento){
	if($(elemento).val()=="" && actual==null){
		$(elemento).attr("placeholder","")
	}else if (actual!=null){
		if (!semanal){
			$(elemento).val(actual)
		}else{
			$(elemento).parents("td").siblings("td").each(function(){
				$(this).find("input").val(actual)
			});
			$(elemento).val(actual)
		}
					
	}
}


function crecer(mando){
	$(mando).css("width","40%");
	$(mando).css("height","auto");
	$(".grande").css("visibility","visible");
}

function menguar(mando){
	$(mando).css("width","80px");
	$(mando).css("height","80px");
	$(".grande").css("visibility","hidden");
}

function mando(hora,semana){
	actual=hora;
	semanal=semana;
}

function parar(){
	actual=null;
	semanal=false;
}
			
function openInNewTab(dia) {
	var horas=[]
				
	$('.'+dia).each(function(){
					
		turno=($(this).val()!=""?$(this).val():$(this).attr("placeholder"));
		horas.push(turno)
	});
	
	$.ajax({
		type: "POST",
		contentType: "application/json; charset=utf-8",
		url:graficar_dia_url,
		data: JSON.stringify({dia:dia,horas:horas}),
		success: function (data) {
					console.log(data.status);
					var win = window.open(graficar_dia_url, '_blank');//hecho
  					win.focus();
  				},
		dataType: "json"
		});
  				
}

$("#modificar").click(function() {
	var horario=[]
	$('tr').each(function (){
		r=recopilar($(this))
		if (r["id"]!=undefined){
			console.log(r)
			horario.push(r)
		}
							

	});

	
	$.ajax({
		type: "POST",
		contentType: "application/json; charset=utf-8",
		url: modificar_horario_url,
		data: JSON.stringify({horario:horario}),
		success: function (data) {
				    console.log(data.status)
				    location.reload()
				},
		dataType: "json"
		});
});

$('tr').focusout(function(){
				
	
		turno=recopilar($(this));
		delete turno.id_trabajador


	$.ajax({
		type: "POST",
		contentType: "application/json; charset=utf-8",
		url: getHoras_url,
		data: JSON.stringify({turno:turno}),
		success: function (data) {
				    console.log(data.status);
				  	$('#'+data.id_horario).find("#horas").html(data.horas);
				    if(data.limite){
				    	$('#'+data.id_horario).find("#horas").css("background","red")
				    	$('#'+data.id_horario).find("#horas").css("color","black")
				    }else{
				    	$('#'+data.id_horario).find("#horas").css({ 'background-color' : '' })
				    }
				},
		dataType: "json"
	});


});