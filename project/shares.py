import datetime
import yfinance as yf
from prettytable import PrettyTable
from cs50 import SQL


# Options
def options(db, user):
    while True:
        try:
            # Make Table
            table = PrettyTable()
            table.field_names = ['Number', 'Option']
            table.add_rows([['1', 'Buy Stocks'], ['2', 'Review Portfolio'], ['3', 'Sell Stocks'], ['4', 'Logout']])
            print(table)

            # Get Input
            option = input("Option: ").strip()
            print()

            # Numeric Option
            if option.isnumeric():
                option = int(option)

                if option == 1:
                    search_stock(db, user)
                    continue
                elif option == 2:
                    portfolio(db, user)
                    continue
                elif option == 3:
                    sell_stocks(db, user)
                    continue
                elif option == 4:
                    break
                else:
                    print("\n*----- Invalid Option! -----*\n")
                    continue

            # Alphabetical Option
            elif option[0].isalpha():
                option = option.lower()

                if option == "buy" or option == "buy stocks":
                    search_stock(db, user)
                    continue
                elif option == "review" or option == "review portfolio":
                    portfolio(db, user)
                    continue
                elif option == "sell" or option == "sell stocks":
                    sell_stocks(db, user)
                    continue
                elif option == "logout":
                    break
                else:
                    print("\n*----- Invalid Option! -----*\n")
                    continue

            else:
                print("\n*----- Invalid Option! -----*\n")
                continue

        except ValueError:
            pass
    return


# Search Stock
def search_stock(db, user):
    while True:
        # Get Input Name
        name = input("Stock Name: ").strip()

        if name == "":
            print("*----- Invalid Input! -----*")
            continue
        else:
            break

    # Retrieve Stock's Price
    stock = yf.Ticker(name)
    ticker = stock.history(period='1d')

    try:
        price = ticker['Close'].iloc[0]

    except IndexError:
        print("\n\n*----- Error Retrieving Data -----*\n\n")
        return

    print("#", end="")
    for _ in range(100):
        print("-", end="")
    print("#\n\n\n\n")

    table  = PrettyTable()
    table.field_names = ['Stock Name', 'Price']
    table.add_rows([[f"{name}", f"{price:.4f}"]])
    print(table)
    print()

    buy_stock(user, price, name, db)


def buy_stock(user, price, name, db):
    while True:
        # Get Input Name
        answer = input("Buy Stocks (y/n)? ").strip().lower()

        if answer == "y" or answer == "yes":
            print()
            break
        elif answer == "n" or answer == "no":
            print()
            return
        else:
            print("*----- Invalid Input! -----*")
            continue

    while True:
        # Get Number
        number = input("How Many Stocks? ").strip()

        if number.isalpha():
            print("*----- Invalid Input! -----*")
            continue
        elif number.isnumeric():
            try:
                number = int(number)
            except ValueError:
                print("*----- Invalid Input! -----*")
                continue
            break

    print()
    db.execute("INSERT INTO accounts (person_id, stock_name, stock_price, shares_bought, time_bought) VALUES (?, ?, ?, ?, ?)", user, name, price, number, datetime.datetime.now())


# Show Portfolio
def portfolio(db, user):
    total_value = 0

    stocks = db.execute("SELECT stock_name, shares_bought, stock_price FROM accounts WHERE person_id = ?", user)
    portfolio = PrettyTable()
    portfolio.field_names = ['Stock Name', 'Quantity', 'Stock Price', 'Value']

    for shares in stocks:
        shares["stock_price"] = f"{shares["stock_price"]:.2f}"

        value = float(shares["stock_price"]) * int(shares["shares_bought"])
        total_value += value

        portfolio.add_row([shares["stock_name"], shares["shares_bought"], f'US$ {shares["stock_price"]}', f"US$ {value:.2f}"])

    print(portfolio)

    assets = PrettyTable()
    assets.field_names = ['Total Value', f"US$ {total_value:.2f}"]
    print(f"{assets}\n\n\n")


# Sell Stocks
def sell_stocks(db, user):
    while True:
        # Get Input Stock
        answer = input("What Stock? ").strip()

        if not answer.isnumeric():
            print()
            break
        else:
            print("*----- Invalid Input! -----*")
            continue

    while True:
        # Get Number
        number = input("How Many Stocks? ").strip()

        if number.isalpha():
            print("*----- Invalid Input! -----*")
            continue
        elif number.isnumeric():
            try:
                number = int(number)
            except ValueError:
                print("*----- Invalid Input! -----*")
                continue
            break

    shares = db.execute("SELECT * FROM accounts WHERE stock_name = ? AND person_id = ? AND shares_bought >= ?", answer, user, number)
    if shares == []:
        print("\n\n*----- Shares Not Found! -----*\n\n")
        return

    table = PrettyTable()
    table.field_names = ['Index', 'Stock Name', 'Stock Price', 'Shares Bought', 'Time']

    index = 1
    for share in shares:
        table.add_row([index, share["stock_name"], f"{share["stock_price"]:.2f}", share["shares_bought"], share["time_bought"]])
        index += 1

    print(f"\n\n{table}\n\n")

    if len(shares) == 1:
        time = shares[0]["time_bought"]
        get_stocks(0, number, answer, user, db, time)

    elif len(shares) > 1:
        while True:
            index = input("What Index Stock To Sell: ")
            try:
                index = int(index)

                if index < 1:
                    continue

            except ValueError:
                continue
            break

        index = index - 1
        time = shares[index]["time_bought"]
        get_stocks(index, number, answer, user, db, time)

    else:
        print("\n\n*----- Invalid Index! -----*\n\n")


# Get Stocks Confirmation
def get_stocks(index, number, answer, user, db, time):
    confirmation = input("Confirm To Sell (y/n): ").strip().lower()

    if confirmation == "y" or confirmation == "yes":
        number_sh = db.execute("SELECT shares_bought FROM accounts WHERE stock_name = ? AND person_id = ? AND shares_bought >= ?", answer, user, number)
        number_sh = number_sh[index]["shares_bought"]
        new_number = number_sh - number
        db.execute("UPDATE accounts SET shares_bought = ? WHERE stock_name = ? AND person_id = ? AND time_bought = ?", new_number, answer, user, time)

        price = db.execute("SELECT stock_price FROM accounts WHERE stock_name = ? AND person_id = ? AND shares_bought = ? and time_bought = ?", answer, user, new_number, time)
        sell = float(price[0]["stock_price"]) * number

        print(f"\n\n*----- Selling Total: US$ {sell:.2f} -----*\n\n")

        print("\n\n*----- Successful Sell! -----*\n\n")

        if new_number == 0:
            db.execute("DELETE FROM accounts WHERE shares_bought = 0;")

    elif confirmation == "n" or confirmation == "no":
        print("\n\n*----- Selling Canceled! -----*\n\n")

