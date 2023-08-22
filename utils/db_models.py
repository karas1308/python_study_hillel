from sqlalchemy import Column, Integer, ForeignKey, String

from utils.database import Base


class Address(Base):
    __tablename__ = "Address"
    id = Column(Integer, primary_key=True)
    town = Column(String(100), nullable=False)
    street = Column(String(250), nullable=False)
    building = Column(Integer, nullable=False)
    apt = Column(Integer)
    entrance = Column(Integer)
    floor = Column(Integer)
    user = Column(Integer, ForeignKey("User.id"), nullable=False)

    def __init__(self, user=None, town=None, street=None, building=None, apt=None, entrance=None, floor=None):
        self.town = town
        self.street = street
        self.building = building
        self.apt = apt
        self.entrance = entrance
        self.floor = floor
        self.user = user


class Category(Base):
    __tablename__ = "Category"
    id = Column(Integer, primary_key=True)
    name = Column(String(250))

    def __init__(self, name=None):
        self.name = name


class Dishes(Base):
    __tablename__ = "Dishes"
    id = Column(Integer, primary_key=True)
    dish_name = Column(String(250))
    price = Column(Integer)
    description = Column(String(1000))
    available = Column(Integer)
    photo = Column(String(250))
    ccal = Column(Integer)
    protein = Column(Integer)
    fat = Column(Integer)
    carb = Column(Integer)
    category = Column(String, ForeignKey("Category.id"))

    def __init__(self, dish_name=None, price=None, description=None, available=None, photo=None, ccal=None,
                 protein=None, fat=None, carb=None, category=None):
        self.dish_name = dish_name
        self.price = price
        self.description = description
        self.available = available
        self.photo = photo
        self.ccal = ccal
        self.protein = protein
        self.fat = fat
        self.carb = carb
        self.category = category


class OrderedDishes(Base):
    __tablename__ = "Ordered_dishes"
    id = Column(Integer, primary_key=True)
    count = Column(Integer)
    order_id = Column(Integer, ForeignKey("Orders.id"))
    dish_id = Column(String, ForeignKey("Dishes.id"))

    def __init__(self, count=None, order_id=None, dish_id=None):
        self.count = count
        self.order_id = order_id
        self.dish_id = dish_id


class Orders(Base):
    __tablename__ = "Orders"
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey("User.id"))
    address = Column(Integer, ForeignKey("Address.id"))
    total = Column(Integer)
    ccal = Column(Integer)
    protein = Column(Integer)
    carb = Column(Integer)
    fat = Column(Integer)
    comment = Column(String(250))
    order_date = Column(String(20))
    rate = Column(Integer)
    status = Column(Integer)

    def __init__(self, user=None, address=None, total=None, ccal=None, protein=None, carb=None,
                 fat=None, comment=None, order_date=None, rate=None, status=None):
        self.user = user
        self.address = address
        self.total = total
        self.ccal = ccal
        self.protein = protein
        self.carb = carb
        self.fat = fat
        self.comment = comment
        self.order_date = order_date
        self.rate = rate
        self.status = status


class Category(Base):
    __tablename__ = "Statuses"
    id = Column(Integer, primary_key=True, nullable=False)
    status = Column(Integer, nullable=False)

    def __init__(self, status=None):
        self.status = status


class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    phone = Column(Integer, unique=True, nullable=False)
    email = Column(String, unique=True)
    password = Column(String, nullable=False)
    tg = Column(String)
    type = Column(Integer)
    last_name = Column(String)

    def __init__(self, name=None, phone=None, email=None, password=None, tg=None, last_name=None):
        self.name = name
        self.phone = phone
        self.email = email
        self.password = password
        self.tg = tg
        self.type = 1
        self.last_name = last_name
