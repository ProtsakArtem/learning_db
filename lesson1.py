from sqlalchemy import create_engine, URL, text
from sqlalchemy.orm import sessionmaker

# connection string format: driver+postgresql://user:pass@Host:port/dbname
url = URL.create(
    drivername='postgresql+psycopg2',
    username="testuser",
    password="testpassword",
    host="localhost",
    port="5432",
    database="testuser"
)


engine = create_engine(url, echo=True)
session_pool = sessionmaker(engine)

with session_pool() as session:
    result = session.execute(text("""
    SELECT * FROM users;
    """))
    for row in result:
        print(row)