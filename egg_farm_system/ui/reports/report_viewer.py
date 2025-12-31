"""
Report viewer widget
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton,
    QTextEdit, QMessageBox, QDateEdit
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont

from modules.reports import ReportGenerator

class ReportViewerWidget(QWidget):
    """Report viewing and export widget"""
    
    def __init__(self):
        super().__init__()
        self.report_generator = ReportGenerator()
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        title = QLabel("Reports")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Report selector
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Report:"))
        
        self.report_combo = QComboBox()
        self.report_combo.addItem("Daily Egg Production", "daily_production")
        self.report_combo.addItem("Monthly Egg Production", "monthly_production")
        self.report_combo.addItem("Feed Usage Report", "feed_usage")
        self.report_combo.addItem("Party Statement", "party_statement")
        self.report_combo.currentIndexChanged.connect(self.on_report_changed)
        selector_layout.addWidget(self.report_combo)
        selector_layout.addStretch()
        layout.addLayout(selector_layout)
        
        # Date selectors
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("Date:"))
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        date_layout.addWidget(self.date_edit)
        date_layout.addStretch()
        layout.addLayout(date_layout)
        
        # Generate and Export buttons
        btn_layout = QHBoxLayout()
        generate_btn = QPushButton("Generate Report")
        generate_btn.clicked.connect(self.generate_report)
        export_btn = QPushButton("Export to CSV")
        export_btn.clicked.connect(self.export_report)
        
        btn_layout.addWidget(generate_btn)
        btn_layout.addWidget(export_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Report content
        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        layout.addWidget(self.report_text)
        
        self.setLayout(layout)
    
    def on_report_changed(self):
        """Handle report type change"""
        self.report_text.clear()
    
    def generate_report(self):
        """Generate selected report"""
        report_type = self.report_combo.currentData()
        
        try:
            date = self.date_edit.date().toPython()
            
            if report_type == "daily_production":
                data = self.report_generator.daily_egg_production_report(1, date)  # TODO: Get farm ID
                if data:
                    text = f"Farm: {data['farm']}\nDate: {data['date']}\n\n"
                    for shed in data['sheds']:
                        text += f"{shed['name']}: {shed['total_eggs']} eggs\n"
                    text += f"\nTotal: {data['totals']['total']} eggs"
                    self.report_text.setText(text)
            else:
                QMessageBox.information(self, "Info", f"Report generation for {report_type} - implement in reports module")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate report: {e}")
    
    def export_report(self):
        """Export report to CSV"""
        QMessageBox.information(self, "Info", "CSV export - implement export functionality")
