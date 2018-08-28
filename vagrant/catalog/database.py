import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Categoria(Base):
    __tablename__ = 'categoria'

    id = Column(Integer, primary_key=True)
    nome = Column(String(250), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'nome': self.nome,
        }


class Item(Base):
    __tablename__ = 'item'

    nome = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)
    descricao = Column(Text)
    data_inclusao = Column(DATETIME)
    categoria_id = Column(Integer, ForeignKey('categoria.id'))
    categoria = relationship(Categoria, backref='itens')
    user = Column(String(250), nullable=False)

    @property
    def serialize(self):
        return {
            'nome': self.nome,
            'id': self.id,
            'descricao': self.descricao,
            'categoria_id': self.categoria_id,
        }


engine = create_engine('sqlite:///catalogo.db')


Base.metadata.create_all(engine)
