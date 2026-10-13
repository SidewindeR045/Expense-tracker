import sys
import json
import os
from datetime import date
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QDoubleSpinBox, QComboBox, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout,
    QHBoxLayout, QMessageBox,
)

DATA_FILE = "expenses.json"
CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"]


class ExpenseTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expense Tracker")
        self.resize(600, 400)
        self.expenses = self.load()

        self.desc = QLineEdit()
        self.desc.setPlaceholderText("Description")
        self.amount = QDoubleSpinBox()
        self.amount.setMaximum(1_000_000)
        self.amount.setPrefix("₹")
        self.category = QComboBox()
        self.category.addItems(CATEGORIES)
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_expense)

        form = QHBoxLayout()
        form.addWidget(self.desc, 2)
        form.addWidget(self.amount)
        form.addWidget(self.category)
        form.addWidget(add_btn)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Date", "Description", "Category", "Amount"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.total_label = QLabel()
        delete_btn = QPushButton("Delete Selected")
        delete_btn.clicked.connect(self.delete_expense)

        bottom = QHBoxLayout()
        bottom.addWidget(self.total_label)
        bottom.addStretch()
        bottom.addWidget(delete_btn)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(self.table)
        layout.addLayout(bottom)

        self.refresh()

    def load(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE) as f:
                return json.load(f)
        return []

    def save(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.expenses, f, indent=2)

    def add_expense(self):
        desc = self.desc.text().strip()
        amount = self.amount.value()
        if not desc or amount <= 0:
            QMessageBox.warning(self, "Missing info", "Enter a description and an amount.")
            return
        self.expenses.append({
            "date": date.today().isoformat(),
            "desc": desc,
            "category": self.category.currentText(),
            "amount": amount,
        })
        self.save()
        self.desc.clear()
        self.amount.setValue(0)
        self.refresh()

    def delete_expense(self):
        row = self.table.currentRow()
        if row < 0:
            return
        self.expenses.pop(row)
        self.save()
        self.refresh()

    def refresh(self):
        self.table.setRowCount(len(self.expenses))
        for r, e in enumerate(self.expenses):
            self.table.setItem(r, 0, QTableWidgetItem(e["date"]))
            self.table.setItem(r, 1, QTableWidgetItem(e["desc"]))
            self.table.setItem(r, 2, QTableWidgetItem(e["category"]))
            self.table.setItem(r, 3, QTableWidgetItem(f"₹{e['amount']:.2f}"))
        total = sum(e["amount"] for e in self.expenses)
        self.total_label.setText(f"Total spent: ₹{total:.2f}")


app = QApplication(sys.argv)
window = ExpenseTracker()
window.show()
sys.exit(app.exec_())