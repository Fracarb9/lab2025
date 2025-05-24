from sqlmodel import create_engine, SQLModel, Session
from typing import Annotated
from fastapi import Depends
from faker import Faker
import os
from app.models.book import Book
from app.models.user import User
from app.models.book_user_link import BookUserLink


sqlite_file_name = "app/data/database.db"  #Percorso del file del DB
sqlite_url = f"sqlite:///{sqlite_file_name}" #Stringa URL di connessione a SQLAlchemy
connect_args = {"check_same_thread": False}  #Disattiva il controllo sul thread di origine
engine = create_engine(sqlite_url, connect_args=connect_args,
                       echo=True)  #Crea l'engine, l'oggetto che SQLAlchemy usa per connettersi al DB, eseguire query e mantenere sessioni
#connect_args: passa parametri specifici per SQLite.
#echo=True: SQLAlchemy stamperà sul terminale tutte le query SQL che esegue — utile per il debugging.



def init_database():
    ds_exists = os.path.isfile(sqlite_file_name)
    SQLModel.metadata.create_all(engine)
    if not ds_exists:
        f = Faker("it_IT")
        with Session(engine) as session:
            for i in range(10):
                user = User(
                    name=f.name(), birth_date=f.date_of_birth(), city=f.city())
                session.add(user)
            session.commit()
            for i in range(10):
                book = Book(title=f.sentence(nb_words=5), author=f.name(),
                            review=f.pyint(1, 5))
                session.add(book)
            session.commit()
            for i in range(5):
                link = BookUserLink(book_id=f.pyint(1, 10),
                                    user_id=f.pyint(1, 10))
                session.add(link)
            session.commit()


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


