"""
Form widgets for transactions (sales, purchases, expenses)
"""
from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QFormLayout,
    QDoubleSpinBox, QDateTimeEdit, QComboBox, QSpinBox
)
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QFont

from modules.sales import SalesManager
from modules.purchases import PurchaseManager
from modules.expenses import ExpenseManager, PaymentManager
from modules.parties import PartyManager
from modules.inventory import InventoryManager
from database.models import RawMaterial
from database.db import DatabaseManager
from config import EXPENSE_CATEGORIES

class TransactionFormWidget(QWidget):
    """Transaction management widget (Sales, Purchases, Expenses)"""
    
    def __init__(self, transaction_type):
        super().__init__()
        self.transaction_type = transaction_type
        self.sales_manager = SalesManager()
        self.purchase_manager = PurchaseManager()
        self.expense_manager = ExpenseManager()
        self.party_manager = PartyManager()
        self.inventory_manager = InventoryManager()
        
        self.init_ui()
        self.refresh_data()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        # Title
        title_text = {
            'sales': 'Sales Management',
            'purchases': 'Purchase Management',
            'expenses': 'Expense Management'
        }.get(self.transaction_type, 'Transactions')
        
        title = QLabel(title_text)
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # New transaction button
        btn_layout = QHBoxLayout()
        new_btn = QPushButton(f"New {title_text.split()[0]}")
        new_btn.clicked.connect(self.add_transaction)
        btn_layout.addWidget(new_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Transactions table
        if self.transaction_type == 'sales':
            headers = ["Date", "Party", "Quantity", "Rate AFG", "Total AFG", "Actions"]
        elif self.transaction_type == 'purchases':
            headers = ["Date", "Party", "Material", "Quantity", "Total AFG", "Actions"]
        else:  # expenses
            headers = ["Date", "Category", "Amount AFG", "Party", "Actions"]
        
        self.table = QTableWidget()
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def refresh_data(self):
        """Refresh transaction data"""
        try:
            if self.transaction_type == 'sales':
                transactions = self.sales_manager.get_sales()
                self.table.setRowCount(len(transactions))
                
                for row, trans in enumerate(transactions):
                    party = self.party_manager.get_party_by_id(trans.party_id)
                    
                    self.table.setItem(row, 0, QTableWidgetItem(trans.date.strftime("%Y-%m-%d")))
                    self.table.setItem(row, 1, QTableWidgetItem(party.name if party else ""))
                    self.table.setItem(row, 2, QTableWidgetItem(str(trans.quantity)))
                    self.table.setItem(row, 3, QTableWidgetItem(f"{trans.rate_afg:.2f}"))
                    self.table.setItem(row, 4, QTableWidgetItem(f"{trans.total_afg:.2f}"))
                    
                    action_widget = self.create_action_buttons(trans, 'sale')
                    self.table.setCellWidget(row, 5, action_widget)
            
            elif self.transaction_type == 'purchases':
                transactions = self.purchase_manager.get_purchases()
                self.table.setRowCount(len(transactions))
                
                for row, trans in enumerate(transactions):
                    party = self.party_manager.get_party_by_id(trans.party_id)
                    session = DatabaseManager.get_session()
                    material = session.query(RawMaterial).filter(RawMaterial.id == trans.material_id).first()
                    
                    self.table.setItem(row, 0, QTableWidgetItem(trans.date.strftime("%Y-%m-%d")))
                    self.table.setItem(row, 1, QTableWidgetItem(party.name if party else ""))
                    self.table.setItem(row, 2, QTableWidgetItem(material.name if material else ""))
                    self.table.setItem(row, 3, QTableWidgetItem(f"{trans.quantity:.2f}"))
                    self.table.setItem(row, 4, QTableWidgetItem(f"{trans.total_afg:.2f}"))
                    
                    action_widget = self.create_action_buttons(trans, 'purchase')
                    self.table.setCellWidget(row, 5, action_widget)
            
            else:  # expenses
                transactions = self.expense_manager.get_expenses()
                self.table.setRowCount(len(transactions))
                
                for row, trans in enumerate(transactions):
                    party = self.party_manager.get_party_by_id(trans.party_id) if trans.party_id else None
                    
                    self.table.setItem(row, 0, QTableWidgetItem(trans.date.strftime("%Y-%m-%d")))
                    self.table.setItem(row, 1, QTableWidgetItem(trans.category))
                    self.table.setItem(row, 2, QTableWidgetItem(f"{trans.amount_afg:.2f}"))
                    self.table.setItem(row, 3, QTableWidgetItem(party.name if party else ""))
                    
                    action_widget = self.create_action_buttons(trans, 'expense')
                    self.table.setCellWidget(row, 4, action_widget)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data: {e}")
    
    def create_action_buttons(self, transaction, trans_type):
        """Create action buttons for transaction"""
        action_layout = QHBoxLayout()
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(lambda: self.delete_transaction(transaction, trans_type))
        
        action_widget = QWidget()
        action_widget.setLayout(action_layout)
        action_layout.addWidget(delete_btn)
        
        return action_widget
    
    def add_transaction(self):
        """Add new transaction"""
        if self.transaction_type == 'sales':
            dialog = SalesDialog(self, None, self.sales_manager, self.party_manager)
        elif self.transaction_type == 'purchases':
            dialog = PurchaseDialog(self, None, self.purchase_manager, self.party_manager, self.inventory_manager)
        else:
            dialog = ExpenseDialog(self, None, self.expense_manager, self.party_manager)
        
        if dialog.exec():
            self.refresh_data()
    
    def delete_transaction(self, transaction, trans_type):
        """Delete transaction"""
        reply = QMessageBox.question(self, "Confirm Delete", "Delete this transaction?")
        if reply == QMessageBox.Yes:
            QMessageBox.information(self, "Info", "Transaction deletion not fully implemented")
            # TODO: Implement actual deletion


class SalesDialog(QDialog):
    """Sales dialog"""
    
    def __init__(self, parent, sale, sales_manager, party_manager):
        super().__init__(parent)
        self.sale = sale
        self.sales_manager = sales_manager
        self.party_manager = party_manager
        
        self.setWindowTitle("New Sale")
        self.setGeometry(100, 100, 400, 250)
        
        layout = QFormLayout()
        
        self.date_edit = QDateTimeEdit()
        self.date_edit.setDateTime(QDateTime.currentDateTime())
        
        self.party_combo = QComboBox()
        for party in party_manager.get_all_parties():
            self.party_combo.addItem(party.name, party.id)
        
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMaximum(10000)
        
        self.rate_afg_spin = QDoubleSpinBox()
        self.rate_usd_spin = QDoubleSpinBox()
        
        layout.addRow("Date:", self.date_edit)
        layout.addRow("Party:", self.party_combo)
        layout.addRow("Quantity:", self.quantity_spin)
        layout.addRow("Rate (AFG):", self.rate_afg_spin)
        layout.addRow("Rate (USD):", self.rate_usd_spin)
        
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        save_btn.clicked.connect(self.save_sale)
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addRow(btn_layout)
        
        self.setLayout(layout)
    
    def save_sale(self):
        """Save sale"""
        try:
            self.sales_manager.record_sale(
                self.party_combo.currentData(),
                self.quantity_spin.value(),
                self.rate_afg_spin.value(),
                self.rate_usd_spin.value(),
                date=self.date_edit.dateTime().toPython()
            )
            QMessageBox.information(self, "Success", "Sale recorded successfully")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to record sale: {e}")


class PurchaseDialog(QDialog):
    """Purchase dialog"""
    
    def __init__(self, parent, purchase, purchase_manager, party_manager, inventory_manager):
        super().__init__(parent)
        self.purchase = purchase
        self.purchase_manager = purchase_manager
        self.party_manager = party_manager
        self.inventory_manager = inventory_manager
        
        self.setWindowTitle("New Purchase")
        self.setGeometry(100, 100, 400, 300)
        
        layout = QFormLayout()
        
        self.date_edit = QDateTimeEdit()
        self.date_edit.setDateTime(QDateTime.currentDateTime())
        
        self.party_combo = QComboBox()
        for party in party_manager.get_all_parties():
            self.party_combo.addItem(party.name, party.id)
        
        self.material_combo = QComboBox()
        materials = inventory_manager.inventory_manager.session.query(RawMaterial).all() if hasattr(inventory_manager, 'inventory_manager') else []
        for material in materials:
            self.material_combo.addItem(material.name, material.id)
        
        self.quantity_spin = QDoubleSpinBox()
        self.quantity_spin.setMaximum(10000)
        
        self.rate_afg_spin = QDoubleSpinBox()
        self.rate_usd_spin = QDoubleSpinBox()
        
        layout.addRow("Date:", self.date_edit)
        layout.addRow("Party:", self.party_combo)
        layout.addRow("Material:", self.material_combo)
        layout.addRow("Quantity:", self.quantity_spin)
        layout.addRow("Rate (AFG):", self.rate_afg_spin)
        layout.addRow("Rate (USD):", self.rate_usd_spin)
        
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        save_btn.clicked.connect(self.save_purchase)
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addRow(btn_layout)
        
        self.setLayout(layout)
    
    def save_purchase(self):
        """Save purchase"""
        try:
            self.purchase_manager.record_purchase(
                self.party_combo.currentData(),
                self.material_combo.currentData(),
                self.quantity_spin.value(),
                self.rate_afg_spin.value(),
                self.rate_usd_spin.value(),
                date=self.date_edit.dateTime().toPython()
            )
            QMessageBox.information(self, "Success", "Purchase recorded successfully")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to record purchase: {e}")


class ExpenseDialog(QDialog):
    """Expense dialog"""
    
    def __init__(self, parent, expense, expense_manager, party_manager):
        super().__init__(parent)
        self.expense = expense
        self.expense_manager = expense_manager
        self.party_manager = party_manager
        
        self.setWindowTitle("New Expense")
        self.setGeometry(100, 100, 400, 250)
        
        layout = QFormLayout()
        
        self.date_edit = QDateTimeEdit()
        self.date_edit.setDateTime(QDateTime.currentDateTime())
        
        self.category_combo = QComboBox()
        for category in EXPENSE_CATEGORIES:
            self.category_combo.addItem(category)
        
        self.amount_afg_spin = QDoubleSpinBox()
        self.amount_usd_spin = QDoubleSpinBox()
        
        self.party_combo = QComboBox()
        self.party_combo.addItem("No Party", None)
        for party in party_manager.get_all_parties():
            self.party_combo.addItem(party.name, party.id)
        
        layout.addRow("Date:", self.date_edit)
        layout.addRow("Category:", self.category_combo)
        layout.addRow("Amount (AFG):", self.amount_afg_spin)
        layout.addRow("Amount (USD):", self.amount_usd_spin)
        layout.addRow("Party:", self.party_combo)
        
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        save_btn.clicked.connect(self.save_expense)
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addRow(btn_layout)
        
        self.setLayout(layout)
    
    def save_expense(self):
        """Save expense"""
        try:
            self.expense_manager.record_expense(
                1,  # TODO: Get actual farm_id
                self.category_combo.currentText(),
                self.amount_afg_spin.value(),
                self.amount_usd_spin.value(),
                party_id=self.party_combo.currentData(),
                date=self.date_edit.dateTime().toPython()
            )
            QMessageBox.information(self, "Success", "Expense recorded successfully")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to record expense: {e}")
