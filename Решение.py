# Легенда: система хранит информацию об издателях (авторах), их книгах и фактах продажи.
# Книги могут продаваться в разных магазинах,
# поэтому требуется учитывать не только что за книга была продана,
# но и в каком магазине это было сделано, а также когда.
#
# Интуитивно необходимо выбрать подходящие типы и связи полей.

# Задание 2
# Используя SQLAlchemy, составить запрос выборки магазинов, продающих целевого издателя.
#
# Напишите Python-скрипт, который:
#
# подключается к БД любого типа на ваш выбор, например, к PostgreSQL;
# импортирует необходимые модели данных;
# принимает имя или идентификатор издателя (publisher), например, через input().
# Выводит построчно факты покупки книг этого издателя:
# название книги | название магазина, в котором была куплена эта книга | стоимость покупки | дата покупки
# Пример (было введено имя автора — Пушкин):
#
# Капитанская дочка | Буквоед     | 600 | 09-11-2022
# Руслан и Людмила  | Буквоед     | 500 | 08-11-2022
# Капитанская дочка | Лабиринт    | 580 | 05-11-2022
# Евгений Онегин    | Книжный дом | 490 | 02-11-2022
# Капитанская дочка | Буквоед     | 600 | 26-10-2022




# Импортируем библиотеки
import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import or_
from datetime import datetime
Base = declarative_base()

# Создаём классы :
# 1) Издатели ( авторы ):
class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=120), unique=True)

    def __str__(self):
        return f'Publisher {self.id}:{self.name}'

# 2) Книги :
class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=120), nullable=False)
    publisher_id = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    # Связь с таблицей Publisher
    publisher = relationship( Publisher , backref="book")

    def __str__(self):
        return f'Book {self.id}:({self.title}, {self.publisher_id} ) '


# 3) Магазины :
class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=80), unique=True)

    def __str__(self):
        return f'Shop {self.id}:{self.name}'

# 4) Сток (склад, хранилище ) Stock
class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    book_id = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    shop_id = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    # Связь с таблицей Book
    book = relationship( Book , backref="stock")
    # Связь с таблицей Shop
    shop = relationship(Shop, backref="stock")
    # shop = relationship("Shop", back_populates="stock")

    def __str__(self):
        return f'Stock {self.id}:({self.count}, {self.book_id}, {self.shop_id}) '




# 5) Продажи :

class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    stock_id = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    price = sq.Column(sq.Integer, nullable=False)
    date_sale = sq.Column(sq.Date ,nullable=False)
    count = sq.Column(sq.Integer, nullable=False)


    # Связь с таблицей Stock
    stock = relationship( Stock , backref="sale")

    def __str__(self):
        return f'Sale {self.id}:({self.price}, {self.date_sale},{self.count},{self.stock_id} ) '


# Создатель таблиц
def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

# Движок подключения
DSN = "postgresql://postgres:Greon68Taganrog2023@localhost:5432/Book_2"
engine = sqlalchemy.create_engine(DSN)

create_tables(engine) # Создали таблицы

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# создание объектов
# 1) Авторы
author1 = Publisher(name='Пушкин')
author2 = Publisher(name='Достоевский')
author3= Publisher(name='Чехов')

session.add_all([author1, author2, author3 ])
session.commit()  # фиксируем изменения

# 2) Книги
book1 = Book (title="Дубровский",publisher_id= 1)
book2 = Book (title="Евгений Онегин",publisher_id= 1)
book3 = Book (title="Пиковая Дама",publisher_id= 1)
book4 = Book (title="Руслан и Людмила",publisher_id= 1)
book5 = Book (title="Идиот",publisher_id= 2)
book6 = Book (title="Преступление и наказание",publisher_id= 2)
book7 = Book (title="Бесы",publisher_id= 2)
book8 = Book (title="Вишневый сад",publisher_id= 3)
book9 = Book (title="Ионыч",publisher_id= 3)
book10 = Book (title="Каштанка",publisher_id= 3)

session.add_all([book1, book2, book3, book4, book5, book6 ,book7, book8, book9 ,book10])
session.commit()  # фиксируем изменения

# 3) Магазины :
shop1 = Shop (name='Буквоед')
shop2 = Shop (name='Алфавит')
shop3 = Shop (name='Книжный дом ')

session.add_all([shop1,shop2,shop3])
session.commit() # фиксируем изменения

