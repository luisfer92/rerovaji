from flask_wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
 
class nuevoTrabajador(Form):
    nombre = StringField('nombre', validators=[DataRequired()])
    apellido= StringField('apellidos', validators=[DataRequired()])
    dni = StringField('dni', validators=[DataRequired()])
    telefono = StringField('telefono', validators=[DataRequired()])
    contrato = IntegerField('contrato', validators=[DataRequired()])
    local=IntegerField('local',validators=[DataRequired()])

class loginForm(Form):
	email= StringField('nombre', validators=[DataRequired()])
	password=StringField('password', validators=[DataRequired()])



class registerForm(Form):
	nombre=StringField('nombre', validators=[DataRequired()])
	email= StringField('email', validators=[DataRequired()])
	password=StringField('password', validators=[DataRequired()])


