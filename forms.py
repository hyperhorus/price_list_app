from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DecimalField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, Regexp
from models import ImpresionChoice, ColorsChoice

class ProductForm(FlaskForm):
    """Form for creating and editing products"""

    clave_producto = StringField(
        'Clave de Producto',
        validators=[
            DataRequired(message='Campo requerido'),
            Length(min=2, max=100),
            Regexp(r'^[a-zA-Z0-9_-]+$', message='Solo letras, números, guiones y guiones bajos')
        ]
    )

    tipo_producto = StringField(
        'Tipo del Producto',
        validators=[DataRequired(message='Campo requerido'), Length(min=2, max=255)]
    )

    descripcion = TextAreaField('Descripción', validators=[Optional(), Length(max=1000)])

    medidas = StringField('Medidas', validators=[Optional(), Length(max=100)])

    material = StringField('Material', validators=[Optional(), Length(max=100)])

    empaque = IntegerField(
        'Empaque (Cantidad)',
        validators=[Optional(), NumberRange(min=0, message='Debe ser mayor o igual a 0')]
    )

    impresion = SelectField(
        'Tipo de Impresión',
        choices=[],  # Will be populated dynamically
        validators=[DataRequired(message='Seleccione una opción')]
    )

    colores = SelectField(
        'Color',
        choices=[],  # Will be populated dynamically
        validators=[DataRequired(message='Seleccione un color')]
    )

    precio_unitario = DecimalField(
        'Precio Unitario',
        places=2,
        validators=[DataRequired(message='Campo requerido'), NumberRange(min=0)]
    )

    precio_mayorista = DecimalField(
        'Precio Mayorista',
        places=2,
        validators=[Optional(), NumberRange(min=0)]
    )

    precio_cliente = DecimalField(
        'Precio Cliente',
        places=2,
        validators=[Optional(), NumberRange(min=0)]
    )

    precio_promocion = DecimalField(
        'Precio Promoción',
        places=2,
        validators=[Optional(), NumberRange(min=0)]
    )

    precio_cliente_mayorista = DecimalField(
        'Precio Cliente Mayorista',
        places=2,
        validators=[Optional(), NumberRange(min=0)]
    )

    available = BooleanField('Disponible', default=True)

    submit = SubmitField('Guardar Producto')

    def __init__(self, *args, **kwargs):
        """Initialize form and load dynamic choices"""
        super(ProductForm, self).__init__(*args, **kwargs)

        # Load choices from database
        self.impresion.choices = ImpresionChoice.get_choices()
        self.colores.choices = ColorsChoice.get_choices()

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Optional, Length, Email

class CustomerForm(FlaskForm):
    nombre_empresa = StringField(
        'Empresa',
        validators=[Optional(), Length(max=150)]
    )

    contacto_nombre = StringField(
        'Contacto',
        validators=[Optional(), Length(max=100)]
    )

    email = StringField(
        'Email',
        validators=[Optional(), Email(), Length(max=100)]
    )

    telefono = StringField(
        'Teléfono',
        validators=[Optional(), Length(max=20)]
    )

    rfc = StringField(
        'RFC',
        validators=[Optional(), Length(max=15)]
    )

    submit = SubmitField('Guardar Cliente')