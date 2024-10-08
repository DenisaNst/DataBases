from sqlalchemy import Column, Integer, String, Text, Date, Time, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

username = 'root'
password = 'anastasia23'
host = 'localhost'
port = '3306'
database = 'project'
engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}', echo=True)

metadata = MetaData(bind=engine)
metadata.reflect(bind=engine)

Base = declarative_base(metadata=metadata)

class Customer(Base):
    __tablename__ = 'Customers'
    CustomerID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(Text)
    Gender = Column(Text)
    Address = Column(String(255))
    Birthdate = Column(Date)
    Phone = Column(String(255))

    orders = relationship("OrderInfo", back_populates="customer")
    login_information = relationship("LoginInformation", uselist=False, back_populates="customer")

    def __repr__(self):
        return f"<Customer(Name='{self.Name}', Gender='{self.Gender}', Address='{self.Address}', Birthdate='{self.Birthdate}', Phone='{self.Phone}')>"

# OrderInfo model
class OrderInfo(Base):
    __tablename__ = 'OrderInfo'
    OrderNumber = Column(Integer, primary_key=True, autoincrement=True)
    CustomerID = Column(Integer, ForeignKey('Customers.CustomerID', ondelete='CASCADE', onupdate='CASCADE'))
    Date = Column(Date)
    Time = Column(Time)

    customer = relationship("Customer", back_populates="orders")
    menu_items = relationship("MenuItemsOrder", back_populates="order")
    pizza_orders = relationship("PizzaOrder", back_populates="order")
    delivery = relationship("Delivery", uselist=False, back_populates="order")
    order_price = relationship("OrderPrice", uselist=False, back_populates="order")
    order_delivery = relationship("OrderDeliveryTime", back_populates="order")

    def __repr__(self):
        return f"<OrderInfo(OrderNumber={self.OrderNumber}, CustomerID={self.CustomerID}, Date={self.Date}, Time={self.Time})>"

