from datetime import date, datetime
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, joinedload
from database import Base, Categoria, Item
import requests

engine = create_engine(
    'sqlite:///catalogo.db',
    connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def buscaTodasCategorias():
    return session.query(Categoria).all()


def buscaCategoria_porId(id):
    return session.query(Categoria).filter_by(id=id).one()


def ultimosItens():
    return session.query(Item, Categoria).join(Categoria).\
        order_by(desc(Item.data_inclusao)).limit(10)


def buscaItens_porCategoria(categoria_id):
    return session.query(Item).filter_by(categoria_id=categoria_id).all()


def contaItens_porCategoria(categoria_id):
    return session.query(Item).filter_by(categoria_id=categoria_id).count()


def bucaItem_porCategoriaId(categoria_id, item_id):
    return session.query(Item).\
        filter_by(categoria_id=categoria_id, id=item_id).one()
