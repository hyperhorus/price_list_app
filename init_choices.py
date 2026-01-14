"""
Initialize choice tables with default values
"""

from app import app
from models import db, ImpresionChoice, ColorsChoice


def init_impresion_choices():
    """Initialize printing method choices"""

    impresion_data = [
        {'nombre': 'Grabado laser', 'orden': 1},
        {'nombre': 'Serigrafia', 'orden': 2},
        {'nombre': 'Tampografia', 'orden': 3},
        {'nombre': 'Sublimacion', 'orden': 4},
        {'nombre': 'Bordado', 'orden': 5},
        {'nombre': 'Transfer', 'orden': 6},
        {'nombre': 'Impresión digital', 'orden': 7},
        {'nombre': 'Offset', 'orden': 8},
        {'nombre': 'Grabado punta diamante', 'orden': 9},
        {'nombre': 'Sandblast', 'orden': 10},
        {'nombre': 'Troquelado', 'orden': 11},
        {'nombre': 'Fundido', 'orden': 12},
    ]

    print("\n📝 Initializing Impresion Choices...")
    print("-" * 60)

    for data in impresion_data:
        existing = ImpresionChoice.query.filter_by(nombre=data['nombre']).first()

        if not existing:
            choice = ImpresionChoice(**data)
            db.session.add(choice)
            print(f"  ✓ Added: {data['nombre']}")
        else:
            print(f"  ⊘ Skipped: {data['nombre']} (already exists)")

    try:
        db.session.commit()
        print("✅ Impresion choices initialized successfully")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error: {e}")


def init_colors_choices():
    """Initialize color choices"""

    colors_data = [
        {'nombre': 'Rojo', 'codigo_hex': '#FF0000', 'orden': 1},
        {'nombre': 'Azul', 'codigo_hex': '#0000FF', 'orden': 2},
        {'nombre': 'Verde', 'codigo_hex': '#00FF00', 'orden': 3},
        {'nombre': 'Amarillo', 'codigo_hex': '#FFFF00', 'orden': 4},
        {'nombre': 'Negro', 'codigo_hex': '#000000', 'orden': 5},
        {'nombre': 'Blanco', 'codigo_hex': '#FFFFFF', 'orden': 6},
        {'nombre': 'Naranja', 'codigo_hex': '#FFA500', 'orden': 7},
        {'nombre': 'Rosa', 'codigo_hex': '#FFC0CB', 'orden': 8},
        {'nombre': 'Morado', 'codigo_hex': '#800080', 'orden': 9},
        {'nombre': 'Gris', 'codigo_hex': '#808080', 'orden': 10},
        {'nombre': 'Café', 'codigo_hex': '#8B4513', 'orden': 11},
        {'nombre': 'Dorado', 'codigo_hex': '#FFD700', 'orden': 12},
        {'nombre': 'Plateado', 'codigo_hex': '#C0C0C0', 'orden': 13},
        {'nombre': 'Turquesa', 'codigo_hex': '#40E0D0', 'orden': 14},
        {'nombre': 'Multicolor', 'codigo_hex': None, 'orden': 15},
        {'nombre': 'Humo', 'codigo_hex': None, 'orden': 16},
    ]

    print("\n🎨 Initializing Color Choices...")
    print("-" * 60)

    for data in colors_data:
        existing = ColorsChoice.query.filter_by(nombre=data['nombre']).first()

        if not existing:
            choice = ColorsChoice(**data)
            db.session.add(choice)
            print(f"  ✓ Added: {data['nombre']}")
        else:
            print(f"  ⊘ Skipped: {data['nombre']} (already exists)")

    try:
        db.session.commit()
        print("✅ Color choices initialized successfully")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error: {e}")


def main():
    """Initialize all choice tables"""

    print("=" * 60)
    print("INITIALIZING CHOICE TABLES")
    print("=" * 60)

    with app.app_context():
        # Create tables if they don't exist
        db.create_all()

        # Initialize choices
        init_impresion_choices()
        init_colors_choices()

        # Show summary
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)

        impresion_count = ImpresionChoice.query.count()
        colors_count = ColorsChoice.query.count()

        print(f"📝 Impresion choices: {impresion_count}")
        print(f"🎨 Color choices: {colors_count}")
        print("=" * 60)
        print("\n✅ Initialization completed!")


if __name__ == '__main__':
    main()