import tkinter as tk
from tkinter import messagebox
from db import (add_user, get_user, get_all_pizzas, session, get_all_items, add_order, add_pizza_order,
                add_menu_item_order, add_order_price)
from User import MenuItems, OrderInfo, Customer, PizzaOrder, Pizza, MenuItemsOrder, OrderPrice
from sqlalchemy import func


class PizzaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pizza Delivery App - Login or Sign Up")
        self.root.geometry("600x500")
        self.create_login_signup_screen()

    def create_login_signup_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Login", command=self.login_user).pack(pady=10)
        tk.Button(self.root, text="Sign Up", command=self.create_signup_screen).pack(pady=10)

    def create_signup_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Sign Up - Please fill in your details:").pack(pady=10)

        tk.Label(self.root, text="Name:").pack(pady=5)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack(pady=5)

        tk.Label(self.root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        tk.Label(self.root, text="Gender:").pack(pady=5)
        self.gender_entry = tk.Entry(self.root)
        self.gender_entry.pack(pady=5)

        tk.Label(self.root, text="Address:").pack(pady=5)
        self.address_entry = tk.Entry(self.root)
        self.address_entry.pack(pady=5)

        tk.Label(self.root, text="Phone:").pack(pady=5)
        self.phone_entry = tk.Entry(self.root)
        self.phone_entry.pack(pady=5)

        tk.Label(self.root, text="Birthdate (YYYY-MM-DD):").pack(pady=5)
        self.birthdate_entry = tk.Entry(self.root)
        self.birthdate_entry.pack(pady=5)

        tk.Button(self.root, text="Sign Up", command=self.signup_user).pack(pady=10)
        tk.Button(self.root, text="Back to Login", command=self.create_login_signup_screen).pack(pady=5)

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        from datetime import datetime

        user = get_user(username, password)
        if user:
            messagebox.showinfo("Login Success", f"Welcome, {username}!")
            self.create_pizza_menu(username)
            self.details_order(username)

            customer=session.query(Customer).filter_by(Name=username).first().Birthdate
            birthmonth=func.month(customer)
            birthday=func.day(customer)
            print (birthmonth)
            if birthmonth == datetime.now().month and birthday == datetime.now().day:
                messagebox.showinfo("Birthday Discount", f"Happy Birthday, {username}!IT'S YOUR BIRTHDAY! YOU GET A FREE PIZZA AND A DRINK FROM US!")

        else:
            messagebox.showerror("Login Failed", "Invalid credentials. Please try again.")

    def signup_user(self):
        name = self.name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        gender = self.gender_entry.get()
        address = self.address_entry.get()
        phone = self.phone_entry.get()
        birthdate = self.birthdate_entry.get()

        if not all([name, username, password, gender, address, phone, birthdate]):
            messagebox.showerror("Sign Up Failed", "All fields are required!")
            return

        try:
            add_user(name, password, gender, address, phone, birthdate)
            messagebox.showinfo("Sign Up Success", "Account created successfully!")
            self.create_login_signup_screen()
        except Exception as e:
            messagebox.showerror("Sign Up Failed", f"An error occurred: {e}")

    def create_pizza_menu(self, username):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Choose Your Pizza:").pack(pady=10)

        # Fetch pizza info with dynamically calculated prices
        pizza_info = get_all_pizzas(session)

        # Display the pizzas with their dynamically calculated prices
        for pizza_name, pizza_price in pizza_info:
            tk.Button(self.root, text=f"{pizza_name} - ${pizza_price:.2f}",
                      command=lambda pizza=pizza_name: add_pizza_order(username, pizza)).pack(pady=5)

        menu_info = get_all_items(session)

        for menu_items_name, menu_items_price in menu_info:
            tk.Button(self.root, text=f"{menu_items_name} - ${menu_items_price:.2f}",
                      command=lambda menu = menu_items_name: add_menu_item_order(username, menu)).pack(pady=5)

        place_order = tk.Button(self.root, text="Place Order", command=lambda: self.place_order(username)).pack(pady=10)

    def details_order(self, username):
        from datetime import datetime
        hour = datetime.now()

        from datetime import date
        today = date.today()

        customerid = session.query(Customer).filter_by(Name=username).first().CustomerID
        time = hour
        date = today

        add_order(customerid, date, time)

    def place_order(self,username):
        for widget in self.root.winfo_children():
            widget.destroy()

        total_price=0
        tk.Label(self.root, text="Order Details:").pack(pady=10)

        customerid = session.query(Customer).filter_by(Name= username).first().CustomerID

        order_number = session.query(OrderInfo).filter_by(CustomerID = customerid).order_by(OrderInfo.OrderNumber.desc()).first().OrderNumber

        pizzas = session.query(Pizza) \
            .join(PizzaOrder, Pizza.PizzaID == PizzaOrder.PizzaID) \
            .filter(PizzaOrder.OrderNumber == order_number).all()

        for pizza in pizzas:
            label = tk.Label(self.root, text=f"Pizza: {pizza.Name}, Dietary Info: {pizza.DietaryInfo}, Price: {pizza.Price:.2f}")
            total_price=self.calculate_pizza_price(order_number, username)
            label.pack()

        menu_items = session.query(MenuItems) \
            .join(MenuItemsOrder, MenuItems.MenuItemsID == MenuItemsOrder.MenuItemsID) \
            .filter(MenuItemsOrder.OrderNumber == order_number).all()

        for menu_item in menu_items:
            label2 = tk.Label(self.root, text=f"Menu_Item: {menu_item.Name}, Price: {menu_item.Price:.2f}")
            total_price= total_price+ self.calculate_menu_item_price(order_number, username)
            label2.pack()

        # total_pizza_count = session.query(func.count(PizzaOrder.PizzaID)) \
        #     .join(OrderInfo) \
        #     .filter(OrderInfo.CustomerID == customerid).scalar()

        labelPrice = tk.Label(self.root, text=f"Total Price: {total_price:.2f}").pack()

        add_order_price(order_number, total_price)

    def calculate_menu_item_price(self, order_number, username):
        from datetime import datetime

        total_price=0

        customer=session.query(Customer).filter_by(Name=username).first().Birthdate
        birthmonth=func.month(customer)
        birthday=func.day(customer)

        if birthmonth == datetime.now().month and birthday == datetime.now().day:
            return 0
        else:
            menu_items = session.query(MenuItems) \
                .join(MenuItemsOrder, MenuItems.MenuItemsID == MenuItemsOrder.MenuItemsID) \
                .filter(MenuItemsOrder.OrderNumber == order_number).all()

            for menu_item in menu_items:
                total_price=total_price+menu_item.Price
            return total_price



    def calculate_pizza_price(self, order_number, username):
        from datetime import datetime

        total_price=0

        customer=session.query(Customer).filter_by(Name=username).first().Birthdate
        birthmonth=func.month(customer)
        birthday=func.day(customer)

        if birthmonth == datetime.now().month and birthday == datetime.now().day:
            return 0
        else:
            pizzas = session.query(Pizza) \
                .join(PizzaOrder, Pizza.PizzaID == PizzaOrder.PizzaID) \
                .filter(PizzaOrder.OrderNumber == order_number).all()

            for pizza in pizzas:
                total_price=total_price+pizza.Price
            return total_price



def main():
        root = tk.Tk()
        app = PizzaApp(root)
        root.mainloop()

if __name__ == "__main__":
    main()