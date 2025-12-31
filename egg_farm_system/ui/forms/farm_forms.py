"""
Form widgets for farms
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QFormLayout,
    QSpinBox, QDoubleSpinBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from modules.farms import FarmManager
from modules.sheds import ShedManager
from config import MAX_FARMS

class FarmFormWidget(QWidget):
    """Farm management widget"""
    
    farm_changed = Signal()
    
    def __init__(self):
        super().__init__()
        self.farm_manager = FarmManager()
        self.shed_manager = ShedManager()
        self.init_ui()
        self.refresh_farms()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Farm Management")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # New farm button
        btn_layout = QHBoxLayout()
        new_farm_btn = QPushButton("Add New Farm")
        new_farm_btn.clicked.connect(self.add_farm)
        btn_layout.addWidget(new_farm_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Farms table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "Location", "Sheds", "Actions"])
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 150)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def refresh_farms(self):
        """Refresh farms table"""
        try:
            farms = self.farm_manager.get_all_farms()
            self.table.setRowCount(len(farms))
            
            for row, farm in enumerate(farms):
                self.table.setItem(row, 0, QTableWidgetItem(farm.name))
                self.table.setItem(row, 1, QTableWidgetItem(farm.location or ""))
                self.table.setItem(row, 2, QTableWidgetItem(str(len(farm.sheds))))
                
                # Actions
                action_layout = QHBoxLayout()
                edit_btn = QPushButton("Edit")
                edit_btn.clicked.connect(lambda checked, f=farm: self.edit_farm(f))
                delete_btn = QPushButton("Delete")
                delete_btn.clicked.connect(lambda checked, f=farm: self.delete_farm(f))
                
                action_widget = QWidget()
                action_widget.setLayout(action_layout)
                action_layout.addWidget(edit_btn)
                action_layout.addWidget(delete_btn)
                
                self.table.setCellWidget(row, 3, action_widget)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load farms: {e}")
    
    def add_farm(self):
        """Add new farm dialog"""
        dialog = FarmDialog(self, None)
        if dialog.exec():
            self.refresh_farms()
            self.farm_changed.emit()
    
    def edit_farm(self, farm):
        """Edit farm dialog"""
        dialog = FarmDialog(self, farm)
        if dialog.exec():
            self.refresh_farms()
            self.farm_changed.emit()
    
    def delete_farm(self, farm):
        """Delete farm"""
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete farm '{farm.name}'?"
        )
        if reply == QMessageBox.Yes:
            try:
                self.farm_manager.delete_farm(farm.id)
                self.refresh_farms()
                self.farm_changed.emit()
                QMessageBox.information(self, "Success", "Farm deleted successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete farm: {e}")


class FarmDialog(QDialog):
    """Farm creation/edit dialog"""
    
    def __init__(self, parent, farm):
        super().__init__(parent)
        self.farm = farm
        self.farm_manager = FarmManager()
        
        self.setWindowTitle("Farm Details" if farm else "New Farm")
        self.setGeometry(100, 100, 400, 200)
        
        layout = QFormLayout()
        
        self.name_edit = QLineEdit()
        self.location_edit = QLineEdit()
        
        if farm:
            self.name_edit.setText(farm.name)
            self.location_edit.setText(farm.location or "")
        
        layout.addRow("Farm Name:", self.name_edit)
        layout.addRow("Location:", self.location_edit)
        
        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        
        save_btn.clicked.connect(self.save_farm)
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        
        layout.addRow(btn_layout)
        
        self.setLayout(layout)
    
    def save_farm(self):
        """Save farm"""
        try:
            name = self.name_edit.text().strip()
            location = self.location_edit.text().strip()
            
            if not name:
                QMessageBox.warning(self, "Validation", "Farm name is required")
                return
            
            if self.farm:
                self.farm_manager.update_farm(self.farm.id, name, location)
                QMessageBox.information(self, "Success", "Farm updated successfully")
            else:
                farms = self.farm_manager.get_all_farms()
                if len(farms) >= 4:
                    QMessageBox.warning(
                        self, "Limit Reached",
                        f"Maximum {4} farms allowed"
                    )
                    return
                
                self.farm_manager.create_farm(name, location)
                QMessageBox.information(self, "Success", "Farm created successfully")
            
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save farm: {e}")
