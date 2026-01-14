"""
Quick setup script - Initialize everything
"""

from app import app
from models import db, ImpresionChoice, ColorsChoice


def quick_setup():
    """Quick setup with common choices"""

    print("=" * 70)
    print("QUICK SETUP - CHOICE TABLES")
    print("=" * 70)

    with app.app_context():
        # Create tables
        print("\n📦 Creating database tables...")
        db.create_all()
        print("✅ Tables created")

        # Impresion choices
        impresion_choices = [
            'Grabado laser',
            'Serigrafia',
            'Tampografia',
            'Sublimación',
            'Bordado',
        ]

        print("\n📝 Adding Impresion choices...")
        for i, nombre in enumerate(impresion_choices, 1):
            if not ImpresionChoice.query.filter_by(nombre=nombre).first():
                choice = ImpresionChoice(nombre=nombre, orden=i)
                db.session.add(choice)
                print(f"  ✓ {nombre}")

        # Color choices
        color_choices = [
            ('Rojo', '#FF0000'),
            ('Azul', '#0000FF'),
            ('Verde', '#00FF00'),
            ('Amarillo', '#FFFF00'),
            ('Negro', '#000000'),
            ('Blanco', '#FFFFFF'),
            ('Naranja', '#FFA500'),
            ('Rosa', '#FFC0CB'),
            ('Morado', '#800080'),
            ('Gris', '#808080'),
            ('Multicolor', None),
            ('Humo', None),
        ]

        print("\n🎨 Adding Color choices...")
        for i, (nombre, hex_code) in enumerate(color_choices, 1):
            if not ColorsChoice.query.filter_by(nombre=nombre).first():
                choice = ColorsChoice(nombre=nombre, codigo_hex=hex_code, orden=i)
                db.session.add(choice)
                print(f"  ✓ {nombre}")

        try:
            db.session.commit()
            print("\n✅ Setup completed successfully!")

            # Summary
            print("\n" + "=" * 70)
            print("SUMMARY")
            print("=" * 70)
            print(f"📝 Impresion choices: {ImpresionChoice.query.count()}")
            print(f"🎨 Color choices: {ColorsChoice.query.count()}")
            print("=" * 70)

        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error: {e}")


if __name__ == '__main__':
    quick_setup()