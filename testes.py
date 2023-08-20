import unittest
import tkinter as tk
from main import Expense, ExpenseList, ExpenseObserver, GUI


class TestExpenseList(unittest.TestCase):
    def test_add_expense(self):
        expense_list = ExpenseList()
        expense = Expense("Test Expense", 50)
        expense_list.add_expense(expense)
        self.assertEqual(len(expense_list.expenses), 1)

    def test_register_observer(self):
        expense_list = ExpenseList()
        observer = ExpenseObserver(expense_list, tk.Tk())
        expense_list.register_observer(observer)
        self.assertEqual(len(expense_list.observers), 1)

class TestExpenseObserver(unittest.TestCase):
    def test_update(self):
        expense_list = ExpenseList()
        observer = ExpenseObserver(expense_list, tk.Tk())
        expense_list.register_observer(observer)

        expense = Expense("Test Expense", 50)
        expense_list.add_expense(expense)

        self.assertIn("Test Expense", observer.expenses_display.cget("text"))

class TestGUI(unittest.TestCase):
    def test_add_expense(self):
        root = tk.Tk()
        expense_list = ExpenseList()
        app = GUI(root, expense_list)

        description_entry = app.description_entry
        amount_entry = app.amount_entry
        add_button = app.add_button

        description_entry.insert(0, "Test Expense")
        amount_entry.insert(0, "50")
        add_button.invoke()

        self.assertEqual(len(expense_list.expenses), 1)

if __name__ == "__main__":
    unittest.main()
