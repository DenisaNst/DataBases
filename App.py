import tkinter as tk
from tkinter import messagebox
from db import add_user, get_user, get_all_pizzas, session

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
        self.name_entry = tk.Entry(self.root)  # Changed to self.name_entry
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

        user = get_user(username, password)
        if user:
            messagebox.showinfo("Login Success", f"Welcome, {username}!")
            self.create_pizza_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials. Please try again.")

    def signup_user(self):
        name = self.name_entry.get()  # Use the name_entry for Name
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
            add_user(name, username, password, gender, address, phone, birthdate)  # Pass name instead of username
            messagebox.showinfo("Sign Up Success", "Account created successfully!")
            self.create_login_signup_screen()
        except Exception as e:
            messagebox.showerror("Sign Up Failed", f"An error occurred: {e}")

    def create_pizza_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Choose Your Pizza:").pack(pady=10)
        pizza_info = get_all_pizzas(session)

        for pizza_name, pizza_price in pizza_info:
            tk.Button(self.root, text=f"{pizza_name} - ${pizza_price}",
                      command=lambda name=pizza_name: self.choose_pizza(name)).pack(pady=5)

    def choose_pizza(self, pizza_name):
        messagebox.showinfo("Pizza Choice", f"You chose a {pizza_name} pizza!")

def main():
    root = tk.Tk()
    app = PizzaApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
