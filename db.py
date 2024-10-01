from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from User import Customer, LoginInformation, Pizza, Ingredients, PizzaIngredients, MenuItems, OrderInfo
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
        total_cost = 0
        # Fetch ingredients associated with the pizza
        ingredients = session.query(Ingredients).join(PizzaIngredients).filter(PizzaIngredients.PizzaID == pizza.PizzaID).all()

        for ingredient in ingredients:
            total_cost = total_cost + ingredient.Price

        final_price = total_cost * 1.4 * 1.09

        pizza.Price = final_price
        pizza_info.append((pizza.Name, final_price))

    return pizza_info

def get_all_items(session):
    menu_items = session.query(MenuItems).all()
    menu_info = []

    for menu_item in menu_items:
        menu_info.append((menu_item.Name, menu_item.Price))

    return menu_info

def add_pizza_table(session, pizza_info):
    for pizza in pizza_info:
        try:
            session.add(pizza.Price)
            session.commit()
            print(f"Pizza {pizza_info['name']} added successfully.")
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
            raise



#ORDERS!!!
def add_order(customerid, date, time, price):


    order_info = OrderInfo(CustomerID = customerid, Date =date, Time= time, Price=price)
    session.add(order_info)

    session.commit()
    print(f"Order {order_info} added successfully.")

def close_session():
    session.close()

def main():
    print(get_all_pizzas(session))

if __name__ == "__main__":
    main()