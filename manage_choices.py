"""
Command-line tool to manage dropdown choices
"""

from app import app
from models import db, ImpresionChoice, ColorsChoice


def list_impresion_choices():
    """List all printing method choices"""
    print("\n📝 IMPRESION CHOICES")
    print("=" * 70)

    choices = ImpresionChoice.query.order_by(ImpresionChoice.orden, ImpresionChoice.nombre).all()

    if not choices:
        print("  No choices found")
        return

    for choice in choices:
        status = "✓ Active" if choice.activo else "✗ Inactive"
        print(f"  {choice.id}. {choice.nombre:<30} [Orden: {choice.orden}] {status}")


def list_colors_choices():
    """List all color choices"""
    print("\n🎨 COLOR CHOICES")
    print("=" * 70)

    choices = ColorsChoice.query.order_by(ColorsChoice.orden, ColorsChoice.nombre).all()

    if not choices:
        print("  No choices found")
        return

    for choice in choices:
        status = "✓ Active" if choice.activo else "✗ Inactive"
        hex_code = f"({choice.codigo_hex})" if choice.codigo_hex else ""
        print(f"  {choice.id}. {choice.nombre:<20} {hex_code:<10} [Orden: {choice.orden}] {status}")


def add_impresion_choice():
    """Add new printing method choice"""
    print("\n➕ ADD IMPRESION CHOICE")
    print("-" * 70)

    nombre = input("Enter name: ").strip()

    if not nombre:
        print("❌ Name cannot be empty")
        return

    existing = ImpresionChoice.query.filter_by(nombre=nombre).first()
    if existing:
        print(f"❌ '{nombre}' already exists")
        return

    orden = input("Enter order (default: 0): ").strip()
    orden = int(orden) if orden.isdigit() else 0

    choice = ImpresionChoice(nombre=nombre, orden=orden, activo=True)

    try:
        db.session.add(choice)
        db.session.commit()
        print(f"✅ Added '{nombre}'")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error: {e}")


def add_color_choice():
    """Add new color choice"""
    print("\n➕ ADD COLOR CHOICE")
    print("-" * 70)

    nombre = input("Enter name: ").strip()

    if not nombre:
        print("❌ Name cannot be empty")
        return

    existing = ColorsChoice.query.filter_by(nombre=nombre).first()
    if existing:
        print(f"❌ '{nombre}' already exists")
        return

    codigo_hex = input("Enter hex code (optional, e.g., #FF0000): ").strip()
    codigo_hex = codigo_hex if codigo_hex else None

    orden = input("Enter order (default: 0): ").strip()
    orden = int(orden) if orden.isdigit() else 0

    choice = ColorsChoice(nombre=nombre, codigo_hex=codigo_hex, orden=orden, activo=True)

    try:
        db.session.add(choice)
        db.session.commit()
        print(f"✅ Added '{nombre}'")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error: {e}")


def toggle_choice_status(choice_type):
    """Toggle active/inactive status"""
    print(f"\n🔄 TOGGLE {choice_type.upper()} STATUS")
    print("-" * 70)

    choice_id = input("Enter choice ID: ").strip()

    if not choice_id.isdigit():
        print("❌ Invalid ID")
        return

    Model = ImpresionChoice if choice_type == 'impresion' else ColorsChoice
    choice = Model.query.get(int(choice_id))

    if not choice:
        print("❌ Choice not found")
        return

    choice.activo = not choice.activo
    status = "active" if choice.activo else "inactive"

    try:
        db.session.commit()
        print(f"✅ '{choice.nombre}' is now {status}")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error: {e}")


def delete_choice(choice_type):
    """Delete a choice"""
    print(f"\n🗑️  DELETE {choice_type.upper()}")
    print("-" * 70)

    choice_id = input("Enter choice ID: ").strip()

    if not choice_id.isdigit():
        print("❌ Invalid ID")
        return

    Model = ImpresionChoice if choice_type == 'impresion' else ColorsChoice
    choice = Model.query.get(int(choice_id))

    if not choice:
        print("❌ Choice not found")
        return

    confirm = input(f"Delete '{choice.nombre}'? (yes/no): ").strip().lower()

    if confirm == 'yes':
        try:
            db.session.delete(choice)
            db.session.commit()
            print(f"✅ Deleted '{choice.nombre}'")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error: {e}")
    else:
        print("❌ Cancelled")


def main_menu():
    """Main menu"""

    while True:
        print("\n" + "=" * 70)
        print("CHOICE MANAGEMENT SYSTEM")
        print("=" * 70)
        print("\n1. List Impresion Choices")
        print("2. List Color Choices")
        print("3. Add Impresion Choice")
        print("4. Add Color Choice")
        print("5. Toggle Impresion Status")
        print("6. Toggle Color Status")
        print("7. Delete Impresion Choice")
        print("8. Delete Color Choice")
        print("9. Exit")

        choice = input("\nSelect option (1-9): ").strip()

        if choice == '1':
            list_impresion_choices()
        elif choice == '2':
            list_colors_choices()
        elif choice == '3':
            add_impresion_choice()
        elif choice == '4':
            add_color_choice()
        elif choice == '5':
            toggle_choice_status('impresion')
        elif choice == '6':
            toggle_choice_status('color')
        elif choice == '7':
            delete_choice('impresion')
        elif choice == '8':
            delete_choice('color')
        elif choice == '9':
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid option")


if __name__ == '__main__':
    with app.app_context():
        main_menu()