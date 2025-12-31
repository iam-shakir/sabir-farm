"""
Feed management forms
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox,
    QDialog, QFormLayout, QComboBox, QDoubleSpinBox, QTableWidget, QTableWidgetItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from modules.feed_mill import RawMaterialManager, FeedFormulaManager, FeedProductionManager

class FeedFormWidget(QWidget):
    """Feed management widget"""
    
    def __init__(self):
        super().__init__()
        self.raw_material_manager = RawMaterialManager()
        self.formula_manager = FeedFormulaManager()
        self.production_manager = FeedProductionManager()
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        title = QLabel("Feed Management")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        raw_material_btn = QPushButton("Manage Raw Materials")
        raw_material_btn.clicked.connect(self.manage_raw_materials)
        
        formula_btn = QPushButton("Manage Formulas")
        formula_btn.clicked.connect(self.manage_formulas)
        
        production_btn = QPushButton("Produce Batch")
        production_btn.clicked.connect(self.produce_batch)
        
        btn_layout.addWidget(raw_material_btn)
        btn_layout.addWidget(formula_btn)
        btn_layout.addWidget(production_btn)
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def manage_raw_materials(self):
        """Manage raw materials"""
        QMessageBox.information(self, "Info", "Raw materials management - implement raw material list and CRUD")
    
    def manage_formulas(self):
        """Manage feed formulas"""
        QMessageBox.information(self, "Info", "Feed formulas management - implement formula creation and ingredients")
    
    def produce_batch(self):
        """Produce feed batch"""
        QMessageBox.information(self, "Info", "Feed production - implement batch creation from formulas")
