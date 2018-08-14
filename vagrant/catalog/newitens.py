from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime
from database import Base, Categoria, Item

engine = create_engine('sqlite:///catalogo.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Categorias e Itens
categoria1 = Categoria(nome="Futebol")

session.add(categoria1)
session.commit()

Item1 = Item(nome="Camisa do seu Time", descricao="A camisa do seu time do coracao",
                     data_inclusao=datetime.now(), categoria=categoria1)

session.add(Item1)
session.commit()

Item2 = Item(nome="Meiao do seu Time", descricao="O meiao do seu time do coracao",
                     data_inclusao=datetime.now(), categoria=categoria1)

session.add(Item2)
session.commit()

Item3 = Item(nome="Bermuda do seu Time", descricao="A bermuda do seu time do coracao",
                     data_inclusao=datetime.now(), categoria=categoria1)

session.add(Item3)
session.commit()

categoria2 = Categoria(nome="Luta")

session.add(categoria2)
session.commit()

Item1 = Item(nome="Quimono", descricao="O Quimono cobra",
                     data_inclusao=datetime.now(), categoria=categoria2)

session.add(Item1)
session.commit()

Item2 = Item(nome="Luvas de box ", descricao="Luvas para treino de box",
                     data_inclusao=datetime.now(), categoria=categoria2)

session.add(Item2)
session.commit()

Item3 = Item(nome="Protetor bucal", descricao="Proteja os seus dentes nos momentos dificeis",
                     data_inclusao=datetime.now(), categoria=categoria2)

session.add(Item3)
session.commit()

print "added menu items!"