class OrderPrice(Base):
    __tablename__ = 'OrderPrice'
    OrderNumber = Column(Integer, ForeignKey('OrderInfo.OrderNumber', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    Price = Column(Float)

    order = relationship("OrderInfo", back_populates="order_price")
    def __repr__(self):
        return f"<OrderPrice(OrderNumber={self.OrderNumber}, Price={self.Price})>"

# LoginInformation model
class LoginInformation(Base):
    __tablename__ = 'LoginInformation'
    CustomerID = Column(Integer, ForeignKey('Customers.CustomerID'), primary_key=True)
    Username = Column(String(255))
    Password = Column(String(255))

    customer = relationship("Customer", back_populates="login_information")

    def __repr__(self):
        return f"<LoginInformation(CustomerID={self.CustomerID}, Username='{self.Username}', Password='{self.Password}')>"

# MenuItems model
class MenuItems(Base):
    __tablename__ = 'MenuItems'
    MenuItemsID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(Text)
    Price = Column(Float)

    orders = relationship("MenuItemsOrder", back_populates="menu_item")

    def __repr__(self):
        return f"<MenuItems(MenuItemsID={self.MenuItemsID}, Name='{self.Name}', Price={self.Price})>"

# MenuItemsOrder model
class MenuItemsOrder(Base):
    __tablename__ = 'MenuItemsOrder'
    OrderNumber = Column(Integer, ForeignKey('OrderInfo.OrderNumber', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    MenuItemsID = Column(Integer, ForeignKey('MenuItems.MenuItemsID'))

    order = relationship("OrderInfo", back_populates="menu_items")
    menu_item = relationship("MenuItems", back_populates="orders")

    def __repr__(self):
        return f"<MenuItemsOrder(OrderNumber={self.OrderNumber}, MenuItemsID={self.MenuItemsID})>"

# Pizza model
class Pizza(Base):
    __tablename__ = 'Pizza'
    PizzaID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String)
    DietaryInfo = Column(String)
    Price = Column(Float)

    # Use plural for clarity, since it's one pizza to many ingredients
    condimente = relationship("PizzaIngredients", back_populates="pizza")
    orders = relationship("PizzaOrder", back_populates="pizza")

    def __repr__(self):
        return f"<Pizza(PizzaID={self.PizzaID}, Name='{self.Name}', DietaryInfo='{self.DietaryInfo}')>"

# PizzaOrder model
class PizzaOrder(Base):
    __tablename__ = 'PizzaOrder'
    OrderNumber = Column(Integer, ForeignKey('OrderInfo.OrderNumber', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    PizzaID = Column(Integer, ForeignKey('Pizza.PizzaID', ondelete='CASCADE', onupdate='CASCADE'))

    order = relationship("OrderInfo", back_populates="pizza_orders")
    pizza = relationship("Pizza", back_populates="orders")

    def __repr__(self):
        return f"<PizzaOrder(OrderNumber={self.OrderNumber}, PizzaID={self.PizzaID})>"

# DeliveryPerson model
class DeliveryPerson(Base):
    __tablename__ = 'DeliveryPerson'
    DeliveryID = Column(Integer, primary_key=True, autoincrement=True)
    AssignedArea = Column(String(255))
    Availability = Column(Text)

    deliveries = relationship("Delivery", back_populates="delivery_person")

    def __repr__(self):
        return f"<DeliveryPerson(DeliveryID={self.DeliveryID}, AssignedArea='{self.AssignedArea}', Availability={self.Availability}')>"

# Delivery model
class Delivery(Base):
    __tablename__ = 'Delivery'
    OrderNumber = Column(Integer, ForeignKey('OrderInfo.OrderNumber', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    DeliveryID = Column(Integer, ForeignKey('DeliveryPerson.DeliveryID'), primary_key=True)
    Status = Column(Text)
    DeliveryTime = Column(Time)

    order = relationship("OrderInfo", back_populates="delivery")
    delivery_person = relationship("DeliveryPerson", back_populates="deliveries")

    def __repr__(self):
        return f"<Delivery(OrderNumber={self.OrderNumber}, DeliveryID={self.DeliveryID}, Status='{self.Status}', DeliveryTime='{self.DeliveryTime}')>"

# Ingredients model
class Ingredients(Base):
    __tablename__ = 'Ingredients'
    IngredientID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(Text)
    Price = Column(Float)

    pizza_ingredients = relationship("PizzaIngredients", back_populates="spice")

    def __repr__(self):
        return f"<Ingredients(IngredientID={self.IngredientID}, Name='{self.Name}', Price={self.Price})>"

class PizzaIngredients(Base):
    __tablename__ = 'PizzaIngredients'
    PizzaID = Column(Integer, ForeignKey('Pizza.PizzaID'), primary_key=True)
    IngredientID = Column(Integer, ForeignKey('Ingredients.IngredientID'), primary_key=True)
    DietaryInfo = Column(String)
    Price = Column(Float)

    pizza = relationship("Pizza", back_populates="condimente")  # Make sure this matches with Pizza's 'ingredients'
    spice = relationship("Ingredients", back_populates="pizza_ingredients")

    def __repr__(self):
        return f"<PizzaIngredients(PizzaID={self.PizzaID}, IngredientID={self.IngredientID}, DietaryInfo='{self.DietaryInfo}', Price={self.Price})>"

class Adress(Base):
    __tablename__ = 'Adress'
    ID = Column(Integer, primary_key = True)
    Zone = Column(String)
    Time = Column (Time)

    def __repr__(self):
        return f"<Adress(ID = {self.ID}, Zone = {self.Zone}, Time={self.Time})>"

class OrderDeliveryTime(Base):
    __tablename__ = 'OrderDeliveryTime'
    OrderNumber = Column(Integer, ForeignKey('OrderInfo.OrderNumber'), primary_key = True)
    TimeDelivery = Column (Time)

    order = relationship("OrderInfo", back_populates="order_delivery")
    def __repr__(self):
        return f"<OrderDeliveryTime(OrderNumber = {self.OrderNumber}, TimeDelivery={self.TimeDelivery})>"

class DiscountCode(Base):
    __tablename__ = 'DiscountCode'
    CodeID = Column(Integer, primary_key = True, autoincrement = True)
    Code = Column(Text)
    Discount = Column(Float)

    def __repr__(self):
        return f"<DiscountCode(CodeID= {self.CodeID}, Code = {self.Code}, Discount={self.Discount})>"
# Create all tables
Base.metadata.create_all(engine)

# Session setup
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()



