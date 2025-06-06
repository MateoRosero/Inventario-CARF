from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.file import FileAllowed

class CategoriaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    descripcion = TextAreaField('Descripción')
    submit = SubmitField('Guardar')

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=150)])
    descripcion = TextAreaField('Descripción')
    categoria = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    precio = DecimalField('Precio', validators=[DataRequired()], places=2)
    cantidad = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Guardar')

class MovimientoForm(FlaskForm):
    producto = SelectField('Producto', coerce=int, validators=[DataRequired()])
    tipo = SelectField('Tipo', choices=[('INGRESO','Ingreso'), ('SALIDA','Salida')], validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Registrar Movimiento')
