from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pizza Delivery App")

        # Create widgets
        self.label = QLabel("Welcome to Pizza Delivery App", self)
        self.login_button = QPushButton("Login", self)
        self.signup_button = QPushButton("Sign Up", self)

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.login_button)
        layout.addWidget(self.signup_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Connect buttons to functions
        self.login_button.clicked.connect(self.show_login)
        self.signup_button.clicked.connect(self.show_signup)

    def show_login(self):
        self.label.setText("Login Clicked")
        # Implement login functionality here

    def show_signup(self):
        self.label.setText("Sign Up Clicked")
        # Implement sign-up functionality here

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
