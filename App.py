import tkinter as tk
from tkinter import messagebox, ttk
from db import (add_user, get_user, get_all_pizzas, session, get_all_items, add_order, add_pizza_order,
                add_menu_item_order, add_order_price, add_time_delivery, add_delivery)
from User import MenuItems, OrderInfo, Customer, PizzaOrder, Pizza, MenuItemsOrder, OrderPrice, Adress, DeliveryPerson, \
    Delivery, DiscountCode


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
        self.gender_entry = ttk.Combobox(self.root, values=["Female", "Male", "Other"])
        self.gender_entry.pack(pady=5)

        tk.Label(self.root, text="Address:").pack(pady=5)
        self.address_entry = ttk.Combobox(self.root, values=["N", "S", "W", "E", "NE", "NW", "SE", "SW"])
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

            customer = session.query(Customer).filter_by(Name=username).first()
            birthdate = customer.Birthdate
            birthmonth = birthdate.month
            birthday = birthdate.day
            print(birthmonth)
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

        tk.Label(self.root, text="Choose Your Pizza:", font = 50).pack(pady=10)

        # Fetch pizza info with dynamically calculated prices
        pizza_info = get_all_pizzas(session)

        # Display the pizzas with their dynamically calculated prices
        for pizza_name,  pizza_dietary_info, pizza_price in pizza_info:
            tk.Button(self.root, text=f"{pizza_name} - {pizza_dietary_info} - ${pizza_price:.2f}",
                      command=lambda pizza=pizza_name: add_pizza_order(username, pizza), font = 40).pack(pady=5)

        menu_info = get_all_items(session)

        for menu_items_name, menu_items_price in menu_info:
            tk.Button(self.root, text=f"{menu_items_name} - ${menu_items_price:.2f}",
                      command=lambda menu = menu_items_name: add_menu_item_order(username, menu), font = 40).pack(pady=5)

        label_discount=tk.Label(self.root, text="Enter Discount Code:", font = 40)
        label_discount.place(relx=1.0, rely=0.0, anchor='ne', x=-50, y=550)
        entry_discount=tk.Entry(self.root, font=40)
        entry_discount.place(relx=1.0, rely=0.0, anchor='ne', x=-50, y=600)

        discount_code = entry_discount.get()


        place_order = tk.Button(self.root, text="Place Order", command=lambda: self.place_order(username, discount_code), font = 40)
        place_order.place(relx=1.0, rely=0.0, anchor='ne', x=-50, y=700)



    def details_order(self, username):
        from datetime import datetime
        hour = datetime.now()

        from datetime import date
        today = date.today()

        customerid = session.query(Customer).filter_by(Name=username).first().CustomerID
        time = hour
        date = today

        add_order(customerid, date, time)

    def place_order(self,username, discount_code):
        for widget in self.root.winfo_children():
            widget.destroy()

        customerid = session.query(Customer).filter_by(Name= username).first().CustomerID

        order_number = session.query(OrderInfo).filter_by(CustomerID = customerid).order_by(OrderInfo.OrderNumber.desc()).first().OrderNumber

        pizzas = session.query(Pizza) \
            .join(PizzaOrder, Pizza.PizzaID == PizzaOrder.PizzaID) \
            .filter(PizzaOrder.OrderNumber == order_number).all()

        total_price=0

        if not pizzas:
            messagebox.showerror("Order Error", "You must select at least one pizza to place an order.")
            self.create_pizza_menu(username)
        else:
            tk.Label(self.root, text="Order Details:").pack(pady=10)

            for pizza in pizzas:
                label = tk.Label(self.root, text=f"Pizza: {pizza.Name}, Dietary Info: {pizza.DietaryInfo}, Price: {pizza.Price:.2f}")
                total_price=self.calculate_pizza_price(order_number, username, discount_code)
                label.pack()

            menu_items = session.query(MenuItems) \
                .join(MenuItemsOrder, MenuItems.MenuItemsID == MenuItemsOrder.MenuItemsID) \
                .filter(MenuItemsOrder.OrderNumber == order_number).all()

            for menu_item in menu_items:
                label2 = tk.Label(self.root, text=f"Menu_Item: {menu_item.Name}, Price: {menu_item.Price:.2f}")
                total_price= total_price+ self.calculate_menu_item_price(order_number, username)
                label2.pack()


            labelPrice = tk.Label(self.root, text=f"Total Price: {total_price:.2f}").pack()

            add_order_price(order_number, total_price)

            tk.Button(self.root, text="Confirm Order", command=lambda: self.confirmation_order(username)).pack(pady=10)

    def confirmation_order(self, username):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Order Confirmed!").pack(pady=10)

        from datetime import datetime, timedelta
        hour = datetime.now()

        customer = session.query(Customer).filter_by(Name=username).first()
        customer_address = customer.Address

        # Get the delivery time from the Adress table where the zone matches the customer's address
        address = session.query(Adress).filter_by(Zone=customer_address).first()
        if address:
            time_zone = address.Time
        else:
            messagebox.showerror("Error", "Delivery zone not found.")
            return

        time_arrival = hour + timedelta(hours=time_zone.hour, minutes=time_zone.minute, seconds=time_zone.second)

        customerid = session.query(Customer).filter_by(Name= username).first().CustomerID
        order_number = session.query(OrderInfo).filter_by(CustomerID = customerid).order_by(OrderInfo.OrderNumber.desc()).first().OrderNumber

        add_time_delivery(order_number, time_arrival)
        tk.Label(self.root, text=f"Estimated time of arrival: {time_arrival.strftime('%H:%M:%S')}").pack(pady=10)

        minutes_preparation=timedelta(minutes=20)
        pizza_ready=hour+minutes_preparation

        tk.Button(self.root, text="Check Status", command=lambda: self.check_status( pizza_ready, time_arrival)).pack(pady=10)
        tk.Button(self.root, text="Cancel Order", command=lambda: self.cancel_order(hour, username)).pack(pady=10)

        self.delivery_system(username, hour,order_number)

    def delivery_system(self, username, hour_confirmation, order_number):
        from datetime import datetime, timedelta

        customer = session.query(Customer).filter_by(Name=username).first()
        customer_address = customer.Address

        # Find an available delivery person for the assigned area
        area_delivery_guy = session.query(DeliveryPerson).filter_by(AssignedArea=customer_address, Availability="Available").first()
        if not area_delivery_guy:
            messagebox.showerror("Error", "No available delivery person for the assigned area.")
            return

        area_delivery_guy_ID = area_delivery_guy.DeliveryID

        recent_orders = (
            session.query(Delivery)
            .join(OrderInfo, Delivery.OrderNumber == OrderInfo.OrderNumber)
            .join(Customer, OrderInfo.CustomerID == Customer.CustomerID)
            .filter(Customer.Address == customer.Address)
            .all()
        )

        if not recent_orders:
            three_minutes_ago = hour_confirmation - timedelta(minutes=3)
        else :
            delivery_time = recent_orders[0].DeliveryTime
            delivery_datetime = datetime.combine(datetime.today(), delivery_time)
            three_minutes_ago = delivery_datetime - timedelta(minutes=3)

        recent_orders = (
            session.query(Delivery)
            .join(OrderInfo, Delivery.OrderNumber == OrderInfo.OrderNumber)
            .join(Customer, OrderInfo.CustomerID == Customer.CustomerID)
            .filter(Customer.Address == customer.Address).filter(Delivery.DeliveryTime >= three_minutes_ago)
            .all()
        )
        print(recent_orders)

    # Calculate the total number of pizzas in the recent orders
        total_pizzas = 0
        for order in recent_orders:
            total_pizzas += session.query(PizzaOrder).filter_by(OrderNumber=order.OrderNumber).count()

        # Add the current order's pizzas to the total
        current_order_pizzas = session.query(PizzaOrder).filter_by(OrderNumber=order_number).count()
        total_pizzas += current_order_pizzas

        # If the total number of pizzas is less than or equal to 3, group the orders
        if total_pizzas <= 3:
            for order in recent_orders:
                add_delivery(order.OrderNumber, area_delivery_guy_ID, 'Undelivered', hour_confirmation)
            add_delivery(order_number, area_delivery_guy_ID, 'Undelivered', hour_confirmation)
        else:
            add_delivery(order_number, area_delivery_guy_ID, 'Undelivered', hour_confirmation)
            area_delivery_guy.Availability = "Unavailable"
        session.commit()

    def cancel_order(self, hour_confirm, username):

        from datetime import datetime, timedelta
        hour_now = datetime.now()

        fiveminutes= timedelta(minutes=5)
        cancel_time=hour_confirm+fiveminutes
        if hour_now < cancel_time:
            for widget in self.root.winfo_children():
                widget.destroy()

            customerid = session.query(Customer).filter_by(Name=username).first().CustomerID

            pizzas = session.query(PizzaOrder) \
                .join(OrderInfo) \
                .filter(OrderInfo.CustomerID == customerid) \
                .order_by(OrderInfo.OrderNumber.desc()) \
                .limit(1) \
                .all()

            for pizza in pizzas:
                session.delete(pizza)

            menu_items = session.query(MenuItemsOrder) \
                .join(OrderInfo) \
                .filter(OrderInfo.CustomerID == customerid).order_by(OrderInfo.OrderNumber.desc()) \
                .limit(1) \
                .all()

            for menu_item in menu_items:
                session.delete(menu_item)

            order_price = session.query(OrderPrice) \
                .join(OrderInfo) \
                .filter(OrderInfo.CustomerID == customerid).order_by(OrderInfo.OrderNumber.desc()) \
                .limit(1) \
                .all()

            for price in order_price:
                session.delete(price)

            order_delivery = session.query(OrderPrice) \
                .join(OrderInfo) \
                .filter(OrderInfo.CustomerID == customerid).order_by(OrderInfo.OrderNumber.desc()) \
                .limit(1) \
                .all()

            for delivery in order_delivery:
                session.delete(delivery)

            session.commit()
        else:
            messagebox.showerror("Error", "You can't cancel an order. It's too late!")
            return

        tk.Label(self.root, text="Order Cancelled!").pack(pady=10)
        tk.Button(self.root, text="Back to Menu", command=lambda: self.create_pizza_menu(username)).pack()

    def check_status(self, pizza_ready, time_arrival):

        for widget in self.root.winfo_children():
            widget.destroy()

        from datetime import datetime
        hour_now = datetime.now()

        self.setting_labels(hour_now, pizza_ready, time_arrival)


        refresh=tk.Button(self.root, text="Refresh 🔃", command=lambda: self.check_status(pizza_ready, time_arrival), font=("Helvetica", 24))
        refresh.place(relx=0.5, rely=0.6, anchor='center')
        logout=tk.Button(self.root, text="Log Out", command=self.create_login_signup_screen, font=("Helvetica", 24))
        logout.place(relx=0.5, rely=0.7, anchor='center')


    def setting_labels(self, hour_now, pizza_ready, time_arrival):

        if hour_now < pizza_ready:
            prepare = tk.Label(self.root, text="In preparation", font=("Helvetica", 24, "bold"))
            prepare.place(relx=0.5, rely=0.3, anchor='center')
            delivery = tk.Label(self.root, text="Being delivered", font=("Helvetica", 15, "bold"))
            delivery.place(relx=0.5, rely=0.4, anchor='center')
            delivered = tk.Label(self.root, text="Delivered! Bon appetite!🍕", font=("Helvetica", 15, "bold"))
            delivered.place(relx=0.5, rely=0.5, anchor='center')
        elif hour_now < time_arrival:
            prepare = tk.Label(self.root, text="In preparation", font=("Helvetica", 15, "bold"), fg='green')
            prepare.place(relx=0.5, rely=0.3, anchor='center')
            delivery = tk.Label(self.root, text="Being delivered", font=("Helvetica", 24, "bold"))
            delivery.place(relx=0.5, rely=0.4, anchor='center')
            delivered = tk.Label(self.root, text="Delivered! Bon appetite!🍕", font=("Helvetica", 15, "bold"))
            delivered.place(relx=0.5, rely=0.5, anchor='center')
        else:
            prepare = tk.Label(self.root, text="In preparation", font=("Helvetica", 15, "bold"), fg='green')
            prepare.place(relx=0.5, rely=0.3, anchor='center')
            delivery = tk.Label(self.root, text="Being delivered", font=("Helvetica", 15, "bold"), fg='green')
            delivery.place(relx=0.5, rely=0.4, anchor='center')
            delivered = tk.Label(self.root, text="Delivered! Bon appetite!🍕", font=("Helvetica", 24, "bold"))
            delivered.place(relx=0.5, rely=0.5, anchor='center')

    def calculate_menu_item_price(self, order_number, username):
        from datetime import datetime

        total_price=0

        customerid = session.query(Customer).filter_by(Name= username).first().CustomerID

        pizza_orders = session.query(PizzaOrder) \
            .join(OrderInfo) \
            .filter(OrderInfo.CustomerID == customerid).all()

        total_pizza_count = len(pizza_orders)

        customer = session.query(Customer).filter_by(Name=username).first()
        birthdate = customer.Birthdate
        birthmonth = birthdate.month
        birthday = birthdate.day

        if birthmonth == datetime.now().month and birthday == datetime.now().day:
            return 0
        elif total_pizza_count > 10:
            menu_items = session.query(MenuItems) \
                .join(MenuItemsOrder, MenuItems.MenuItemsID == MenuItemsOrder.MenuItemsID) \
                .filter(MenuItemsOrder.OrderNumber == order_number).all()

            for menu_item in menu_items:
                total_price=total_price+(menu_item.Price-menu_item.Price*0.10)
            return total_price
        else:
            menu_items = session.query(MenuItems) \
                .join(MenuItemsOrder, MenuItems.MenuItemsID == MenuItemsOrder.MenuItemsID) \
                .filter(MenuItemsOrder.OrderNumber == order_number).all()

            for menu_item in menu_items:
                total_price=total_price+menu_item.Price
            return total_price

    def calculate_pizza_price(self, order_number, username, discount_code):
        from datetime import datetime

        total_price=0

        customerid = session.query(Customer).filter_by(Name= username).first().CustomerID

        pizza_orders = session.query(PizzaOrder) \
            .join(OrderInfo) \
            .filter(OrderInfo.CustomerID == customerid).all()

        total_pizza_count = len(pizza_orders)
        print(total_pizza_count)


        customer = session.query(Customer).filter_by(Name=username).first()
        birthdate = customer.Birthdate
        birthmonth = birthdate.month
        birthday = birthdate.day

        if birthmonth == datetime.now().month and birthday == datetime.now().day:
            return 0
        elif total_pizza_count > 10:
            pizzas = session.query(Pizza) \
                .join(PizzaOrder, Pizza.PizzaID == PizzaOrder.PizzaID) \
                .filter(PizzaOrder.OrderNumber == order_number).all()

            for pizza in pizzas:
                total_price =total_price + (pizza.Price - pizza.Price * 0.10)
            return total_price

        else:
            pizzas = session.query(Pizza) \
                .join(PizzaOrder, Pizza.PizzaID == PizzaOrder.PizzaID) \
                .filter(PizzaOrder.OrderNumber == order_number).all()

            for pizza in pizzas:
                total_price=total_price+pizza.Price

        # if discount_code:
        #     discount_customer = session.query(DiscountCode).filter_by(Code=discount_code).first()
        #     if discount_customer:
        #         total_price = total_price - total_price * discount_customer.Discount
        #     else:
        #         messagebox.showerror("Error", "Discount code is invalid.")


        return total_price

def main():
        root = tk.Tk()
        app = PizzaApp(root)
        root.mainloop()

if __name__ == "__main__":
    main()