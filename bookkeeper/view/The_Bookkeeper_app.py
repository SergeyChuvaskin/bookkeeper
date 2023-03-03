from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QToolBar,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QSplitter,
    QGroupBox
)
from PySide6.QtCore import Qt, QDateTime
from expenses_widget import ExpensesWidget
from budget_widget import BudgetWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        with open('style.css', 'r') as f:
            self.setStyleSheet(f.read())

        self.setGeometry(50, 50, 683, 500)
        self.setWindowTitle("The Bookkeeper App")

        # Create the splitter and set its orientation
        splitter = QSplitter(Qt.Vertical)

        # Create the expenses widget and add it to a group box
        expenses_group_box = QGroupBox("Последние расходы")
        expenses_widget = ExpensesWidget()
        expenses_layout = QVBoxLayout()
        expenses_layout.addWidget(expenses_widget)
        expenses_group_box.setLayout(expenses_layout)

        # Create the budget widget and add it to a group box
        budget_group_box = QGroupBox("Бюджет")
        budget_widget = BudgetWidget()
        budget_layout = QVBoxLayout()
        budget_layout.addWidget(budget_widget)
        budget_group_box.setLayout(budget_layout)

        # Add the group boxes to the splitter
        splitter.addWidget(expenses_group_box)
        splitter.addWidget(budget_group_box)

        # Set the splitter as the central widget of the main window
        self.setCentralWidget(splitter)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()