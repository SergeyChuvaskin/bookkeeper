from PySide6.QtWidgets import QApplication
from bookkeeper.view.expenses_widget import ExpensesWidget


def test_add_expense():
    app = QApplication([])
    expenses_widget = ExpensesWidget()

    initial_row_count = expenses_widget.table.rowCount()

    expenses_widget.description_input.setText("Test expense")
    expenses_widget.amount_input.setValue(10)
    expenses_widget.date_input.setDate(app.dateTime().currentDateTime().date())
    expenses_widget.add_expense()

    assert expenses_widget.table.rowCount() == initial_row_count + 1

    added_item = expenses_widget.table.item(initial_row_count, 0)
    assert added_item.text() == "Test expense"

    added_item = expenses_widget.table.item(initial_row_count, 1)
    assert added_item.text() == "10"

    added_item = expenses_widget.table.item(initial_row_count, 2)
    assert added_item.text() == app.dateTime().currentDateTime().toString("dd.MM.yyyy")
