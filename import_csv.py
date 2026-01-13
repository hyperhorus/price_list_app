"""
CSV Import Script for Flask Price List Application
Imports products from CSV file to MySQL database
"""

import csv
import sys
import os
from decimal import Decimal, InvalidOperation
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import models
from models import db, Product
from app import app


class CSVImporter:
    """Handle CSV import operations"""

    def __init__(self):
        self.imported = 0
        self.skipped = 0
        self.errors = 0
        self.error_details = []

    def clean_decimal(self, value):
        """Convert value to Decimal, handling various formats"""
        if pd.isna(value) or value == '' or value is None:
            return None

        try:
            # Remove currency symbols and commas
            if isinstance(value, str):
                value = value.replace('$', '').replace(',', '').strip()
            return Decimal(str(value))
        except (InvalidOperation, ValueError):
            return None

    def clean_integer(self, value):
        """Convert value to integer"""
        if pd.isna(value) or value == '' or value is None:
            return None

        try:
            return int(float(value))
        except (ValueError, TypeError):
            return None

    def clean_string(self, value):
        """Clean string value"""
        if pd.isna(value) or value is None:
            return None
        return str(value).strip() if str(value).strip() != '' else None

    def clean_boolean(self, value):
        """Convert value to boolean"""
        if pd.isna(value) or value == '' or value is None:
            return True  # Default to available

        if isinstance(value, bool):
            return value

        value_str = str(value).lower().strip()
        return value_str in ['yes', 'sí', 'si', 'true', '1', 'disponible', 'available']

    def import_from_csv(self, csv_file_path, skip_duplicates=True, update_existing=False):
        """
        Import products from CSV file

        Args:
            csv_file_path: Path to CSV file
            skip_duplicates: Skip if clave_producto exists (default: True)
            update_existing: Update existing products (default: False)
        """

        print("=" * 70)
        print("CSV IMPORT TO MYSQL DATABASE")
        print("=" * 70)
        print(f"File: {csv_file_path}")
        print(f"Skip duplicates: {skip_duplicates}")
        print(f"Update existing: {update_existing}")
        print("=" * 70)

        # Check file exists
        if not os.path.exists(csv_file_path):
            print(f"❌ Error: File not found: {csv_file_path}")
            return False

        try:
            # Read CSV with pandas (handles encoding better)
            print("\n📖 Reading CSV file...")

            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
            df = None

            for encoding in encodings:
                try:
                    df = pd.read_csv(csv_file_path, encoding=encoding)
                    print(f"✓ Successfully read with {encoding} encoding")
                    break
                except UnicodeDecodeError:
                    continue

            if df is None:
                print("❌ Could not read CSV file with any encoding")
                return False

            print(f"✓ Found {len(df)} rows")

            # Display column names
            print(f"\n📋 Columns found: {list(df.columns)}")

            # Required columns
            required_columns = ['clave_producto', 'nombre_producto', 'precio_unitario']
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                print(f"❌ Missing required columns: {missing_columns}")
                print(f"   Required: {required_columns}")
                return False

            # Import with Flask app context
            with app.app_context():
                print("\n🔄 Starting import...")
                print("-" * 70)

                for index, row in df.iterrows():
                    row_num = index + 2  # +2 because Excel/CSV rows start at 1 and we have header

                    try:
                        # Get clave_producto
                        clave = self.clean_string(row['clave_producto'])

                        if not clave:
                            self.errors += 1
                            error_msg = f"Row {row_num}: Missing clave_producto"
                            self.error_details.append(error_msg)
                            print(f"⚠️  {error_msg}")
                            continue

                        # Check if product exists
                        existing_product = Product.query.filter_by(clave_producto=clave).first()

                        if existing_product:
                            if skip_duplicates and not update_existing:
                                self.skipped += 1
                                print(f"⊘  Row {row_num}: Skipped '{clave}' (already exists)")
                                continue
                            elif update_existing:
                                product = existing_product
                                print(f"🔄 Row {row_num}: Updating '{clave}'")
                            else:
                                self.skipped += 1
                                continue
                        else:
                            product = Product()
                            print(f"✓  Row {row_num}: Creating '{clave}'")

                        # Set product data
                        product.clave_producto = clave
                        product.nombre_producto = self.clean_string(row['nombre_producto']) or 'Sin nombre'
                        product.descripcion = self.clean_string(row.get('descripcion'))
                        product.medidas = self.clean_string(row.get('medidas'))
                        product.material = self.clean_string(row.get('material'))
                        product.empaque = self.clean_integer(row.get('empaque'))
                        product.impresion = self.clean_string(row.get('impresion'))
                        product.colores = self.clean_string(row.get('colores'))

                        # Prices (required: precio_unitario)
                        precio_unitario = self.clean_decimal(row['precio_unitario'])
                        if precio_unitario is None:
                            self.errors += 1
                            error_msg = f"Row {row_num}: Invalid precio_unitario for '{clave}'"
                            self.error_details.append(error_msg)
                            print(f"❌ {error_msg}")
                            continue

                        product.precio_unitario = precio_unitario
                        product.precio_mayorista = self.clean_decimal(row.get('precio_mayorista'))
                        product.precio_cliente = self.clean_decimal(row.get('precio_cliente'))
                        product.precio_promocion = self.clean_decimal(row.get('precio_promocion'))
                        product.precio_cliente_mayorista = self.clean_decimal(row.get('precio_cliente_mayorista'))

                        # Availability
                        product.available = self.clean_boolean(row.get('available', True))

                        # Add to session
                        if not existing_product:
                            db.session.add(product)

                        self.imported += 1

                        # Commit every 50 records
                        if self.imported % 50 == 0:
                            db.session.commit()
                            print(f"   💾 Committed {self.imported} products...")

                    except Exception as e:
                        self.errors += 1
                        error_msg = f"Row {row_num}: {str(e)}"
                        self.error_details.append(error_msg)
                        print(f"❌ {error_msg}")
                        db.session.rollback()
                        continue

                # Final commit
                try:
                    db.session.commit()
                    print("\n💾 Final commit completed")
                except Exception as e:
                    print(f"❌ Final commit error: {e}")
                    db.session.rollback()
                    return False

            # Print summary
            self.print_summary()
            return True

        except Exception as e:
            print(f"\n❌ Import failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    def print_summary(self):
        """Print import summary"""
        print("\n" + "=" * 70)
        print("IMPORT SUMMARY")
        print("=" * 70)
        print(f"✓ Successfully imported: {self.imported}")
        print(f"⊘ Skipped (duplicates):  {self.skipped}")
        print(f"❌ Errors:                {self.errors}")
        print(f"📊 Total processed:       {self.imported + self.skipped + self.errors}")
        print("=" * 70)

        if self.error_details:
            print("\n⚠️  ERROR DETAILS:")
            print("-" * 70)
            for error in self.error_details[:10]:  # Show first 10 errors
                print(f"  • {error}")

            if len(self.error_details) > 10:
                print(f"  ... and {len(self.error_details) - 10} more errors")


def main():
    """Main execution function"""

    # Default CSV file
    csv_file = 'products.csv'

    # Check for command line argument
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]

    # Check if file exists
    if not os.path.exists(csv_file):
        print(f"❌ Error: File '{csv_file}' not found")
        print(f"\nUsage: python import_csv.py [csv_file_path]")
        print(f"Example: python import_csv.py products.csv")
        sys.exit(1)

    # Options
    print("\n🔧 Import Options:")
    print("  1. Import new products only (skip duplicates)")
    print("  2. Import and update existing products")
    print("  3. Replace all products (delete and reimport)")

    choice = input("\nSelect option (1-3) [default: 1]: ").strip() or '1'

    skip_duplicates = True
    update_existing = False
    delete_all = False

    if choice == '2':
        skip_duplicates = False
        update_existing = True
    elif choice == '3':
        confirm = input("⚠️  This will DELETE all existing products. Continue? (yes/no): ")
        if confirm.lower() == 'yes':
            delete_all = True
        else:
            print("❌ Cancelled")
            sys.exit(0)

    # Delete all if requested
    if delete_all:
        with app.app_context():
            print("\n🗑️  Deleting all existing products...")
            try:
                deleted = Product.query.delete()
                db.session.commit()
                print(f"✓ Deleted {deleted} products")
            except Exception as e:
                print(f"❌ Error deleting products: {e}")
                db.session.rollback()
                sys.exit(1)

    # Create importer and run
    importer = CSVImporter()
    success = importer.import_from_csv(csv_file, skip_duplicates, update_existing)

    if success:
        print("\n✅ Import completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Import failed!")
        sys.exit(1)


if __name__ == '__main__':
    main()