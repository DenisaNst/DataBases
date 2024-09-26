from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from User import Customer, LoginInformation, Pizza, Ingredient, PizzaIngredients
from sqlalchemy.exc import IntegrityError

engine = create_engine('mysql+pymysql://root:anastasia23@localhost/project', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

def add_user(name, username, password, gender, address, phone, birthdate):

    try:
        customer = Customer(Name=name, Username =username, Gender=gender, Address=address, Phone=phone, Birthdate=birthdate)

        login_info = LoginInformation(Username=username, Password=password, customer=customer)

        session.add(customer)
        session.add(login_info)

        session.commit()
        print(f"User {username} added successfully.")
    except IntegrityError:
        session.rollback()
        print("Error: Username already exists.")
        raise
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
        raise

def get_user(username, password):
    try:
        # Query the login information table for the given username and password
        user = session.query(LoginInformation).filter_by(Username=username, Password=password).first()
        return user
    except Exception as e:
        print(f"An error occurred while fetching the user: {e}")
        return None

def user_exists(username):
    try:
        user = session.query(LoginInformation).filter_by(Username=username).first()
        return user is not None
    except Exception as e:
        print(f"An error occurred while checking the user: {e}")
        return False

def get_customer_info(username):
    try:
        user = session.query(LoginInformation).filter_by(Username=username).first()
        if user:
            return user.customer
        return None
    except Exception as e:
        print(f"An error occurred while fetching customer info: {e}")
        return None

def get_all_pizzas(session):
    pizzas = session.query(Pizza).all()
    pizza_info = []

    for pizza in pizzas:
        ingredient_costs = []

        for pizza_ingredient in pizza.ingredients:
            ingredient = session.query(Ingredient).filter_by(IngredientID=pizza_ingredient.IngredientID).first()
            if ingredient:
                ingredient_costs.append(ingredient.Price)

        price = pizza.calculate_pizza_price(ingredient_costs)
        pizza_info.append((pizza.Name, price))

    return pizza_info


def close_session():
    session.close()
