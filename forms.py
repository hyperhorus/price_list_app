from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DecimalField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, Regexp

IMPRESION_CHOICES = [
    ('', 'Seleccionar...'),
    ('Grabado laser', 'Grabado laser'),
    ('Serigrafia', 'Serigrafia'),
    ('Tampografia', 'Tampografia'),
    ('Grabado', 'Grabado'),
    ('Grabado punta diamante', 'Grabado punta diamante'),
    ('Sublimado', 'Sublimado'),
    ('Fundido', 'Fundido'),
    ('Sandblast', 'Sandblast'),
    ('Troquelado', 'Troquelado'),
]

COLORS_CHOICES = [
    ('', 'Seleccionar...'),
    ('Rojo', 'Rojo'),
    ('Azul', 'Azul'),
    ('Verde', 'Verde'),
    ('Amarillo', 'Amarillo'),
    ('Negro', 'Negro'),
    ('Blanco', 'Blanco'),
    ('Naranja', 'Naranja'),
    ('Rosa', 'Rosa'),
    ('Morado', 'Morado'),
    ('Gris', 'Gris'),
    ('Café', 'Café'),
    ('Humo', 'Humo'),
    ('Dorado', 'Dorado'),
    ('Plateado', 'Plateado'),
    ('Dorado', 'Dorado'),
    ('Bronce', 'Bronce'),
    ('Multicolor', 'Multicolor'),
]


class ProductForm(FlaskForm):
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
        choices=IMPRESION_CHOICES,
        validators=[DataRequired(message='Seleccione una opción')]
    )

    colores = SelectField(
        'Color',
        choices=COLORS_CHOICES,
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