from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customers'  # IMPORTANT: matches existing table name

    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_empresa = db.Column(db.String(150))
    contacto_nombre = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    rfc = db.Column(db.String(15))

    def __repr__(self):
        return f'<Customer {self.nombre_empresa}>'

    def to_dict(self):
        return {
            'customer_id': self.customer_id,
            'nombre_empresa': self.nombre_empresa,
            'contacto_nombre': self.contacto_nombre,
            'email': self.email,
            'telefono': self.telefono,
            'rfc': self.rfc,
        }

class ImpresionChoice(db.Model):
    """Table for printing method choices"""
    __tablename__ = 'impresion_choice'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    activo = db.Column(db.Boolean, default=True, nullable=False)
    orden = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ImpresionChoice {self.nombre}>'

    @staticmethod
    def get_choices():
        """Get active choices for dropdown"""
        choices = ImpresionChoice.query.filter_by(activo=True).order_by(ImpresionChoice.orden,
                                                                        ImpresionChoice.nombre).all()
        return [('', 'Seleccionar...')] + [(c.nombre, c.nombre) for c in choices]


class ColorsChoice(db.Model):
    """Table for color choices"""
    __tablename__ = 'colors_choice'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    codigo_hex = db.Column(db.String(7))  # Optional: for displaying color
    activo = db.Column(db.Boolean, default=True, nullable=False)
    orden = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ColorsChoice {self.nombre}>'

    @staticmethod
    def get_choices():
        """Get active choices for dropdown"""
        choices = ColorsChoice.query.filter_by(activo=True).order_by(ColorsChoice.orden, ColorsChoice.nombre).all()
        return [('', 'Seleccionar...')] + [(c.nombre, c.nombre) for c in choices]

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer,  primary_key=True)
    clave_producto = db.Column(db.String(100), unique=True, nullable=False, index=True)
    tipo_producto = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    medidas = db.Column(db.String(100))
    material = db.Column(db.String(100))
    empaque = db.Column(db.Integer)
    impresion = db.Column(db.String(50))
    colores = db.Column(db.String(100))
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    precio_mayorista = db.Column(db.Numeric(10, 2))
    precio_cliente = db.Column(db.Numeric(10, 2))
    precio_promocion = db.Column(db.Numeric(10, 2))
    precio_cliente_mayorista = db.Column(db.Numeric(10, 2))
    available = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Product {self.clave_producto}>'

    def to_dict(self):
        return {
            'id': self.id,
            'clave_producto': self.clave_producto,
            'tipo_producto': self.tipo_producto,
            'descripcion': self.descripcion,
            'medidas': self.medidas,
            'material': self.material,
            'empaque': self.empaque,
            'impresion': self.impresion,
            'colores': self.colores,
            'precio_unitario': float(self.precio_unitario) if self.precio_unitario else 0,
            'precio_mayorista': float(self.precio_mayorista) if self.precio_mayorista else 0,
            'precio_cliente': float(self.precio_cliente) if self.precio_cliente else 0,
            'precio_promocion': float(self.precio_promocion) if self.precio_promocion else 0,
            'precio_cliente_mayorista': float(self.precio_cliente_mayorista) if self.precio_cliente_mayorista else 0,
            'available': self.available,
        }