# 4) Сток (склад, хранилище ) Stock
stock1 = Stock(book_id=1, shop_id= 1 , count=5 )
stock2 = Stock(book_id=2, shop_id= 1 , count=4 )
stock3 = Stock(book_id=3, shop_id= 1 , count=7 )
stock4 = Stock(book_id=4, shop_id= 1 , count=3 )
stock5 = Stock(book_id=5, shop_id= 1 , count=8 )
stock6 = Stock(book_id=6, shop_id= 1 , count=3 )
stock7 = Stock(book_id=7, shop_id= 1 , count=5 )
stock8 = Stock(book_id=8, shop_id= 1 , count=4 )
stock9 = Stock(book_id=9, shop_id= 1 , count=6 )
stock10 = Stock(book_id=10, shop_id= 1 , count=6 )
stock11 = Stock(book_id=1, shop_id= 2 , count=4 )
stock12 = Stock(book_id=2, shop_id= 2 , count=4 )
stock13 = Stock(book_id=3, shop_id= 2 , count=7 )
stock14 = Stock(book_id=4, shop_id= 2 , count=3 )
stock15 = Stock(book_id=5, shop_id= 2 , count=5 )
stock16 = Stock(book_id=6, shop_id= 2 , count=7 )
stock17 = Stock(book_id=7, shop_id= 2 , count=8 )
stock18 = Stock(book_id=8, shop_id= 2 , count=3 )
stock19 = Stock(book_id=9, shop_id= 2 , count=6 )
stock20 = Stock(book_id=10, shop_id= 2 , count=5 )
stock21 = Stock(book_id=1, shop_id= 3 , count=6 )
stock22 = Stock(book_id=2, shop_id= 3 , count=3 )
stock23 = Stock(book_id=3, shop_id= 3 , count=9 )
stock24 = Stock(book_id=4, shop_id= 3 , count=5 )
stock25 = Stock(book_id=5, shop_id= 3 , count=5 )
stock26 = Stock(book_id=6, shop_id= 3 , count=7 )
stock27 = Stock(book_id=7, shop_id= 3 , count=4 )
stock28 = Stock(book_id=8, shop_id= 3 , count=7 )
stock29 = Stock(book_id=9, shop_id= 3 , count=3 )
stock30 = Stock(book_id=10, shop_id= 3 , count=8 )

session.add_all([stock1,stock2,stock3,stock4,stock5,stock6,stock7,stock8,stock9,stock10])
session.add_all([stock11,stock12,stock13,stock14,stock15,stock16,stock17,stock18,stock19,stock20])
session.add_all([stock21,stock22,stock23,stock24,stock25,stock26,stock27,stock28,stock29,stock30])
session.commit() # фиксируем изменения




# 5) Продажи :
sale1 = Sale (stock_id=1, price=300, date_sale = datetime(2022,10,26), count= 1)
sale2 = Sale (stock_id=13, price=530, date_sale = datetime(2022,10,26), count= 1)
sale3 = Sale (stock_id=6, price=450, date_sale = datetime(2022,10,26), count= 2)
sale4 = Sale (stock_id=29, price=460, date_sale = datetime(2022,11,2), count= 1)
sale5 = Sale (stock_id=19, price=470, date_sale = datetime(2022,11,2), count= 2)
sale6 = Sale (stock_id=2, price=530, date_sale = datetime(2022,11,2), count= 1)
sale7 = Sale (stock_id=21, price=320, date_sale = datetime(2022,11,2), count= 3)
sale8 = Sale (stock_id=25, price=380, date_sale = datetime(2022,11,3), count= 1)
sale9 = Sale (stock_id=1, price=300, date_sale = datetime(2022,11,3), count= 1)
sale10 = Sale (stock_id=8, price=600, date_sale = datetime(2022,11,3), count= 1)
sale11 = Sale (stock_id=16, price=490, date_sale = datetime(2022,11,4), count= 1)
sale12 = Sale (stock_id=14, price=520, date_sale = datetime(2022,11,4), count= 1)
sale13 = Sale (stock_id=26, price=500, date_sale = datetime(2022,11,5), count= 3)
sale14 = Sale (stock_id=9, price=430, date_sale = datetime(2022,11,5), count= 2)
sale15 = Sale (stock_id=24, price=540, date_sale = datetime(2022,11,5), count= 1)
sale16 = Sale (stock_id=30, price=280, date_sale = datetime(2022,11,5), count= 2)

session.add_all([sale1, sale2, sale3, sale4, sale5, sale6, sale7, sale9])
session.add_all([sale9, sale10, sale11, sale12,sale13, sale14, sale15, sale16])
session.add_all([sale1])
session.commit() # фиксируем изменения


# Объединяем таблицы для решения поставленной задачи
qu = session.query(Book, Shop, Sale, Publisher) \
    .join(Book) \
    .join(Stock) \
    .join(Sale) \
    .join(Shop)
    #.filter(Publisher.name == input('Введите название издателя: ')).all()

# # Проверка - Итерируемся по строкам
# for s in qu:
#     print(f' {s.Book.title} | {s.Shop.name}| {s.Sale.price} | {s.Sale.date_sale}' )


# Функция вывода записи через input и or
publisher_name= input("Из списка:\n\n1:Пушкин \n2:Достоевский \n3:Чехов\n\nВведите фамилию автора , "
                      "либо напишите 'None' если хотите получить результат исключительно через id автора : ")
publisher_id = int(input("Введите id автора ,либо цифру '0' если хотите получить результат исключительно через  фамилию автора :  "))
# Функция вывода записи через input и or
def query_func (publisher_name= None, publisher_id= None ) :

    ''' Функция принимает на вход либо имя автора , либо его id из таблицы Publisher.
     На выходе получаем таблицу со столбцами :
     название книги | название магазина, в котором была куплена эта книга | стоимость покупки | дата покупки'''
    print()
    if publisher_id == 0 :
        for s in qu.filter (Publisher.name == publisher_name ).all():
            print(f'{s.Book.title} | {s.Shop.name}| {s.Sale.price} | {s.Sale.date_sale}')

    elif publisher_id != 0:
        for s in qu.filter(or_ (Publisher.name == publisher_name ,Publisher.id == publisher_id )).all():
           print(f' {s.Book.title} | {s.Shop.name}| {s.Sale.price} | {s.Sale.date_sale}' )

# Вызываем функцию
query_func (publisher_name, publisher_id )