import random
import hashlib
from shares import options
from prettytable import PrettyTable


# Get Inputs
def get_input(db):
    print()

    while True:
        try:
            # Make Table
            table  = PrettyTable()
            table.field_names = ['Number', 'Option']
            table.add_rows([['1', 'Register'], ['2', 'Login'], ['3', 'Delete Account'], ['4', 'Close Program']])
            print(table)

            # Get Input
            option = input("Option: ").strip()
            print()

            # Numeric Option
            if option.isnumeric():
                option = int(option)

                if option == 1:
                    register(db)
                    continue
                elif option == 2:
                    user = login(db)
                    if user:
                        options(db, user)
                    continue
                elif option == 3:
                    deleter(db)
                    continue
                elif option == 4:
                    break
                else:
                    print("\n*----- Invalid Option! -----*\n")
                    continue

            # Alphabetical Option
            elif option[0].isalpha():
                option = option.lower()

                if option == "register":
                    register(db)
                    continue
                elif option == "login":
                    user = login(db)
                    if user:
                        options(db, user)
                    continue
                elif option == "delete" or option == "delete account":
                    deleter(db)
                    continue
                elif option == "close" or option == "close program":
                    break
                else:
                    print("\n*----- Invalid Option! -----*\n")
                    continue

            else:
                print(option.isalpha())
                print("\n*----- Invalid Option! -----*\n")
                continue

        except ValueError:
            pass
    return


# Get Login
def login(db):
    while True:
        # Get Input Name
        name = input("Name: ").lower()

        if name == "":
            continue

        # Hash Code
        name = hash_code(name)

        while True:
            # Get Input Password
            password = input("Password: ")

            if password == "":
                continue
            else:
                break

        break

    # Confirm Name
    if name_confirmation(db, name):
        print("\n*----- User Not Found! -----*\n")
        return

    salt = db.execute("SELECT id_salt FROM people WHERE person_id = ?", name)
    salt = salt[0]["id_salt"]
    password = hash_code(salt + password)

    password_confirmation = db.execute("SELECT id_key FROM people WHERE person_id = ?", name)
    password_id = password_confirmation[0]["id_key"]

    # Confirm Password
    if password == password_id:
        print("\n*----- Succesfull Login! -----*\n")
        return name
    else:
        print("\n*----- Wrong Password! Try Again! -----*\n")
    return


# Register User
def register(db):
    while True:
        # Get Input Name
        name = input("Name (In Lowercase): ").lower()

        if name == "":
            continue

        # Hash Code
        name = hash_code(name)

        while True:
            # Get Input Password
            password = input("Password (Symbols, Lowercase, Uppercase, Numbers): ")

            if password == "":
                continue
            else:
                break

        break

    # Get Salt
    salt = str(random.randint(0, 100000000000000))
    password = salt + password
    password = hash_code(password)

    if name_confirmation(db, name):
        db.execute("INSERT INTO people (person_id, id_key, id_salt) VALUES (?, ?, ?);", name, password, salt)
        print("\n*----- Succesfull Register! -----*\n")
        return

    else:
        print("\n*----- Try Another User Name! -----*\n")
        return


# Delete User
def deleter(db):
    while True:
        # Get Input Name
        name = input("Name: ").lower()

        if name == "":
            continue

        # Hash Code
        name = hash_code(name)

        while True:
            # Get Input Password
            password = input("Password: ")

            if password == "":
                continue
            else:
                break

        break

    # Confirm Name
    if name_confirmation(db, name):
        print("\n*----- User Not Found! -----*\n")
        return

    salt = db.execute("SELECT id_salt FROM people WHERE person_id = ?", name)
    salt = salt[0]["id_salt"]
    password = hash_code(salt + password)

    password_confirmation = db.execute("SELECT id_key FROM people WHERE person_id = ?", name)
    password_id = password_confirmation[0]["id_key"]

    # Confirm Password
    if password == password_id:
        db.execute("DELETE FROM people WHERE id_key = ? AND person_id = ?", password, name)
        db.execute("DELETE FROM accounts WHERE person_id = ?", name)
        print("\n*----- Succesfull Deleting! -----*\n")
    else:
        print("\n*----- Wrong Password! Try Again! -----*\n")
    return


# Name Confirmation
def name_confirmation(db, name):
    # Confirm Name
    name_confirmation = db.execute("SELECT person_id FROM people WHERE person_id = ?", (name,))

    if name_confirmation:
         return False
    else:
        return True


# Hash Code
def hash_code(string):
    # Hash Code
    sha256 = hashlib.sha256()

    sha256.update(string.encode("utf-8"))

    return sha256.hexdigest()
