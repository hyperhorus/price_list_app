from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from models import db, Product, ImpresionChoice, ColorsChoice, Customer, Quotation, QuotationDetail
from forms import ProductForm, CustomerForm
from config import Config
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from flask import render_template, redirect, url_for, flash

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

    # Auto-initialize choices if tables are empty
    if ImpresionChoice.query.count() == 0 or ColorsChoice.query.count() == 0:
        print("\n⚠️  Choice tables are empty. Initializing with default values...")
        print("Run 'python init_choices.py' to customize choices.\n")


# ... rest of your app.py code remains the same ...

@app.context_processor
def inject_counts():
    """Available in ALL templates"""
    return dict(
        product_count=Product.query.count(),
        customer_count=Customer.query.count()
    )


# ==================== ROUTES ====================

@app.route('/')
@app.route('/products')
def index():
    """Display all products"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    available_filter = request.args.get('available', '', type=str)

    query = Product.query

    if search:
        query = query.filter(
            (Product.clave_producto.ilike(f'%{search}%')) |
            (Product.tipo_producto.ilike(f'%{search}%')) |
            (Product.descripcion.ilike(f'%{search}%'))
        )

    if available_filter == 'yes':
        query = query.filter(Product.available == True)
    elif available_filter == 'no':
        query = query.filter(Product.available == False)

    products = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )

    return render_template('index.html', products=products, search=search, available_filter=available_filter)


@app.route('/product/create', methods=['GET', 'POST'])
def create_product():
    """Create new product"""
    form = ProductForm()

    if form.validate_on_submit():
        existing = Product.query.filter_by(clave_producto=form.clave_producto.data).first()
        if existing:
            flash(f'La clave "{form.clave_producto.data}" ya existe.', 'danger')
            return render_template('create_product.html', form=form)

        try:
            product = Product(
                clave_producto=form.clave_producto.data,
                tipo_producto=form.tipo_producto.data,
                descripcion=form.descripcion.data,
                medidas=form.medidas.data,
                material=form.material.data,
                empaque=form.empaque.data,
                impresion=form.impresion.data,
                colores=form.colores.data,
                precio_unitario=form.precio_unitario.data,
                precio_mayorista=form.precio_mayorista.data,
                precio_cliente=form.precio_cliente.data,
                precio_promocion=form.precio_promocion.data,
                precio_cliente_mayorista=form.precio_cliente_mayorista.data,
                available=form.available.data
            )

            db.session.add(product)
            db.session.commit()

            flash(f'Producto "{product.tipo_producto}" creado exitosamente.', 'success')
            return redirect(url_for('view_product', id=product.id))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear producto: {str(e)}', 'danger')

    return render_template('create_product.html', form=form)


@app.route('/product/<int:id>')
def view_product(id):
    """View product details"""
    product = Product.query.get_or_404(id)
    return render_template('view_product.html', product=product)


@app.route('/product/<int:id>/edit', methods=['GET', 'POST'])
def edit_product(id):
    """Edit product"""
    product = Product.query.get_or_404(id)
    form = ProductForm()

    if form.validate_on_submit():
        if form.clave_producto.data != product.clave_producto:
            existing = Product.query.filter_by(clave_producto=form.clave_producto.data).first()
            if existing:
                flash(f'La clave "{form.clave_producto.data}" ya existe.', 'danger')
                return render_template('edit_product.html', form=form, product=product)

        try:
            product.clave_producto = form.clave_producto.data
            product.tipo_producto = form.tipo_producto.data
            product.descripcion = form.descripcion.data
            product.medidas = form.medidas.data
            product.material = form.material.data
            product.empaque = form.empaque.data
            product.impresion = form.impresion.data
            product.colores = form.colores.data
            product.precio_unitario = form.precio_unitario.data
            product.precio_mayorista = form.precio_mayorista.data
            product.precio_cliente = form.precio_cliente.data
            product.precio_promocion = form.precio_promocion.data
            product.precio_cliente_mayorista = form.precio_cliente_mayorista.data
            product.available = form.available.data

            db.session.commit()
            flash(f'Producto actualizado exitosamente.', 'success')
            return redirect(url_for('view_product', id=product.id))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar: {str(e)}', 'danger')

    elif request.method == 'GET':
        form.clave_producto.data = product.clave_producto
        form.tipo_producto.data = product.tipo_producto
        form.descripcion.data = product.descripcion
        form.medidas.data = product.medidas
        form.material.data = product.material
        form.empaque.data = product.empaque
        form.impresion.data = product.impresion
        form.colores.data = product.colores
        form.precio_unitario.data = product.precio_unitario
        form.precio_mayorista.data = product.precio_mayorista
        form.precio_cliente.data = product.precio_cliente
        form.precio_promocion.data = product.precio_promocion
        form.precio_cliente_mayorista.data = product.precio_cliente_mayorista
        form.available.data = product.available

    return render_template('edit_product.html', form=form, product=product)


@app.route('/product/<int:id>/toggle-availability', methods=['POST'])
def toggle_availability(id):
    """Toggle product availability"""
    product = Product.query.get_or_404(id)

    try:
        product.available = not product.available
        db.session.commit()

        status = 'disponible' if product.available else 'no disponible'
        flash(f'Producto marcado como {status}.', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')

    return redirect(url_for('view_product', id=product.id))


@app.route('/product/<int:id>/delete', methods=['POST'])
def delete_product(id):
    """Delete product"""
    product = Product.query.get_or_404(id)

    try:
        db.session.delete(product)
        db.session.commit()
        flash(f'Producto eliminado exitosamente.', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')

    return redirect(url_for('index'))


@app.route('/product/<int:id>/print')
def print_product(id):
    """Generate PDF for single product"""
    product = Product.query.get_or_404(id)

    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Title
    story.append(Paragraph(f'<b>{product.tipo_producto}</b>', styles['Heading1']))
    story.append(Spacer(1, 0.2 * inch))

    # Product details table
    data = [
        ['Campo', 'Valor'],
        ['Clave', product.clave_producto],
        ['Descripción', product.descripcion or 'N/A'],
        ['Medidas', product.medidas or 'N/A'],
        ['Material', product.material or 'N/A'],
        ['Empaque', str(product.empaque) if product.empaque else 'N/A'],
        ['Impresión', product.impresion or 'N/A'],
        ['Colores', product.colores or 'N/A'],
        ['Precio Unitario', f'${product.precio_unitario:.2f}'],
        ['Precio Mayorista', f'${product.precio_mayorista:.2f}' if product.precio_mayorista else 'N/A'],
        ['Precio Cliente', f'${product.precio_cliente:.2f}' if product.precio_cliente else 'N/A'],
        ['Precio Promoción', f'${product.precio_promocion:.2f}' if product.precio_promocion else 'N/A'],
        ['Precio Cliente Mayorista',
         f'${product.precio_cliente_mayorista:.2f}' if product.precio_cliente_mayorista else 'N/A'],
        ['Disponible', 'Sí' if product.available else 'No'],
    ]

    table = Table(data, colWidths=[2.5 * inch, 3.5 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))

    story.append(table)
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph(f'Generado: {datetime.now().strftime("%d/%m/%Y %H:%M")}', styles['Normal']))

    doc.build(story)
    pdf_buffer.seek(0)

    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'Producto_{product.clave_producto}.pdf'
    )


@app.route('/products/print-all')
def print_all_products():
    """Generate PDF of all available products"""
    products = Product.query.filter_by(available=True).order_by(Product.clave_producto).all()

    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()

    story.append(Paragraph('<b>LISTA DE PRECIOS</b>', styles['Heading1']))
    story.append(Paragraph(f'Generado: {datetime.now().strftime("%d/%m/%Y %H:%M")}', styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    # Table data
    data = [['Clave', 'Producto', 'Impresión', 'Unitario', 'Mayorista', 'Cliente', 'Promo']]

    for product in products:
        data.append([
            product.clave_producto,
            product.tipo_producto[:25],
            product.impresion or '',
            f'${product.precio_unitario:.2f}',
            f'${product.precio_mayorista:.2f}' if product.precio_mayorista else '',
            f'${product.precio_cliente:.2f}' if product.precio_cliente else '',
            f'${product.precio_promocion:.2f}' if product.precio_promocion else '',
        ])

    table = Table(data, colWidths=[1 * inch, 2 * inch, 1.2 * inch, 0.9 * inch, 0.9 * inch, 0.9 * inch, 0.8 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))

    story.append(table)
    doc.build(story)
    pdf_buffer.seek(0)

    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'ListaPrecios_{datetime.now().strftime("%Y%m%d")}.pdf'
    )


from sqlalchemy import or_  # Make sure to import or_


@app.route('/customers')
def customers():
    # 1. Get the search term from the URL
    search = request.args.get('search', '', type=str)

    query = Customer.query

    # 2. If a search term exists, filter the query
    if search:
        query = query.filter(
            or_(
                Customer.nombre_empresa.ilike(f'%{search}%'),
                Customer.contacto_nombre.ilike(f'%{search}%'),
                Customer.email.ilike(f'%{search}%'),
                Customer.rfc.ilike(f'%{search}%')
            )
        )

    # 3. Order results
    customers = query.order_by(Customer.nombre_empresa).all()

    # 4. Pass 'customers' AND 'search' back to the template
    return render_template('customers/index.html', customers=customers, search=search)


@app.route('/customer/create', methods=['GET', 'POST'])
def create_customer():
    form = CustomerForm()

    if form.validate_on_submit():
        customer = Customer(
            nombre_empresa=form.nombre_empresa.data,
            contacto_nombre=form.contacto_nombre.data,
            email=form.email.data,
            telefono=form.telefono.data,
            rfc=form.rfc.data,
        )

        db.session.add(customer)
        db.session.commit()

        flash('Cliente creado correctamente', 'success')
        return redirect(url_for('customers'))

    return render_template('customers/create.html', form=form)


@app.route('/customer/<int:customer_id>/edit', methods=['GET', 'POST'])
def edit_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    form = CustomerForm(obj=customer)

    if form.validate_on_submit():
        customer.nombre_empresa = form.nombre_empresa.data
        customer.contacto_nombre = form.contacto_nombre.data
        customer.email = form.email.data
        customer.telefono = form.telefono.data
        customer.rfc = form.rfc.data

        db.session.commit()
        flash('Cliente actualizado', 'success')
        return redirect(url_for('customers'))

    return render_template('customers/edit.html', form=form, customer=customer)


@app.route('/customer/<int:customer_id>')
def view_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return render_template('customers/view.html', customer=customer)


from flask import jsonify, request
import json


# --- QUOTATION ROUTES ---

@app.route('/quotations')
def quotations():
    # Order by newest first
    quotes = Quotation.query.order_by(Quotation.fecha.desc()).all()
    return render_template('quotations/index.html', quotes=quotes)


@app.route('/quotations/create', methods=['GET', 'POST'])
def create_quotation():
    # --- POST: SAVE DATA ---
    if request.method == 'POST':
        try:
            data = request.get_json()

            # 1. Create Header
            new_quote = Quotation(
                customer_id=int(data['customer_id']),
                vigencia_dias=int(data.get('vigencia_dias', 15)),
                status='Borrador',
                notas_generales=data.get('notas_generales'),
                tiempo_entrega_dias=int(data.get('tiempo_entrega_dias', 5)),
                anticipo_requerido_porcentaje=float(data.get('anticipo', 50))
            )
            db.session.add(new_quote)
            db.session.flush()

            # 2. Create Details
            for item in data['items']:
                detail = QuotationDetail(
                    quotation_id=new_quote.quotation_id,
                    clave_producto=item['clave_producto'],
                    cantidad=int(item['cantidad']),
                    precio_pactado=float(item['precio']),
                    tecnica_personalizacion=item.get('tecnica'),
                    costo_personalizacion=float(item.get('costo_personalizacion', 0)),
                    ubicacion_impresion=item.get('ubicacion'),
                    comentarios_diseno=item.get('comentarios')
                )
                db.session.add(detail)

            db.session.commit()
            return jsonify({'success': True, 'redirect': url_for('view_quotation', q_id=new_quote.quotation_id)})

        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    # --- GET: LOAD FORM DATA ---

    # We rename these variables to avoid "shadowing" warnings
    all_customers = Customer.query.order_by(Customer.nombre_empresa).all()
    active_products = Product.query.filter_by(available=True).order_by(Product.tipo_producto).all()

    # Debug print to check in your console if data is actually loading
    print(f"Loaded {len(all_customers)} customers and {len(active_products)} products.")

    return render_template(
        'quotations/create.html',
        customers=all_customers,  # Pass 'all_customers' as 'customers' to the template
        products=active_products  # Pass 'active_products' as 'products' to the template
    )


@app.route('/quotations/<int:q_id>')
def view_quotation(q_id):
    quote = Quotation.query.get_or_404(q_id)
    return render_template('quotations/view.html', quote=quote)


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("Flask Price List Application")
    print("=" * 60)
    print("\n🌐 Open: http://localhost:5000")
    print("🛑 Press CTRL+C to stop\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
