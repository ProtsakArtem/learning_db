import random

from environs import Env
from faker import Faker
from lesson3 import User, Order, Product, OrderProduct, Base
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, URL, text
from sqlalchemy.orm import sessionmaker

class Repo:
    def __init__(self, session: Session):
        self.session: Session = session

    def add_user(
        self,
        telegram_id: int,
        full_name: str,
        language_code: str,
        username: str = None,
        referrer_id: int = None,
    ) -> User:
        insert_stmt = insert(
            User,
        ).values(
            telegram_id=telegram_id,
            full_name=full_name,
            language_code=language_code,
            username=username,
            referrer_id=referrer_id,
        ).on_conflict_do_update(
            index_elements=[User.telegram_id],
            set_=dict(
                username=username,
                full_name=full_name,
            ),
        ).returning(User)
        stmt = select(User).from_statement(insert_stmt)
        result = self.session.scalars(stmt)
        self.session.commit()
        return result.first()

    def get_user_by_id(self, telegram_id: int) -> User:
        stmt = select(User).where(User.telegram_id == telegram_id)
        print(stmt)
        result = self.session.execute(stmt)
        return result.scalars().first()

    def add_order(self, user_id: int) -> Order:
        stmt = select(Order).from_statement(insert(Order).values(user_id=user_id).returning(Order))
        result = self.session.scalars(stmt)
        self.session.commit()
        return result.first()

    def add_product(self, title: str, description: str, price: float) -> Product:
        stmt = select(Product).from_statement(insert(Product).values(title=title, description=description, price=price).returning(Product))
        result = self.session.scalars(stmt)
        self.session.commit()
        return result.first()


    def add_product_to_order(self, order_id: int, product_id: int, quantity: int):
        stmt = insert(OrderProduct).values(order_id=order_id, product_id=product_id, quantity=quantity).on_conflict_do_update(
        index_elements=['order_id', 'product_id'],
        set_=dict(quantity=quantity)
    )
        self.session.execute(stmt)
        self.session.commit()
def seed_fake_data(repo: Repo):
    Faker.seed(0)
    fake = Faker()
    users = []
    orders = []
    products = []
    for x in range(10):
        referrer_id = None if not users else users[-1].telegram_id
        user = repo.add_user(
            telegram_id=fake.pyint(),
            full_name=fake.name(),
            language_code=fake.language_code(),
            username=fake.user_name(),
            referrer_id=referrer_id
        )
        users.append(user)
    for x in range(10):
        order = repo.add_order(
            user_id=random.choice(users).telegram_id
        )
        orders.append(order)
    for x in range(10):
        product = repo.add_product(
            title=fake.word(),
            description=fake.sentence(),
            price=fake.pyint(),
        )
        products.append(product)
    for order in orders:
        for x in range(3):
            repo.add_product_to_order(
                order_id=order.order_id,
                product_id=random.choice(products).product_id,
                quantity=fake.pyint(min_value=1, max_value=100),
            )

if __name__ == '__main__':
    # connection string format: driver+postgresql://user:pass@Host:port/dbname
    env = Env()
    env.read_env(".env")
    url = URL.create(
        drivername="postgresql+psycopg2",  # driver name = postgresql + the library we are using (psycopg2)
        username=env.str("POSTGRES_USER"),
        password=env.str("POSTGRES_PASSWORD"),
        host=env.str("DATABASE_HOST"),
        database=env.str("POSTGRES_DB"),
        port=5432
    ).render_as_string(hide_password=False)

    engine = create_engine(url, echo=True)
    session_pool = sessionmaker(bind=engine)
    with session_pool() as session:
        repo = Repo(session)
        seed_fake_data(repo)
