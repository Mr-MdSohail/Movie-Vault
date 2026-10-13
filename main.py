# FIRST UNDERTAND THIS BEFORE GOING TO THE PROGRAM 👇👇👇:

# Command Line Interface : You control a program by typing commands/instructions in a terminal instead of clicking buttons in a graphical interface.

# 1️⃣ Add Expense
# User enters something like:
# Amount: 250
# Category: Food
# Description: Dinner
# Date: 2026-09-20
# Python takes the information and stores it in SQL.

# 2️⃣ View Expenses
# Display all stored expenses.
# Something like:
# ID   Amount   Category       Description       Date
# -----------------------------------------------------
# 1    50       Food           Coffee            2026-09-18
# 2    200      Transport      Bus               2026-09-19
# 3    500      Shopping       Shoes             2026-09-20

# 3️⃣ Search Expenses
# This is where the project starts becoming more interesting.
# You could search by:
# Category
# Date
# Amount
# Description
# For example:
# Search by category:
# Food
# And SQL finds the matching records.

# 4️⃣ update Expense
# Suppose you accidentally entered:
# ₹500
# instead of:
# ₹50
# You can select the expense ID and modify it.
# Enter expense ID: 3
# What do you want to update?
# 1. Amount
# 2. Category
# 3. Description
# 4. Date
# Python takes the new value and SQL updates the database.

# 5️⃣ Delete Expense
# Select an expense ID:
# Enter expense ID: 3
# The record gets removed from the database.

# 6️⃣ View Summary 📊
# This is where SQL becomes really useful.
# Instead of simply displaying rows, your program can ask the database questions like:
# Total spent: ₹4,850
# Food:          ₹1,250
# Transport:     ₹800
# Shopping:      ₹2,000
# Entertainment: ₹800

import sqlite3
from tabulate import tabulate

connection = sqlite3.connect(
    r"expenses_tracker.db" #PLEASE UPLOAD FULL PATH OF DATABASE
)
cursor = connection.cursor()


def view():
    cursor.execute("""SELECT * FROM EXPENSES;""")
    view_records = cursor.fetchall()
    print(
        tabulate(
            view_records,
            headers=["ID", "Amount", "Category", "Description", "Date"],
            tablefmt="fancy_grid",
        )
    )

