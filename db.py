from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from User import Customer, LoginInformation, Pizza, Ingredients, PizzaIngredients, MenuItems, OrderInfo, PizzaOrder, \
    MenuItemsOrder, OrderPrice, OrderDeliveryTime, Delivery
from sqlalchemy.exc import IntegrityError

engine = create_engine('mysql+pymysql://root:anastasia23@localhost/project', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

def add_user(name, password, gender, address, phone, birthdate):

    try:
        customer = Customer(Name=name, Gender=gender, Address=address, Phone=phone, Birthdate=birthdate)

        login_info = LoginInformation(Username=name, Password=password, customer=customer)

        session.add(customer)
        session.add(login_info)

        session.commit()
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
        pizza_info.append((pizza.Name, pizza.DietaryInfo, final_price))

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
def add_order(customerid, date, time):
    order_info = OrderInfo(CustomerID = customerid, Date =date, Time= time)
    session.add(order_info)

    session.commit()
    print(f"Order {order_info} added successfully.")

def add_order_price(order_number, price):
    order_price = OrderPrice(OrderNumber = order_number, Price = price)
    session.add(order_price)

    session.commit()
    print(f"Order Price {order_price} added successfully.")

def add_pizza_order( username, pizza_name):

    customerid = session.query(Customer).filter_by(Name= username).first().CustomerID

    order_number = session.query(OrderInfo).filter_by(CustomerID = customerid).order_by(OrderInfo.OrderNumber.desc()).first().OrderNumber

    pizza_id = session.query(Pizza).filter_by(Name=pizza_name).first().PizzaID

    pizza_order = PizzaOrder(OrderNumber = order_number, PizzaID = pizza_id)
    session.add(pizza_order)

    session.commit()
    print(f"Pizza Order {pizza_order} added successfully.")

def add_menu_item_order(username , menu):
    customerid = session.query(Customer).filter_by(Name=username).first().CustomerID

    order_number = session.query(OrderInfo).filter_by(CustomerID = customerid).order_by(OrderInfo.OrderNumber.desc()).first().OrderNumber

    menu_item_id = session.query(MenuItems).filter_by(Name=menu).first().MenuItemsID

    menu_item_order = MenuItemsOrder(OrderNumber = order_number, MenuItemsID = menu_item_id)
    session.add(menu_item_order)

    session.commit()
    print(f"Menu Item Order {menu_item_order} added successfully.")

def add_time_delivery(order_number, arrival_time):
    order_time = OrderDeliveryTime(OrderNumber = order_number, TimeDelivery = arrival_time)
    session.add(order_time)

    session.commit()
    print(f"Order Time {order_time} added successfully.")

def add_delivery(order_number, area_delivery_guy_ID, status, hour_confirmation):
    delivery = Delivery(OrderNumber = order_number, DeliveryID = area_delivery_guy_ID, Status=status, DeliveryTime = hour_confirmation)
    session.add(delivery)

    session.commit()
    print(f"Delivery {delivery} added successfully.")

def close_session():
    session.close()

def main():
    print(get_all_pizzas(session))

if __name__ == "__main__":
    main()