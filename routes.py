import os
from flask import render_template, url_for, redirect, flash, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from app import app, db
from models import Categoria, Producto, MovimientoInventario
from forms import CategoriaForm, ProductoForm, MovimientoForm

@app.route('/')
def index():
    return render_template('index.html')

# --------- RUTAS DE CATEGORÍA ---------
@app.route('/categorias')
def listar_categorias():
    categorias = Categoria.query.all()
    return render_template('categorias_list.html', categorias=categorias)

@app.route('/categoria/nueva', methods=['GET','POST'])
def crear_categoria():
    form = CategoriaForm()
    if form.validate_on_submit():
        nueva = Categoria(nombre=form.nombre.data, descripcion=form.descripcion.data)
        db.session.add(nueva)
        db.session.commit()
        return redirect(url_for('listar_categorias'))
    return render_template('categoria_form.html', form=form, accion='Nueva Categoría')

@app.route('/categoria/editar/<int:id>', methods=['GET','POST'])
def editar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    form = CategoriaForm(obj=categoria)
    if form.validate_on_submit():
        categoria.nombre = form.nombre.data
        categoria.descripcion = form.descripcion.data
        db.session.commit()
        return redirect(url_for('listar_categorias'))
    return render_template('categoria_form.html', form=form, accion='Editar Categoría')

@app.route('/categoria/eliminar/<int:id>')
def eliminar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    return redirect(url_for('listar_categorias'))

# --------- RUTAS DE PRODUCTO ---------
@app.route('/productos')
def listar_productos():
    categoria_id = request.args.get('categoria', type=int)
    busqueda = request.args.get('q', '', type=str)

    # Consulta base
    query = Producto.query

    # Filtro por categoría
    if categoria_id:
        query = query.filter_by(categoria_id=categoria_id)

    # Búsqueda por nombre
    if busqueda:
        query = query.filter(Producto.nombre.ilike(f'%{busqueda}%'))

    productos = query.all()
    categorias = Categoria.query.all()
    return render_template('productos_list.html', productos=productos, categorias=categorias, categoria_id=categoria_id, busqueda=busqueda)

@app.route('/producto/nuevo', methods=['GET','POST'])
def crear_producto():
    form = ProductoForm()
    form.categoria.choices = [(c.id, c.nombre) for c in Categoria.query.all()]
    if form.validate_on_submit():

        nuevo = Producto(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            categoria_id=form.categoria.data,
            precio=form.precio.data,
            cantidad=form.cantidad.data
        )
        db.session.add(nuevo)
        db.session.commit()
        return redirect(url_for('listar_productos'))
    return render_template('producto_form.html', form=form, accion='Nuevo Producto')

@app.route('/producto/editar/<int:id>', methods=['GET','POST'])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    form = ProductoForm(obj=producto)
    form.categoria.choices = [(c.id, c.nombre) for c in Categoria.query.all()]
    if form.validate_on_submit():
        producto.nombre = form.nombre.data
        producto.descripcion = form.descripcion.data
        producto.categoria_id = form.categoria.data
        producto.precio = form.precio.data
        producto.cantidad = form.cantidad.data

        db.session.commit()
        return redirect(url_for('listar_productos'))
    return render_template('producto_form.html', form=form, accion='Editar Producto', producto=producto)

@app.route('/producto/eliminar/<int:id>')
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    # Eliminar el producto de la base de datos      
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for('listar_productos'))

@app.route('/producto/<int:id>')
def detalle_producto(id):
    producto = Producto.query.get_or_404(id)
    return render_template('producto_detail.html', producto=producto)

# --------- RUTAS DE INVENTARIO y GRÁFICAS ---------
@app.route('/inventario')
def lista_inventario():
    productos = Producto.query.all()
    return render_template('inventario_grafica.html', productos=productos)

@app.route('/inventario/data')
def inventario_data():
    productos = Producto.query.all()
    etiquetas = [p.nombre for p in productos]
    valores = [p.cantidad for p in productos]
    return jsonify({'etiquetas': etiquetas, 'valores': valores})

# --------- RUTAS DE MOVIMIENTOS DE INVENTARIO ---------
@app.route('/movimiento/nuevo', methods=['GET','POST'])
def nuevo_movimiento():
    form = MovimientoForm()
    form.producto.choices = [(p.id, p.nombre) for p in Producto.query.all()]
    if form.validate_on_submit():
        mov = MovimientoInventario(
            producto_id=form.producto.data,
            tipo=form.tipo.data,
            cantidad=form.cantidad.data
        )
        producto = Producto.query.get(form.producto.data)
        if form.tipo.data == 'INGRESO':
            producto.cantidad += form.cantidad.data
        else:
            producto.cantidad -= form.cantidad.data if producto.cantidad >= form.cantidad.data else 0
        db.session.add(mov)
        db.session.commit()
        return redirect(url_for('lista_inventario'))
    return render_template('movimiento_form.html', form=form, accion='Registrar Movimiento')

