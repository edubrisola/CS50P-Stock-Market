# Stock Management System

#### Video Demo: <URL https://youtu.be/PXk4CaC4zWU>

#### Description:
The Stock Management System is a comprehensive application designed to manage stock trading and user accounts. This project is a command-line interface (CLI) tool that allows users to register, log in, manage their stock portfolios, and perform stock transactions.

The application is implemented in Python and utilizes the SQLite database to store user and stock data. The system is structured into multiple Python files, each responsible for different aspects of the application.

**Files Overview:**

1. **input.py**:
   - Contains functions related to user input and account management.
   - **hash_code(string)**: Computes the SHA-256 hash of the input string for secure password storage.
   - **get_input(db)**: Handles the main menu options for user actions including registration, login, account deletion, and program exit.
   - **login(db)**: Manages the login process, including password verification.
   - **register(db)**: Facilitates user registration by storing user credentials securely.
   - **deleter(db)**: Handles user account deletion and associated data removal.

2. **shares.py**:
   - Manages stock-related functionalities.
   - **options(db, user)**: Presents the options available to the logged-in user, such as buying, reviewing, or selling stocks.
   - **search_stock(db, user)**: Allows users to search for stock prices and initiate purchases.
   - **buy_stock(user, price, name, db)**: Handles the purchasing of stocks and updates the user's portfolio.
   - **portfolio(db, user)**: Displays the user's current stock portfolio and its total value.
   - **sell_stocks(db, user)**: Manages the selling of stocks, including stock selection and confirmation.
   - **get_stocks(index, number, answer, user, db, time)**: Confirms and processes stock sales.

3. **project.py**:
   - The entry point for the application.
   - **main()**: Initializes the database connection and invokes the get_input function to start the application.

**Design Choices:**

- **SHA-256 Hashing**: For secure password storage, SHA-256 hashing is used. It ensures that passwords are not stored in plaintext and enhances security against unauthorized access.
- **Command-Line Interface**: A CLI was chosen to keep the application lightweight and focus on core functionalities without the complexity of a graphical user interface.
- **SQLite Database**: SQLite was selected for its simplicity and ease of use in managing user and stock data within a single file.

This project demonstrates fundamental concepts of user authentication, database interactions, and financial transactions within a Python application. It provides a robust foundation for understanding how to manage user data and perform secure operations in a CLI environment.

Feel free to explore the code and test the functionalities to get a hands-on experience with stock management in a simulated trading environment.

