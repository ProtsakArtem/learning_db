from datetime import datetime
import random

from sqlalchemy import URL, VARCHAR, TIMESTAMP, BIGINT, INTEGER, create_engine, select, ForeignKey
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column, relationship, sessionmaker, Session
from faker import Faker

faker = Faker()

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
    title: Mapped[str] = mapped_column(VARCHAR(255), primary_key=True, nullable=False)
    author_name: Mapped[str] = mapped_column(VARCHAR(255),ForeignKey("authors.name"), nullable=False)
    year: Mapped[str] = mapped_column(VARCHAR(20), nullable=False)
    awards: Mapped[str] = mapped_column(VARCHAR(1000), nullable=True)
    pages: Mapped[int] = mapped_column(BIGINT, nullable=False)

    author = relationship("Author", back_populates="books")


class Author(Base, TableNameMixin):
    name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, primary_key=True)
    age: Mapped[int] = mapped_column(INTEGER)
    country: Mapped[str] = mapped_column(VARCHAR(100))

    books = relationship("Book", back_populates="author")


class Repo():
    def __init__(self, session: Session):
        self.session: Session = session

    def add_book(self, title: str, author_name: str, year: int, awards: str, pages: int) -> Book:
        stmt = select(Book).from_statement(insert(Book).values(title=title, author_name=author_name, year=year, awards=awards, pages=pages).on_conflict_do_nothing().returning(Book))
        result = self.session.scalars(stmt)
        self.session.commit()
        return result.first()

    def add_author(self, name: str, age: int, country: str) -> Author:
        stmt = select(Author).from_statement(
            insert(Author).values(name=name, age=age, country=country).returning(
                Author))
        result = self.session.scalars(stmt)
        self.session.commit()
        return result.first()

    def get_all_author_books(self, author_name: str):
        stmt = select(Book).filter(Book.author_name == author_name)
        result = self.session.execute(stmt)
        return result.scalars().all()

def set_fake_data(repo: Repo):
    authors = []
    books = []
    for x in range(10):
        author = repo.add_author(
            name = faker.name(),
            age = faker.random_int(min=30, max=100),
            country = faker.country_code()
        )
        authors.append(author)

    for x in range(100):
        book = repo.add_book(
            title = faker.word(),
            author_name = random.choice(authors).name,
            year = random.randint(1, 100),
            awards = faker.word(),
            pages = random.randint(1, 2000)
        )
        books.append(book)




engine = create_engine(url, echo=True)
Base.metadata.create_all(engine)
session_pool = sessionmaker(bind=engine)
with session_pool() as session:
    repo = Repo(session)
    # set_fake_data(repo)
    asd = (repo.get_all_author_books("Amanda Campos"))
    for x in asd:
        print(f"""
        {x.title}
        {x.author_name}
        {x.year}
        {x.awards}
        {x.pages}
        """)