from flask import Flask, render_template, request, redirect, url_for, jsonify
app = Flask(__name__)
from datetime import date, datetime
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database import Base, Categoria, Item

engine = create_engine('sqlite:///catalogo.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/catalog/')
def siteHome():
	categoriasMenu = session.query(Categoria).all()
	ultimosItens = session.query(Item, Categoria).join(Categoria).order_by(desc(Item.data_inclusao)).limit(10)
	return render_template('home.html', categoriasMenu=categoriasMenu, ultimosItens=ultimosItens)


@app.route('/catalog/<int:categoria_id>/')
@app.route('/catalog/<int:categoria_id>/items/')
def catalogoItens(categoria_id):
	categoriasMenu = session.query(Categoria).all()
	categoria = session.query(Categoria).filter_by(id=categoria_id).one()
	query = session.query(Item).filter_by(categoria_id=categoria_id)
	itensCategoria = query.all()
	contador = query.count()
	return render_template('items.html', categoriasMenu=categoriasMenu, categoria=categoria, itensCategoria=itensCategoria, contador=contador)


@app.route('/catalog/<int:categoria_id>/<int:item_id>/')
def descricaoItem(categoria_id, item_id):
	categoria = session.query(Categoria).filter_by(id=categoria_id).one()
	item = session.query(Item).filter_by(categoria_id=categoria_id, id=item_id).one()
	return render_template('item.html', categoria=categoria, item=item)


@app.route('/catalog/new/', methods=['GET','POST'])
def adicionaItem():
	if request.method == 'POST':
		newItem = Item(nome=request.form['nome'], descricao=request.form['descricao'], data_inclusao=datetime.now(), categoria_id=request.form['categoria_id'])
		session.add(newItem)
		session.commit()
		return redirect(url_for('siteHome'))
	else:
		categorias = session.query(Categoria).all()
		return render_template('newitem.html', categorias=categorias)


@app.route('/catalog/<int:categoria_id>/<int:item_id>/edit/', methods=['GET', 'POST'])
def alteraItem(categoria_id, item_id):
	item = session.query(Item).filter_by(categoria_id=categoria_id, id=item_id).one()
	if request.method == 'POST':
			if request.form['nome']:
				item.nome = request.form['nome']
			if request.form['descricao']:
				item.descricao = request.form['descricao']
			if request.form['categoria_id']:
				item.categoria_id = request.form['categoria_id']
			session.add(Item)
			session.commit()
			return redirect(url_for('descricaoItem', categoria_id = item.categoria_id, item_id = item.id))
	else:
		categorias = session.query(Categoria).all()
		return render_template('edititem.html', categoria_id=categoria_id, item_id=item_id, item=item, categorias=categorias)


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 8000)
