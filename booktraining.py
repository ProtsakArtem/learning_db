from datetime import datetime

from sqlalchemy import URL, VARCHAR, TIMESTAMP, BIGINT, INTEGER, create_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column, relationship, sessionmaker

url = URL.create(
    drivername="postgresql+psycopg2",  # driver name = postgresql + the library we are using (psycopg2)
    username='testuser',
    password='testpassword',
    host='localhost',
    database='testuser',
    port=5432
).render_as_string(hide_password=False)

class Base(DeclarativeBase):
    pass


class TableNameMixin:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + "s"



class Book(Base, TableNameMixin):
    title: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True, nullable=False, )
    author_name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    year: Mapped[str] = mapped_column(VARCHAR(20), nullable=False)
    awards: Mapped[str] = mapped_column(VARCHAR(1000), nullable=True)
    pages: Mapped[int] = mapped_column(BIGINT, nullable=False)

    author = relationship("Author", back_populates="books")


class Author(Base, TableNameMixin):
    name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, primary_key=True)
    age: Mapped[int] = mapped_column(INTEGER)
    country: Mapped[str] = mapped_column(VARCHAR(100))

    books = relationship("Book", back_populates="author")


def fill_table_random():


engine = create_engine(url, echo=True)
Base.metadata.create_all(engine)
session_pool = sessionmaker(bind=engine)
with session_pool() as session:
