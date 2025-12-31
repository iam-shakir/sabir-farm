"""
Form widgets for inventory
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox, QDialog, QFormLayout, QLineEdit, QDoubleSpinBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from modules.inventory import InventoryManager

class InventoryFormWidget(QWidget):
    """Inventory management widget"""
    
    def __init__(self):
        super().__init__()
        self.inventory_manager = InventoryManager()
        self.init_ui()
        self.refresh_data()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Inventory Management")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Tabs for different inventory types
        self.raw_materials_table = self.create_table(
            ["Material", "Stock (kg)", "Cost AFG", "Cost USD", "Total Value AFG", "Status"]
        )
        self.finished_feed_table = self.create_table(
            ["Feed Type", "Stock (kg)", "Cost/kg AFG", "Total Value AFG", "Status"]
        )
        
        # Raw materials section
        layout.addWidget(QLabel("Raw Materials Inventory"))
        layout.addWidget(self.raw_materials_table)
        
        # Finished feed section
        layout.addWidget(QLabel("Finished Feed Inventory"))
        layout.addWidget(self.finished_feed_table)
        
        # Summary
        self.summary_label = QLabel()
        layout.addWidget(self.summary_label)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def create_table(self, headers):
        """Create data table"""
        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        return table
    
    def refresh_data(self):
        """Refresh inventory data"""
        try:
            # Raw materials
            raw_materials = self.inventory_manager.get_raw_materials_inventory()
            self.raw_materials_table.setRowCount(len(raw_materials))
            
            for row, material in enumerate(raw_materials):
                self.raw_materials_table.setItem(row, 0, QTableWidgetItem(material['name']))
                self.raw_materials_table.setItem(row, 1, QTableWidgetItem(f"{material['stock']:.2f}"))
                self.raw_materials_table.setItem(row, 2, QTableWidgetItem(f"{material['cost_afg']:.2f}"))
                self.raw_materials_table.setItem(row, 3, QTableWidgetItem(f"{material['cost_usd']:.2f}"))
                self.raw_materials_table.setItem(row, 4, QTableWidgetItem(f"{material['inventory_value_afg']:.2f}"))
                
                status = "⚠ Low" if material['is_low'] else "OK"
                self.raw_materials_table.setItem(row, 5, QTableWidgetItem(status))
            
            # Finished feed
            finished_feed = self.inventory_manager.get_finished_feed_inventory()
            self.finished_feed_table.setRowCount(len(finished_feed))
            
            for row, feed in enumerate(finished_feed):
                self.finished_feed_table.setItem(row, 0, QTableWidgetItem(feed['feed_type']))
                self.finished_feed_table.setItem(row, 1, QTableWidgetItem(f"{feed['stock_kg']:.2f}"))
                self.finished_feed_table.setItem(row, 2, QTableWidgetItem(f"{feed['cost_per_kg_afg']:.2f}"))
                self.finished_feed_table.setItem(row, 3, QTableWidgetItem(f"{feed['inventory_value_afg']:.2f}"))
                
                status = "⚠ Low" if feed['is_low'] else "OK"
                self.finished_feed_table.setItem(row, 4, QTableWidgetItem(status))
            
            # Summary
            totals = self.inventory_manager.get_total_inventory_value()
            summary_text = f"Total Inventory Value: Afs {totals['total_afg']:,.2f} (${totals['total_usd']:,.2f})"
            self.summary_label.setText(summary_text)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load inventory: {e}")
