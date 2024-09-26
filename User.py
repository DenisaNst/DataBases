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
    Price = Column(Float)

    customer = relationship("Customer", back_populates="orders")
    menu_items = relationship("MenuItemsOrder", back_populates="order")
    pizza_orders = relationship("PizzaOrder", back_populates="order")
    delivery = relationship("Delivery", uselist=False, back_populates="order")

    def __repr__(self):
        return f"<OrderInfo(OrderNumber={self.OrderNumber}, CustomerID={self.CustomerID}, Date={self.Date}, Time={self.Time}, Price={self.Price})>"

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
    PizzaID = Column(Integer, ForeignKey('Pizza.PizzaID'))

    order = relationship("OrderInfo", back_populates="menu_items")
    menu_item = relationship("MenuItems", back_populates="orders")
    pizza = relationship("Pizza", back_populates="menu_items")

    def __repr__(self):
        return f"<MenuItemsOrder(OrderNumber={self.OrderNumber}, MenuItemsID={self.MenuItemsID}, PizzaID={self.PizzaID})>"

# Pizza model
class Pizza(Base):
    __tablename__ = 'Pizza'
    PizzaID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String)
    DietaryInfo = Column(String)
    Price = Column(Float)

    ingredients = relationship("PizzaIngredients", back_populates="pizza")
    orders = relationship("PizzaOrder", back_populates="pizza")
    menu_items = relationship("MenuItemsOrder", back_populates="pizza")

    def calculate_pizza_price(self, ingredient_costs):
        total_cost = sum(ingredient_costs)
        profit_margin = 0.4
        vat = 0.09

        price_before_vat = total_cost + (total_cost * profit_margin)
        final_price = price_before_vat + (price_before_vat * vat)

        return round(final_price, 2)

    def __repr__(self):
        return f"<Pizza(PizzaID={self.PizzaID}, Name='{self.Name}', Description='{self.Description}', Price={self.Price})>"

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
    Name = Column(String(100))
    PhoneNumber = Column(String(20))
    Address = Column(String(255))

    deliveries = relationship("Delivery", back_populates="delivery_person")

    def __repr__(self):
        return f"<DeliveryPerson(DeliveryID={self.DeliveryID}, Name='{self.Name}', PhoneNumber='{self.PhoneNumber}', Address='{self.Address}')>"

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
class Ingredient(Base):
    __tablename__ = 'Ingredient'
    IngredientID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(Text)
    Price = Column(Float)

    pizza_ingredients = relationship("PizzaIngredients", back_populates="ingredient")

    def __repr__(self):
        return f"<Ingredient(IngredientID={self.IngredientID}, Name='{self.Name}', Price={self.Price})>"

class PizzaIngredients(Base):
    __tablename__ = 'PizzaIngredients'
    PizzaID = Column(Integer, ForeignKey('Pizza.PizzaID'), primary_key=True)
    IngredientID = Column(Integer, ForeignKey('Ingredient.IngredientID'), primary_key=True)  # Changed to singular
    DietaryInfo = Column(String)
    Price = Column(Float)

    pizza = relationship("Pizza", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="pizza_ingredients")

    def __repr__(self):
        return f"<PizzaIngredients(PizzaID={self.PizzaID}, IngredientID={self.IngredientID}, DietaryInfo='{self.DietaryInfo}', Price={self.Price})>"

# Create all tables
Base.metadata.create_all(engine)

# Session setup
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()



