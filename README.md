# Egg Farm Management System

A comprehensive Windows desktop application for managing egg farms with SQLite database and dual currency support.

## Features

- **Farm Management**: Create and manage up to 4 farms
- **Shed & Flock Management**: Track sheds, flocks, and bird mortality
- **Egg Production**: Daily egg collection with grading (Small, Medium, Large, Broken)
- **Feed Manufacturing**: Raw material management, feed formulation, and batch production
- **Inventory Management**: Raw materials, finished feed, low stock alerts
- **Party Management**: Unified customer/supplier system
- **Ledger & Accounting**: Complete financial tracking with dual currency (AFG/USD)
- **Sales & Purchases**: Transaction recording with auto ledger posting
- **Expenses & Payments**: Expense tracking and payment management
- **Reports**: Daily/monthly production, feed usage, party statements, CSV export
- **Dashboard**: Key metrics at a glance

## Technology Stack

- **Python 3.11+**
- **PySide6** (Qt for Python) - UI Framework
- **SQLAlchemy** - ORM
- **SQLite** - Local Database
- **matplotlib/pyqtgraph** - Charts and Analytics

## Installation

1. Install Python 3.11 or later
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
python egg_farm_system/app.py
```

## Building to EXE

```bash
pip install pyinstaller
pyinstaller --onefile --windowed egg_farm_system/app.py
```

## Project Structure

```
egg_farm_system/
├── app.py                 # Main entry point
├── config.py             # Configuration settings
├── database/
│   ├── db.py            # Database manager
│   └── models.py        # SQLAlchemy models
├── modules/
│   ├── farms.py         # Farm management
│   ├── sheds.py         # Shed management
│   ├── flocks.py        # Flock management
│   ├── egg_production.py # Egg tracking
│   ├── feed_mill.py     # Feed manufacturing
│   ├── inventory.py     # Inventory management
│   ├── parties.py       # Party management
│   ├── ledger.py        # Accounting
│   ├── sales.py         # Sales transactions
│   ├── purchases.py     # Purchase transactions
│   ├── expenses.py      # Expenses & payments
│   └── reports.py       # Report generation
├── ui/
│   ├── main_window.py   # Main window
│   ├── dashboard.py     # Dashboard widget
│   ├── forms/           # Form widgets
│   └── reports/         # Report viewer
├── utils/
│   ├── currency.py      # Currency utilities
│   └── calculations.py  # Business calculations
└── assets/              # Images and resources
```

## Database

- **Type**: SQLite (.db file in data/ directory)
- **Auto-created**: On first run
- **Location**: `/data/egg_farm.db`

## Accounting System

### Ledger Balance Rules
- **Positive Balance**: Party owes us
- **Negative Balance**: We owe the party

### Dual Currency
- **Base Currency**: AFG
- **Secondary Currency**: USD
- **Exchange Rate**: Configurable, stored per transaction

## Key Business Logic

1. **Egg Production**: Tracked by shed with automatic grading
2. **Feed Manufacturing**: Cost calculated from raw materials
3. **Inventory**: Weighted average cost method for valuation
4. **Party Ledger**: Single unified ledger per party
5. **Auto Posting**: All transactions automatically post to ledger

## Default Settings

- Max Farms: 4
- Base Currency: AFG
- Secondary Currency: USD
- Default Exchange Rate: 78 AFG = 1 USD

## Notes

- Single user application (no login system)
- Fully offline - no internet required
- Windows desktop application
- Ready for PyInstaller conversion to .exe

## Future Enhancements

- Advanced charting and analytics
- Backup and restore functionality
- Multi-user support with roles
- Cloud sync capability
- Mobile companion app