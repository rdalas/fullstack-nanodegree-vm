from datetime import date, datetime
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, joinedload
# Importa o Modelo da base de dados
from database import Base, Categoria, Item

engine = create_engine(
    'sqlite:///catalogo.db',
    connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def catalogoJson():
    return session.query(Categoria).options(joinedload(Categoria.itens)).all()


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


def bucaItem_porId(id):
    return session.query(Item).filter_by(id=id).one()


def novoItem(nome, descricao, categoria_id, user):
    newItem = Item(
        nome=nome,
        descricao=descricao,
        data_inclusao=datetime.now(),
        categoria_id=categoria_id,
        user=user)
    session.add(newItem)
    session.commit()


def alteraItem(id, nome, descricao, categoria_id):
    item = bucaItem_porId(id)
    if item:
        item.nome = nome
        item.descricao = descricao
        item.categoria_id = categoria_id
        session.add(item)
        session.commit()
        item = [item.id, item.categoria_id]
        return item


def apagaItem(id):
    item = bucaItem_porId(id)
    if item:
        categoria_id = item.categoria_id
        session.delete(item)
        session.commit()
