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

# Объединяем Publisher , Book и Stok

pb = session.query(Publisher).\
    join(Book, Book.publisher_id == Publisher.id).\
    join (Stock, Stock.book_id == Book.id)
    # filter(Stock.id ==1 )
#Цикл по 1-й строке
# for s in pb.all():
#     print(s.id, s.name)
# print("\n")
#
# Цикл по 2-м строкам
# for s in pb.all():
#     print(s.id, s.name)
#     for bk in s.book:
#         print("\t",bk.id, bk.title)
# print("\n")
#
# # Цикл по 3-м строкам
#
# for s in pb.all():
#     # print(s.id, s.name)
#     for bk in s.book:
#         # print(s.id, s.name,bk.id, bk.title)
#         for st in bk.stock:
#             print(f'Автор: {s.name} | Книга : {bk.title}   |   Сток-id - {st.id} : количество - {st.count} | ')
# #
# print("\n")

# Работаем с Stock и Shop
# spsh = session.query(Shop). join(Stock, Stock.shop_id == Shop.id)
# for s in spsh.all():
#     print(s.id,s.name)
#     for sh in s.stock:
#         print('\t',sh.id,sh.shop_id)

shsp = session.query(Stock). join(Shop, Stock.shop_id == Shop.id)
for s in shsp.all():
    #print(s.id,s.name)
    for sh in s.shop:
        print(sh.id,sh.shop_id)