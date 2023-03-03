from PySide6.QtWidgets import QApplication, QWidget, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout
import sys

class BudgetWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

        self.setGeometry(100, 100, 630, 300)

    def setup_ui(self):
        # Create the table widget and set the column headers
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Преиод', 'Сумма', 'Бюджет'])
        self.table.setColumnWidth(0, 83)
        self.table.setColumnWidth(1, 280)
        self.table.setColumnWidth(2, 290)

        # Create the add and delete buttons
        self.add_button = QPushButton('Добавить')
        self.add_button.clicked.connect(self.add_row)
        self.delete_button = QPushButton('Удалить')
        self.delete_button.clicked.connect(self.delete_row)

        # Create the layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)

        # Create the main layout for the widget
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.table)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def add_row(self):
        # Add a new row to the table
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        self.table.setItem(row_count, 0, QTableWidgetItem(''))
        self.table.setItem(row_count, 1, QTableWidgetItem(''))
        self.table.setItem(row_count, 2, QTableWidgetItem(''))

    def delete_row(self):
        # Delete the currently selected row from the table
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = BudgetWidget()
    widget.show()
    sys.exit(app.exec())




