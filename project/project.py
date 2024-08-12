from input import get_input
from cs50 import SQL


def main():

    db = SQL("sqlite:///accounts.db")

    get_input(db)
    return


if __name__ == "__main__":
    main()
