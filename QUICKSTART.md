# Quick Start Guide - Egg Farm Management System

## Prerequisites

- Python 3.11 or higher
- Windows OS (primary target, but works on Linux/macOS with minimal changes)
- ~200 MB disk space for application and database

## Installation Steps

### 1. Clone Repository
```bash
git clone <repository-url>
cd sabir-farm
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Application
```bash
python egg_farm_system/app.py
```

The application will:
- Automatically create a SQLite database in `/egg_farm_system/data/`
- Open the main window with a sidebar navigation
- Display the dashboard with current farm statistics

## First-Time Setup

### 1. Create Farms
- Click "Farm Management" in the sidebar
- Click "Add New Farm"
- Enter farm name and location
- Maximum 4 farms allowed

### 2. Create Sheds
- From farm management, create sheds for each farm
- Define shed capacity
- Each shed can hold multiple flocks

### 3. Create Flocks
- Add flocks to sheds
- Record initial bird count
- Track daily mortalities

### 4. Add Parties
- Click "Parties" in sidebar
- Create customers and suppliers (both use same Party table)
- Record contact information

### 5. Set Up Feed System
- Create raw materials with costs in AFG and USD
- Define feed formulas (Starter, Grower, Layer)
- Set ingredient percentages (must equal 100%)
- Produce batches as needed

## Daily Operations

### Record Egg Production
1. Click "Egg Production" in sidebar
2. Select shed
3. Click "Record Production"
4. Enter counts by grade (Small, Medium, Large, Broken)
5. Save

### Issue Feed to Sheds
1. Click "Feed Management"
2. Select feed type and quantity
3. Select destination shed
4. Record issuance

### Record Sales
1. Click "Sales" in sidebar
2. Click "New Sale"
3. Select party and quantity
4. Enter rates in AFG and USD
5. Save (automatically posts to ledger)

### Record Purchases
1. Click "Purchases" in sidebar
2. Click "New Purchase"
3. Select supplier party and material
4. Enter quantity and rates
5. Save (automatically updates inventory and ledger)

### Record Expenses
1. Click "Expenses" in sidebar
2. Click "New Expense"
3. Select category, amount, and optional party
4. Save

## Accessing Reports

1. Click "Reports" in sidebar
2. Select report type from dropdown
3. Choose date or date range
4. Click "Generate Report"
5. Click "Export to CSV" to save report

## Ledger and Accounting

### Understanding Balances
- **Positive Balance**: Party owes us money
- **Negative Balance**: We owe the party money

### Viewing Party Statement
1. Click "Parties" in sidebar
2. Find party in table
3. Click "View" button
4. Ledger statement with running balance appears

### Dual Currency
- All amounts stored in AFG and USD
- Exchange rate recorded per transaction
- Default exchange rate: 78 AFG = 1 USD
- Can be changed in config.py

## Dashboard Metrics

The dashboard displays:
- **Eggs Today**: Total eggs produced today
- **Feed Used Today**: Total feed issued today
- **Sales Today**: Total revenue from sales today
- **Low Stock Items**: Count of materials below threshold
- **Farm Summary**: Farm statistics and capacity info

## Inventory Management

### Raw Materials
- View current stock, cost per unit
- Automatic low stock alerts
- Supplier tracking
- Weighted average cost calculation

### Finished Feed
- Track feed inventory by type
- Auto-calculated cost per kg
- Low stock alerts
- Automatic updates on batch production

## Tips

1. **Exchange Rate**: Update exchange rate in config.py if needed
2. **Backups**: Database saved in `/egg_farm_system/data/`
3. **Exports**: All reports can be exported to CSV for further analysis
4. **Party Names**: Keep party names unique and descriptive
5. **Feed Formulas**: Ensure formula percentages equal 100% (±0.01%)

## Troubleshooting

### Application Won't Start
- Check Python version: `python --version`
- Verify dependencies: `pip install -r requirements.txt`
- Check for database lock: Delete `data/egg_farm.db` and restart

### Database Issues
- Database auto-created on first run
- Located at: `egg_farm_system/data/egg_farm.db`
- Check database exists: `ls egg_farm_system/data/`

### Import Errors
- Make sure working directory is `/sabir-farm/`
- Virtual environment activated
- All dependencies installed

### UI Display Issues
- Ensure PySide6 is installed: `pip install PySide6`
- Check screen resolution (minimum 1024x768 recommended)

## Building Windows EXE

### Prerequisites
```bash
pip install pyinstaller
```

### Build Command
```bash
pyinstaller --onefile --windowed --icon=app.ico egg_farm_system/app.py
```

### Output
- EXE file located in: `dist/app.exe`
- Ready for distribution to Windows machines

## Data Location

```
sabir-farm/
├── egg_farm_system/
│   ├── data/
│   │   └── egg_farm.db          # SQLite Database
│   └── logs/
│       └── app.log              # Application logs
```

## Contact & Support

For issues, feature requests, or contributions, please refer to project documentation.

## License

[Specify your license here]
