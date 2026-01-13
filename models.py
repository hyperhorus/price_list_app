from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


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