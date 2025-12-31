"""
Dashboard widget
"""
from datetime import datetime, timedelta
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QGridLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from modules.farms import FarmManager
from modules.egg_production import EggProductionManager
from modules.feed_mill import FeedIssueManager
from modules.sales import SalesManager
from modules.inventory import InventoryManager

class DashboardWidget(QWidget):
    """Dashboard displaying key metrics"""
    
    def __init__(self, farm_id):
        super().__init__()
        self.farm_id = farm_id
        self.farm_manager = FarmManager()
        self.egg_manager = EggProductionManager()
        self.feed_manager = FeedIssueManager()
        self.sales_manager = SalesManager()
        self.inventory_manager = InventoryManager()
        
        self.init_ui()
        self.refresh_data()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Dashboard")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Metrics grid
        metrics_layout = QGridLayout()
        
        self.eggs_today_label = self.create_metric_box("Eggs Today", "0")
        self.feed_today_label = self.create_metric_box("Feed Used Today", "0 kg")
        self.sales_today_label = self.create_metric_box("Sales Today", "Afs 0")
        self.low_stock_label = self.create_metric_box("Low Stock Items", "0")
        
        metrics_layout.addWidget(self.eggs_today_label, 0, 0)
        metrics_layout.addWidget(self.feed_today_label, 0, 1)
        metrics_layout.addWidget(self.sales_today_label, 0, 2)
        metrics_layout.addWidget(self.low_stock_label, 0, 3)
        
        layout.addLayout(metrics_layout)
        
        # Farm summary
        self.farm_summary_text = QLabel()
        layout.addWidget(self.farm_summary_text)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def create_metric_box(self, title, value):
        """Create metric display box"""
        group = QGroupBox(title)
        group_layout = QVBoxLayout()
        
        value_label = QLabel(value)
        value_font = QFont()
        value_font.setPointSize(20)
        value_font.setBold(True)
        value_label.setFont(value_font)
        
        group_layout.addWidget(value_label)
        group.setLayout(group_layout)
        
        return group
    
    def refresh_data(self):
        """Refresh dashboard data"""
        try:
            if not self.farm_id:
                return
            
            today = datetime.utcnow()
            
            # Eggs today
            farm = self.farm_manager.get_farm_by_id(self.farm_id)
            if farm:
                total_eggs_today = 0
                for shed in farm.sheds:
                    productions = self.egg_manager.get_daily_production(
                        shed.id, today, today + timedelta(days=1)
                    )
                    total_eggs_today += sum(p.total_eggs for p in productions)
                
                self.eggs_today_label.findChild(QLabel, None).setText(str(total_eggs_today))
                
                # Feed used today
                total_feed_today = 0
                for shed in farm.sheds:
                    issues = self.feed_manager.get_shed_feed_issues(
                        shed.id, today, today + timedelta(days=1)
                    )
                    total_feed_today += sum(i.quantity_kg for i in issues)
                
                self.feed_today_label.findChild(QLabel, None).setText(
                    f"{total_feed_today:.1f} kg"
                )
                
                # Sales today
                sales = self.sales_manager.get_sales(start_date=today, end_date=today + timedelta(days=1))
                total_sales = sum(s.total_afg for s in sales)
                self.sales_today_label.findChild(QLabel, None).setText(
                    f"Afs {total_sales:,.0f}"
                )
                
                # Low stock items
                low_stock = self.inventory_manager.get_low_stock_alerts()
                self.low_stock_label.findChild(QLabel, None).setText(str(len(low_stock)))
                
                # Farm summary
                summary = self.farm_manager.get_farm_summary(self.farm_id)
                if summary:
                    summary_text = f"""
                    Farm: {summary['farm'].name}
                    Sheds: {summary['total_sheds']}
                    Total Capacity: {summary['total_capacity']} birds
                    Total Expenses: Afs {summary['total_expenses']:,.0f}
                    """
                    self.farm_summary_text.setText(summary_text)
        except Exception as e:
            print(f"Error refreshing dashboard: {e}")