while True:
    print(
        "\n========== EXPENSE TRACKER ==========\n\n1. Add Expense\n2. View Expenses\n3. Search Expense\n4. Update Expense\n5. Delete Expense\n6. View Summary\n7. Exit\n"
    )
    try:
        user_choice = int(input("Enter your choice:  "))
    except ValueError:
        print("please choose a valid option...")
        continue
    if user_choice == 1:
        print("Lets add your expense...Please enter the following details")
        user_amt = int(input("Amount: "))
        user_category = input("Category: ").upper()
        user_desc = input("Description: ").upper()
        user_date = input("Date: ").upper()
        cursor.execute(
            """INSERT INTO EXPENSES (AMOUNT,CATEGORY,DESC,DATE) VALUES(?,?,?,?);""",
            (
                user_amt,
                user_category,
                user_desc,
                user_date,
            ),
        )
        connection.commit()
        print("Expense successfully added!")

    elif user_choice == 2:
        view()

    elif user_choice == 3:
        print("How do you wanna search your expenses?")
        search = int(
            input(
                "Choose one option\n1. Search by category\n2. Search by amount\n3. Search by description\n4. Search by date\n"
            )
        )

        if search == 1:
            search_cat = input("Enter category: ").upper()
            cursor.execute(
                """SELECT * FROM EXPENSES
                WHERE CATEGORY IN (?);""",
                (search_cat,),
            )
            search_rec1 = cursor.fetchall()
            print(
                tabulate(
                    search_rec1,
                    headers=["S.No", "Amount", "Category", "Description", "Date"],
                    tablefmt="fancy_grid",
                )
            )

        elif search == 2:
            search_amt = int(input("Enter amount: "))
            cursor.execute(
                """SELECT * FROM EXPENSES
                WHERE AMOUNT IN (?);""",
                (search_amt,),
            )
            search_rec2 = cursor.fetchall()
            print(
                tabulate(
                    search_rec2,
                    headers=["S.No", "Amount", "Category", "Description", "Date"],
                    tablefmt="fancy_grid",
                )
            )

        elif search == 3:
            search_desc = input("Enter description: ").upper()
            cursor.execute(
                """SELECT * FROM EXPENSES
                WHERE DESC LIKE ?;""",
                ("%" + search_desc + "%",),
            )
            search_rec3 = cursor.fetchall()
            print(
                tabulate(
                    search_rec3,
                    headers=["S.No", "Amount", "Category", "Description", "Date"],
                    tablefmt="fancy_grid",
                )
            )

        elif search == 4:
            search_date = input("Enter date: ").upper()
            cursor.execute(
                """SELECT * FROM EXPENSES
                WHERE DATE IN (?);""",
                (search_date,),
            )
            search_rec4 = cursor.fetchall()
            print(
                tabulate(
                    search_rec4,
                    headers=["S.No", "Amount", "Category", "Description", "Date"],
                    tablefmt="fancy_grid",
                )
            )

    elif user_choice == 4:
        view()
        print("What do you wanna update?")
        expense_id = int(input("Enter Expense ID to update: "))
        update = int(
            input("Choose one option\n1. Amount\n2. Category\n3. Description\n4. Date\n")
        )
        if update == 1:
            new_amt = int(input("Enter new amount: "))
            cursor.execute(
                """UPDATE EXPENSES
                SET AMOUNT=?
                WHERE ID=?;""",
                (
                    new_amt,
                    expense_id,
                ),
            )
            connection.commit()
            print("Updated successfully!")

        elif update == 2:
            new_category = input("Enter new category: ").upper()
            cursor.execute(
                """UPDATE EXPENSES
                SET CATEGORY=?
                WHERE ID=?;""",
                (new_category, expense_id),
            )
            connection.commit()
            print("Updated successfully!")

        elif update == 3:
            new_desc = input("Enter new description: ").upper()
            cursor.execute(
                """UPDATE EXPENSES
                SET DESC=?
                WHERE ID=?;""",
                (
                    new_desc,
                    expense_id,
                ),
            )
            connection.commit()
            print("Updated successfully!")

        elif update == 4:
            new_date = input("Enter new date: ").upper()
            cursor.execute(
                """UPDATE EXPENSES
                SET DATE=?
                WHERE ID=?;""",
                (
                    new_date,
                    expense_id,
                ),
            )
            connection.commit()
            print("Updated successfully!")


    elif user_choice == 5:
        delete_id = int(input("Enter Expense ID to delete: "))
        cursor.execute(
            """SELECT * FROM EXPENSES
            WHERE ID=?;""",
            (delete_id,),
        )
        delete_row = cursor.fetchone()
        if delete_row != None:
            confirm = input("Are you sure you want to delete this expense? (Y/N): ").upper()
            if confirm == "Y":
                cursor.execute(
                    """DELETE FROM EXPENSES
                    WHERE ID=?;""",
                    (delete_id,),
                )
                connection.commit()
                print("Deleted Successfully!")
            else:
                print("Deletion cancelled.")
        else:
            print("Expense not found.")


    # Spending by category:

    # FOOD       ₹850
    # TRAVEL     ₹100
    # SHOPPING   ₹300
    elif user_choice == 6:
        print("\n========== EXPENSE SUMMARY ==========\n")
        cursor.execute("""SELECT SUM(AMOUNT)
            FROM EXPENSES;""")
        total = cursor.fetchone()
        print("Total money spent: ", total[0])
        cursor.execute("""SELECT COUNT(*) FROM EXPENSES;""")
        count = cursor.fetchone()
        print("\nNumber of expenses: ", count[0])
        print("\nSpending by category:\n")
        cursor.execute("""SELECT CATEGORY,SUM(AMOUNT) FROM EXPENSES
            GROUP BY CATEGORY;""")
        records = cursor.fetchall()
        print(tabulate(records, headers=["Category", "Total"], tablefmt="fancy_grid"))
    elif user_choice == 7:
        connection.close()
        break
