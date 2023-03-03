from PySide6.QtCore import Qt, QDateTime
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QGridLayout, QWidget, QToolBar

class ExpensesWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 630, 300)

        # Create the table widget and populate it
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Дата", "Сумма", "Категория", "Комментарии"])
        self.table_widget.setColumnWidth(0, 150)
        self.table_widget.setColumnWidth(1, 130)
        self.table_widget.setColumnWidth(2, 140)
        self.table_widget.setColumnWidth(3, 210)
        self.populate_table_widget()
        self.setCentralWidget(self.table_widget)

        # Create the Add and Remove buttons
        add_button = QPushButton("Добавить")
        delete_button = QPushButton("Удалить")
        add_button.clicked.connect(self.add_row)
        delete_button.clicked.connect(self.delete_row)

        # Create the grid layout and add the table and buttons to it
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.table_widget, 0, 0, 1, 2)
        grid_layout.addWidget(add_button, 1, 0)
        grid_layout.addWidget(delete_button, 1, 1)

        # Create a central widget to hold the grid layout and set it as the central widget of the main window
        central_widget = QWidget()
        central_widget.setLayout(grid_layout)
        self.setCentralWidget(central_widget)

        # # Create the toolbar and add it to the main window
        # toolbar = QToolBar()
        # toolbar.addWidget(add_button)
        # toolbar.addWidget(delete_button)
        # self.addToolBar(toolbar)

    def populate_table_widget(self):
        # Assume expenses data is in a list of tuples, where each tuple contains the date, description, and amount
        expenses_data = [

        ]
        row_count = len(expenses_data)
        self.table_widget.setRowCount(row_count)
        for i, (date, desc, amount) in enumerate(expenses_data):
            date_item = QTableWidgetItem(date)
            desc_item = QTableWidgetItem(desc)
            amount_item = QTableWidgetItem("{:.2f}".format(amount))
            date_item.setFlags(Qt.ItemIsEditable)
            desc_item.setFlags(Qt.ItemIsEditable)
            amount_item.setFlags(Qt.ItemIsEditable)
            self.table_widget.setItem(i, 0, date_item)
            self.table_widget.setItem(i, 1, desc_item)
            self.table_widget.setItem(i, 2, amount_item)

    def add_row(self):
        row_count = self.table_widget.rowCount()
        self.table_widget.insertRow(row_count)

        # Add the current date and time to the "Date" column of the newly added row
        now = QDateTime.currentDateTime()
        date_item = QTableWidgetItem(now.toString(Qt.ISODate))
        date_item.setFlags(Qt.ItemIsEditable)
        self.table_widget.setItem(row_count, 0, date_item)

    def delete_row(self):
        selected_rows = set(index.row() for index in self.table_widget.selectedIndexes())
        for row in sorted(selected_rows, reverse=True):
            self.table_widget.removeRow(row)

if __name__ == '__main__':
    app = QApplication([])
    expenses_widget = ExpensesWidget()
    expenses_widget.show()
    app.exec_()
