"""
Form widgets for egg production
"""
from datetime import datetime, timedelta
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QFormLayout,
    QSpinBox, QDateTimeEdit, QComboBox
)
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QFont

from modules.farms import FarmManager
from modules.sheds import ShedManager
from modules.flocks import FlockManager
from modules.egg_production import EggProductionManager

class ProductionFormWidget(QWidget):
    """Egg production tracking widget"""
    
    def __init__(self, farm_id):
        super().__init__()
        self.farm_id = farm_id
        self.farm_manager = FarmManager()
        self.shed_manager = ShedManager()
        self.flock_manager = FlockManager()
        self.egg_manager = EggProductionManager()
        
        self.init_ui()
        self.refresh_data()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Egg Production Tracking")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Farm and shed selector
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Shed:"))
        self.shed_combo = QComboBox()
        self.shed_combo.currentIndexChanged.connect(self.on_shed_changed)
        selector_layout.addWidget(self.shed_combo)
        selector_layout.addStretch()
        layout.addLayout(selector_layout)
        
        # New production button
        btn_layout = QHBoxLayout()
        new_prod_btn = QPushButton("Record Production")
        new_prod_btn.clicked.connect(self.record_production)
        btn_layout.addWidget(new_prod_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Production table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Date", "Small", "Medium", "Large", "Broken", "Total", "Actions"])
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def refresh_data(self):
        """Refresh sheds and production data"""
        try:
            if not self.farm_id:
                return
            
            self.shed_combo.clear()
            farm = self.farm_manager.get_farm_by_id(self.farm_id)
            if farm:
                for shed in farm.sheds:
                    self.shed_combo.addItem(shed.name, shed.id)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data: {e}")
    
    def on_shed_changed(self):
        """Handle shed selection change"""
        self.refresh_productions()
    
    def refresh_productions(self):
        """Refresh production table"""
        try:
            shed_id = self.shed_combo.currentData()
            if not shed_id:
                return
            
            start_date = datetime.utcnow() - timedelta(days=30)
            end_date = datetime.utcnow()
            
            productions = self.egg_manager.get_daily_production(shed_id, start_date, end_date)
            self.table.setRowCount(len(productions))
            
            for row, prod in enumerate(productions):
                self.table.setItem(row, 0, QTableWidgetItem(prod.date.strftime("%Y-%m-%d")))
                self.table.setItem(row, 1, QTableWidgetItem(str(prod.small_count)))
                self.table.setItem(row, 2, QTableWidgetItem(str(prod.medium_count)))
                self.table.setItem(row, 3, QTableWidgetItem(str(prod.large_count)))
                self.table.setItem(row, 4, QTableWidgetItem(str(prod.broken_count)))
                self.table.setItem(row, 5, QTableWidgetItem(str(prod.total_eggs)))
                
                # Actions
                action_layout = QHBoxLayout()
                edit_btn = QPushButton("Edit")
                edit_btn.clicked.connect(lambda checked, p=prod: self.edit_production(p))
                delete_btn = QPushButton("Delete")
                delete_btn.clicked.connect(lambda checked, p=prod: self.delete_production(p))
                
                action_widget = QWidget()
                action_widget.setLayout(action_layout)
                action_layout.addWidget(edit_btn)
                action_layout.addWidget(delete_btn)
                
                self.table.setCellWidget(row, 6, action_widget)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load productions: {e}")
    
    def record_production(self):
        """Record new production"""
        shed_id = self.shed_combo.currentData()
        if not shed_id:
            QMessageBox.warning(self, "Error", "Please select a shed")
            return
        
        dialog = ProductionDialog(self, shed_id, None, self.egg_manager)
        if dialog.exec():
            self.refresh_productions()
    
    def edit_production(self, production):
        """Edit production"""
        dialog = ProductionDialog(self, production.shed_id, production, self.egg_manager)
        if dialog.exec():
            self.refresh_productions()
    
    def delete_production(self, production):
        """Delete production"""
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Delete production record for {production.date.date()}?"
        )
        if reply == QMessageBox.Yes:
            try:
                self.egg_manager.delete_production(production.id)
                self.refresh_productions()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete: {e}")


class ProductionDialog(QDialog):
    """Production recording dialog"""
    
    def __init__(self, parent, shed_id, production, egg_manager):
        super().__init__(parent)
        self.shed_id = shed_id
        self.production = production
        self.egg_manager = egg_manager
        
        self.setWindowTitle("Egg Production" if production else "Record Production")
        self.setGeometry(100, 100, 400, 300)
        
        layout = QFormLayout()
        
        self.date_edit = QDateTimeEdit()
        self.date_edit.setDateTime(QDateTime.currentDateTime())
        
        self.small_spin = QSpinBox()
        self.medium_spin = QSpinBox()
        self.large_spin = QSpinBox()
        self.broken_spin = QSpinBox()
        
        if production:
            self.date_edit.setDateTime(QDateTime(production.date))
            self.small_spin.setValue(production.small_count)
            self.medium_spin.setValue(production.medium_count)
            self.large_spin.setValue(production.large_count)
            self.broken_spin.setValue(production.broken_count)
        
        layout.addRow("Date:", self.date_edit)
        layout.addRow("Small:", self.small_spin)
        layout.addRow("Medium:", self.medium_spin)
        layout.addRow("Large:", self.large_spin)
        layout.addRow("Broken:", self.broken_spin)
        
        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        
        save_btn.clicked.connect(self.save_production)
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addRow(btn_layout)
        
        self.setLayout(layout)
    
    def save_production(self):
        """Save production"""
        try:
            if self.production:
                self.egg_manager.update_production(
                    self.production.id,
                    self.small_spin.value(),
                    self.medium_spin.value(),
                    self.large_spin.value(),
                    self.broken_spin.value()
                )
            else:
                self.egg_manager.record_production(
                    self.shed_id,
                    self.date_edit.dateTime().toPython(),
                    self.small_spin.value(),
                    self.medium_spin.value(),
                    self.large_spin.value(),
                    self.broken_spin.value()
                )
            
            QMessageBox.information(self, "Success", "Production recorded successfully")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {e}")
