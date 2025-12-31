"""
Main application window
"""
import sys
import logging
from datetime import datetime
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame,
    QPushButton, QLabel, QComboBox, QMessageBox, QTabWidget
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont

from database.db import DatabaseManager
from modules.farms import FarmManager
from config import WINDOW_WIDTH, WINDOW_HEIGHT, SIDEBAR_WIDTH
from ui.dashboard import DashboardWidget
from ui.forms.farm_forms import FarmFormWidget
from ui.forms.production_forms import ProductionFormWidget
from ui.forms.inventory_forms import InventoryFormWidget
from ui.forms.party_forms import PartyFormWidget
from ui.forms.transaction_forms import TransactionFormWidget
from ui.reports.report_viewer import ReportViewerWidget

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Egg Farm Management System")
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        DatabaseManager.initialize()
        self.farm_manager = FarmManager()
        
        # Create main layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        
        # Create sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar, 0)
        
        # Create content area
        self.content_area = QFrame()
        self.content_layout = QVBoxLayout()
        self.content_area.setLayout(self.content_layout)
        main_layout.addWidget(self.content_area, 1)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # Load dashboard initially
        self.load_dashboard()
    
    def create_sidebar(self):
        """Create left sidebar navigation"""
        sidebar = QFrame()
        sidebar.setMaximumWidth(SIDEBAR_WIDTH)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #f0f0f0;
                border-right: 1px solid #ddd;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Header
        header_label = QLabel("Navigation")
        header_font = QFont()
        header_font.setPointSize(12)
        header_font.setBold(True)
        header_label.setFont(header_font)
        layout.addWidget(header_label)
        
        # Farm selector
        layout.addWidget(QLabel("Select Farm:"))
        self.farm_combo = QComboBox()
        self.farm_combo.currentIndexChanged.connect(self.on_farm_changed)
        self.refresh_farm_list()
        layout.addWidget(self.farm_combo)
        
        # Navigation buttons
        nav_buttons = [
            ("Dashboard", self.load_dashboard),
            ("Farm Management", self.load_farm_management),
            ("Egg Production", self.load_production),
            ("Feed Management", self.load_feed_management),
            ("Inventory", self.load_inventory),
            ("Parties", self.load_parties),
            ("Sales", self.load_sales),
            ("Purchases", self.load_purchases),
            ("Expenses", self.load_expenses),
            ("Reports", self.load_reports),
        ]
        
        for button_text, callback in nav_buttons:
            btn = QPushButton(button_text)
            btn.clicked.connect(callback)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # Exit button
        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(self.close_application)
        exit_btn.setStyleSheet("QPushButton { background-color: #ff6b6b; color: white; }")
        layout.addWidget(exit_btn)
        
        sidebar.setLayout(layout)
        return sidebar
    
    def refresh_farm_list(self):
        """Refresh farm combo box"""
        try:
            self.farm_combo.clear()
            farms = self.farm_manager.get_all_farms()
            for farm in farms:
                self.farm_combo.addItem(farm.name, farm.id)
        except Exception as e:
            logger.error(f"Error refreshing farm list: {e}")
    
    def get_current_farm_id(self):
        """Get selected farm ID"""
        return self.farm_combo.currentData()
    
    def on_farm_changed(self):
        """Handle farm selection change"""
        if self.farm_combo.count() > 0:
            # Reload current widget with new farm
            pass
    
    def clear_content(self):
        """Clear content area"""
        while self.content_layout.count():
            self.content_layout.takeAt(0).widget().deleteLater()
    
    def load_dashboard(self):
        """Load dashboard widget"""
        self.clear_content()
        dashboard = DashboardWidget(self.get_current_farm_id())
        self.content_layout.addWidget(dashboard)
    
    def load_farm_management(self):
        """Load farm management widget"""
        self.clear_content()
        farm_widget = FarmFormWidget()
        farm_widget.farm_changed.connect(self.refresh_farm_list)
        self.content_layout.addWidget(farm_widget)
    
    def load_production(self):
        """Load egg production widget"""
        self.clear_content()
        prod_widget = ProductionFormWidget(self.get_current_farm_id())
        self.content_layout.addWidget(prod_widget)
    
    def load_feed_management(self):
        """Load feed management widget"""
        self.clear_content()
        from ui.forms.feed_forms import FeedFormWidget
        feed_widget = FeedFormWidget()
        self.content_layout.addWidget(feed_widget)
    
    def load_inventory(self):
        """Load inventory widget"""
        self.clear_content()
        inventory_widget = InventoryFormWidget()
        self.content_layout.addWidget(inventory_widget)
    
    def load_parties(self):
        """Load parties widget"""
        self.clear_content()
        party_widget = PartyFormWidget()
        self.content_layout.addWidget(party_widget)
    
    def load_sales(self):
        """Load sales widget"""
        self.clear_content()
        sales_widget = TransactionFormWidget("sales")
        self.content_layout.addWidget(sales_widget)
    
    def load_purchases(self):
        """Load purchases widget"""
        self.clear_content()
        purchases_widget = TransactionFormWidget("purchases")
        self.content_layout.addWidget(purchases_widget)
    
    def load_expenses(self):
        """Load expenses widget"""
        self.clear_content()
        expenses_widget = TransactionFormWidget("expenses")
        self.content_layout.addWidget(expenses_widget)
    
    def load_reports(self):
        """Load reports widget"""
        self.clear_content()
        reports_widget = ReportViewerWidget()
        self.content_layout.addWidget(reports_widget)
    
    def close_application(self):
        """Close application"""
        DatabaseManager.close()
        self.close()
    
    def closeEvent(self, event):
        """Handle window close"""
        DatabaseManager.close()
        event.accept()
