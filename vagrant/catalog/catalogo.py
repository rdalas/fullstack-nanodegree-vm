from flask import Flask, render_template, request, redirect, url_for, jsonify
app = Flask(__name__)
from datetime import date, datetime
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, joinedload
from database import Base, Categoria, Item

engine = create_engine('sqlite:///catalogo.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/catalog/JSON/')
def catalogoJson():
    categorias = session.query(Categoria).options(joinedload(Categoria.itens)).all()
    return jsonify(catalogo=[dict(c.serialize, itens=[i.serialize for i in c.itens]) for c in categorias])


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


@app.route('/catalog/<int:item_id>/edit/', methods=['GET', 'POST'])
def alteraItem(item_id):
	item = session.query(Item).filter_by(id=item_id).one()
	if request.method == 'POST':
			if request.form['nome']:
				item.nome = request.form['nome']
			if request.form['descricao']:
				item.descricao = request.form['descricao']
			if request.form['categoria_id']:
				item.categoria_id = request.form['categoria_id']
			session.add(item)
			session.commit()
			return redirect(url_for('descricaoItem', categoria_id = item.categoria_id, item_id = item.id))
	else:
		categorias = session.query(Categoria).all()
		return render_template('edititem.html', item=item, categorias=categorias)


@app.route('/catalog/<int:item_id>/delete/', methods=['GET', 'POST'])
def deletaItem(item_id):
	itemToDelete = session.query(Item).filter_by(id=item_id).one()
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		return redirect(url_for('catalogoItens', categoria_id = itemToDelete.categoria_id))
	else:
		return render_template('deleteitem.html', itemToDelete=itemToDelete)


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 8000)
