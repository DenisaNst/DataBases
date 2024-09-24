from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

# Database setup
username = 'root'
password = 'anastasia23'
host = 'localhost'
port = '3306'
database = 'project'
engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}', echo=True)

metadata = MetaData(bind=engine)
metadata.reflect(bind=engine)

Base = declarative_base(metadata=metadata)

from User import Customer, OrderInfo, Delivery, DeliveryPerson, LoginInformation, MenuItems, MenuItemsOrder, Pizza, PizzaIngredients, PizzaOrder, Ingredients

# Create all tables
Base.metadata.create_all(engine)

# Session setup
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()