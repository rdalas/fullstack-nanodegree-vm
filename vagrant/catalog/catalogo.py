from flask import Flask, render_template, request, redirect, url_for, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database import Base, Categoria, Item

engine = create_engine('sqlite:///catalogo.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/catalog')
def siteHome():
	categorias_Menu = session.query(Categoria).all()
	ultimosItens = session.query(Item, Categoria).join(Categoria).order_by(desc(Item.data_inclusao)).limit(10)
	return render_template('home.html', categorias_Menu=categorias_Menu, ultimosItens=ultimosItens)


@app.route('/catalog/<int:categoria_id>')
@app.route('/catalog/<int:categoria_id>/items')
def catalogo_itens(categoria_id):
	categorias_Menu = session.query(Categoria).all()
	categoria = session.query(Categoria).filter_by(id=categoria_id).one()
	query = session.query(Item).filter_by(categoria_id=categoria_id)
	itens_Categoria = query.all()
	contador = query.count()
	return render_template('items.html', categorias_Menu=categorias_Menu, categoria=categoria, itens_Categoria=itens_Categoria, contador=contador)


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 8000)
