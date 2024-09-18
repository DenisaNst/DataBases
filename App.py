import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFormLayout
from Project2 import Customer, session

class SignUpForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QFormLayout()

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText('Name')
        layout.addRow('Name:', self.name_input)

        self.gender_input = QLineEdit(self)
        self.gender_input.setPlaceholderText('Gender')
        layout.addRow('Gender:', self.gender_input)

        self.address_input = QLineEdit(self)
        self.address_input.setPlaceholderText('Address')
        layout.addRow('Address:', self.address_input)

        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText('Phone')
        layout.addRow('Phone:', self.phone_input)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText('Email')
        layout.addRow('Email:', self.email_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addRow('Password:', self.password_input)

        signup_button = QPushButton('Sign Up', self)
        signup_button.clicked.connect(self.signup)
        layout.addWidget(signup_button)

        self.result_label = QLabel()
        layout.addWidget(self.result_label)

        self.setLayout(layout)
        self.setWindowTitle('Customer Sign Up')
        self.show()

    def signup(self):
        name = self.name_input.text()
        gender = self.gender_input.text()
        address = self.address_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        if session.query(Customer).filter_by(email=email).first():
            self.result_label.setText("Email already registered. Please log in.")
            return

        new_customer = Customer(Name=name, Gender=gender, Address=address, Phone=phone, Email=email, Password=password)
        try:
            session.add(new_customer)
            session.commit()
            self.result_label.setText("Customer signed up successfully!")
        except IntegrityError:
            session.rollback()
            self.result_label.setText("Error occurred. Please try again.")

class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QFormLayout()

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText('Email')
        layout.addRow('Email:', self.email_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addRow('Password:', self.password_input)

        login_button = QPushButton('Log In', self)
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        self.result_label = QLabel()
        layout.addWidget(self.result_label)

        self.setLayout(layout)
        self.setWindowTitle('Customer Login')
        self.show()

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()
        user = session.query(Customer).filter_by(Email=email, Password=password).first()

        if user:
            self.result_label.setText("Login successful!")
        else:
            self.result_label.setText("Invalid credentials. Please try again.")

class App(QApplication):
    def __init__(self, args):
        super().__init__(args)
        self.login_window = LoginForm()

if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())