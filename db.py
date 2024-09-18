from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from User import Customer, LoginInformation, OrderInfo
from sqlalchemy.exc import IntegrityError

# Database connection settings
engine = create_engine('mysql+pymysql://root:anastasia23@localhost/project', echo=True)

# Create a configured "Session" class and instantiate a session
Session = sessionmaker(bind=engine)
session = Session()

def add_user(username, password, gender, address, phone, birthdate):
    """
    Adds a new user to the database with login information and customer details.

    Args:
        username (str): The username for login.
        password (str): The password for login.
        gender (str): The gender of the customer.
        address (str): The customer's address.
        phone (str): The customer's phone number.
        birthdate (date): The customer's birthdate (as a datetime.date object).
    """
    try:
        # Create a new customer
        customer = Customer(Name=username, Gender=gender, Address=address, Phone=phone, Birthdate=birthdate)

        # Create a new login information entry for the customer
        login_info = LoginInformation(Username=username, Password=password, customer=customer)

        # Add both the customer and login information to the session
        session.add(customer)
        session.add(login_info)

        # Commit the session to save the changes to the database
        session.commit()
        print(f"User {username} added successfully.")
    except IntegrityError:
        # Rollback in case of an integrity issue (e.g., username already exists)
        session.rollback()
        print("Error: Username already exists.")
        raise
    except Exception as e:
        # Handle any other errors and rollback the session
        session.rollback()
        print(f"An error occurred: {e}")
        raise

def get_user(username, password):
    """
    Fetches a user from the database based on their username and password.

    Args:
        username (str): The username for login.
        password (str): The password for login.

    Returns:
        LoginInformation or None: The login information object if found, otherwise None.
    """
    try:
        # Query the login information table for the given username and password
        user = session.query(LoginInformation).filter_by(Username=username, Password=password).first()
        return user
    except Exception as e:
        print(f"An error occurred while fetching the user: {e}")
        return None

def user_exists(username):
    """
    Checks if a user with the given username already exists.

    Args:
        username (str): The username to check.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    try:
        # Check if the username exists in the LoginInformation table
        user = session.query(LoginInformation).filter_by(Username=username).first()
        return user is not None
    except Exception as e:
        print(f"An error occurred while checking the user: {e}")
        return False

def get_customer_info(username):
    """
    Retrieves customer information associated with the given username.

    Args:
        username (str): The username for which to fetch customer details.

    Returns:
        Customer or None: The customer object if found, otherwise None.
    """
    try:
        # Query for the customer associated with the given username
        user = session.query(LoginInformation).filter_by(Username=username).first()
        if user:
            return user.customer
        return None
    except Exception as e:
        print(f"An error occurred while fetching customer info: {e}")
        return None

# Close session properly
def close_session():
    session.close()
