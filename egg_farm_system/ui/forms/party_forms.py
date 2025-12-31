"""
Form widgets for parties
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QFormLayout,
    QTextEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from modules.parties import PartyManager
from modules.ledger import LedgerManager

class PartyFormWidget(QWidget):
    """Party management widget"""
    
    def __init__(self):
        super().__init__()
        self.party_manager = PartyManager()
        self.ledger_manager = LedgerManager()
        self.init_ui()
        self.refresh_parties()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Party Management")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # New party button
        btn_layout = QHBoxLayout()
        new_party_btn = QPushButton("Add New Party")
        new_party_btn.clicked.connect(self.add_party)
        btn_layout.addWidget(new_party_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Parties table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Name", "Phone", "Balance AFG", "Balance USD", "Actions"])
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 120)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 150)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def refresh_parties(self):
        """Refresh parties table"""
        try:
            parties = self.party_manager.get_all_parties()
            self.table.setRowCount(len(parties))
            
            for row, party in enumerate(parties):
                balance_afg = self.ledger_manager.get_party_balance(party.id, "AFG")
                balance_usd = self.ledger_manager.get_party_balance(party.id, "USD")
                
                self.table.setItem(row, 0, QTableWidgetItem(party.name))
                self.table.setItem(row, 1, QTableWidgetItem(party.phone or ""))
                self.table.setItem(row, 2, QTableWidgetItem(f"{balance_afg:,.2f}"))
                self.table.setItem(row, 3, QTableWidgetItem(f"{balance_usd:,.2f}"))
                
                # Actions
                action_layout = QHBoxLayout()
                view_btn = QPushButton("View")
                view_btn.clicked.connect(lambda checked, p=party: self.view_party(p))
                edit_btn = QPushButton("Edit")
                edit_btn.clicked.connect(lambda checked, p=party: self.edit_party(p))
                delete_btn = QPushButton("Delete")
                delete_btn.clicked.connect(lambda checked, p=party: self.delete_party(p))
                
                action_widget = QWidget()
                action_widget.setLayout(action_layout)
                action_layout.addWidget(view_btn)
                action_layout.addWidget(edit_btn)
                action_layout.addWidget(delete_btn)
                
                self.table.setCellWidget(row, 4, action_widget)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load parties: {e}")
    
    def add_party(self):
        """Add new party dialog"""
        dialog = PartyDialog(self, None, self.party_manager)
        if dialog.exec():
            self.refresh_parties()
    
    def view_party(self, party):
        """View party ledger"""
        try:
            statement = self.ledger_manager.get_ledger_summary(party.id)
            if statement:
                msg = f"""
                Party: {party.name}
                Phone: {party.phone or 'N/A'}
                Address: {party.address or 'N/A'}
                
                Ledger Summary:
                Total Debit AFG: {statement['total_debit_afg']:.2f}
                Total Credit AFG: {statement['total_credit_afg']:.2f}
                Balance AFG: {statement['balance_afg']:.2f}
                
                Total Debit USD: {statement['total_debit_usd']:.2f}
                Total Credit USD: {statement['total_credit_usd']:.2f}
                Balance USD: {statement['balance_usd']:.2f}
                
                Total Entries: {statement['entry_count']}
                Last Entry: {statement['last_entry_date']}
                """
                QMessageBox.information(self, "Party Statement", msg)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to view party: {e}")
    
    def edit_party(self, party):
        """Edit party dialog"""
        dialog = PartyDialog(self, party, self.party_manager)
        if dialog.exec():
            self.refresh_parties()
    
    def delete_party(self, party):
        """Delete party"""
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete '{party.name}'?"
        )
        if reply == QMessageBox.Yes:
            try:
                self.party_manager.delete_party(party.id)
                self.refresh_parties()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete: {e}")


class PartyDialog(QDialog):
    """Party creation/edit dialog"""
    
    def __init__(self, parent, party, party_manager):
        super().__init__(parent)
        self.party = party
        self.party_manager = party_manager
        
        self.setWindowTitle("Party Details" if party else "New Party")
        self.setGeometry(100, 100, 400, 300)
        
        layout = QFormLayout()
        
        self.name_edit = QLineEdit()
        self.phone_edit = QLineEdit()
        self.address_edit = QTextEdit()
        self.notes_edit = QTextEdit()
        
        if party:
            self.name_edit.setText(party.name)
            self.phone_edit.setText(party.phone or "")
            self.address_edit.setText(party.address or "")
            self.notes_edit.setText(party.notes or "")
        
        layout.addRow("Name:", self.name_edit)
        layout.addRow("Phone:", self.phone_edit)
        layout.addRow("Address:", self.address_edit)
        layout.addRow("Notes:", self.notes_edit)
        
        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        
        save_btn.clicked.connect(self.save_party)
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addRow(btn_layout)
        
        self.setLayout(layout)
    
    def save_party(self):
        """Save party"""
        try:
            name = self.name_edit.text().strip()
            phone = self.phone_edit.text().strip()
            address = self.address_edit.toPlainText().strip()
            notes = self.notes_edit.toPlainText().strip()
            
            if not name:
                QMessageBox.warning(self, "Validation", "Party name is required")
                return
            
            if self.party:
                self.party_manager.update_party(self.party.id, name, phone, address, notes)
            else:
                self.party_manager.create_party(name, phone, address, notes)
            
            QMessageBox.information(self, "Success", "Party saved successfully")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {e}")
