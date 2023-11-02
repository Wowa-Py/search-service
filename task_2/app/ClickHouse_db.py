from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создаем соединение с базой данных ClickHouse
engine = create_engine('clickhouse://localhost:8123/mydb')

# Создаем базовый класс для определения моделей таблиц
Base = declarative_base()

# Определяем модель таблицы users
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    ipv4 = Column(String)
    mac = Column(String)

# Создаем сессию для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Выполняем запрос на выборку всех данных из таблицы users
users = session.query(User).all()

# Выводим результаты запроса в консоль
for user in users:
    print(user.username, user.ipv4, user.mac)
