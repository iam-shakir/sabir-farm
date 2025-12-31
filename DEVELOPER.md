# Developer Documentation - Egg Farm Management System

## Architecture Overview

The application follows a clean, modular architecture with clear separation of concerns:

```
Data Layer (Database)
    ↓
Business Logic (Modules)
    ↓
UI Layer (PySide6 Forms/Widgets)
    ↓
User Interface
```

## Module Structure

### Database Layer (`database/`)

**db.py** - Database Connection Manager
- `DatabaseManager`: Singleton managing SQLite connections
- Auto-creates tables on initialization
- Manages session lifecycle
- Enables foreign key constraints

**models.py** - SQLAlchemy ORM Models
- Defines all database entities
- Relationships between entities
- Calculated properties (e.g., flock age, egg totals)
- Enums for types (FeedType, EggGrade, TransactionType)

### Business Logic Modules (`modules/`)

Each module encapsulates business logic for a specific domain:

**farms.py** - Farm Operations
- `FarmManager`: CRUD operations for farms
- Farm summary with statistics
- Related: sheds, expenses

**sheds.py** - Shed Management
- `ShedManager`: CRUD for sheds
- Shed summary with capacity utilization
- Related: flocks, egg production, feed issues

**flocks.py** - Flock Management
- `FlockManager`: CRUD for flocks
- Mortality tracking
- Calculations: live count, age, mortality %
- Related: mortalities

**egg_production.py** - Egg Production Tracking
- `EggProductionManager`: Daily production records
- Production by grade (Small, Medium, Large, Broken)
- Daily/monthly summaries
- Farm-wide production reports

**feed_mill.py** - Feed Manufacturing
- `RawMaterialManager`: Raw material inventory
- `FeedFormulaManager`: Formula creation and validation
- `FeedProductionManager`: Batch production with cost calculation
- `FeedIssueManager`: Feed issuance to sheds
- Automatic stock updates and weighted average costing

**inventory.py** - Inventory Management
- `InventoryManager`: Consolidated inventory view
- Raw materials and finished feed
- Low stock alerts
- Inventory valuation in both currencies

**parties.py** - Party (Customer/Supplier) Management
- `PartyManager`: CRUD for unified Party table
- Party statement generation
- Related: sales, purchases, payments, expenses, ledger

**ledger.py** - Accounting and Ledger
- `LedgerManager`: Financial transaction posting
- Running balance calculations
- Party-wise ledger statements
- Multi-currency support

**sales.py** - Sales Transactions
- `SalesManager`: Record egg sales
- Auto-posting to ledger
- Sales summaries and reports

**purchases.py** - Purchase Transactions
- `PurchaseManager`: Record material purchases
- Auto-posting to ledger
- Inventory updates
- Supplier tracking

**expenses.py** - Expenses and Payments
- `ExpenseManager`: Farm expense recording
- `PaymentManager`: Payment received/paid
- Optional party linking
- Automatic ledger posting

**reports.py** - Report Generation
- `ReportGenerator`: Multi-format reports
- Daily/monthly production reports
- Feed usage analysis
- Party statements
- CSV export functionality

### Utilities (`utils/`)

**currency.py** - Currency Conversion
- `CurrencyConverter`: AFG ↔ USD conversion
- Configurable exchange rates
- Formatted output

**calculations.py** - Business Calculations
- `EggCalculations`: Production percentage, eggs per bird
- `FeedCalculations`: Feed cost per egg, efficiency ratios
- `FinancialCalculations`: Profit, margins, weighted average
- `MortalityCalculations`: Bird count, mortality %, age
- `InventoryCalculations`: Stock valuation

### UI Layer (`ui/`)

**main_window.py** - Main Application Window
- `MainWindow`: Root widget with sidebar navigation
- Farm selector dropdown
- Content area management
- Session management

**dashboard.py** - Dashboard Widget
- `DashboardWidget`: Key metrics display
- Today's statistics
- Farm summary
- Low stock alerts

**forms/** - Form Widgets for Data Entry

- **farm_forms.py**: `FarmFormWidget`, `FarmDialog`
- **production_forms.py**: `ProductionFormWidget`, `ProductionDialog`
- **inventory_forms.py**: `InventoryFormWidget`
- **party_forms.py**: `PartyFormWidget`, `PartyDialog`
- **transaction_forms.py**: `TransactionFormWidget`, `SalesDialog`, `PurchaseDialog`, `ExpenseDialog`
- **feed_forms.py**: `FeedFormWidget` (stub for expansion)

**reports/** - Report Viewing

- **report_viewer.py**: `ReportViewerWidget` for viewing and exporting

## Configuration

**config.py** - Application Configuration
```python
APP_NAME = "Egg Farm Management System"
MAX_FARMS = 4
BASE_CURRENCY = "AFG"
SECONDARY_CURRENCY = "USD"
DEFAULT_EXCHANGE_RATE = 78.0
EXPENSE_CATEGORIES = [...]
FEED_TYPES = ["Starter", "Grower", "Layer"]
EGG_GRADES = ["Small", "Medium", "Large", "Broken"]
```

## Data Flow Examples

### Recording a Sale
```
UI (SalesDialog)
  ↓
SalesManager.record_sale()
  ↓
Creates Sale record
  ↓
LedgerManager.post_entry() (auto-post)
  ↓
Creates Ledger entries (Debit Party, Credit Sales)
  ↓
Database commit
```

### Producing Feed Batch
```
UI (FeedProductionManager dialog)
  ↓
FeedProductionManager.produce_batch()
  ↓
Validate formula (sum = 100%)
  ↓
Calculate cost from raw materials
  ↓
Update RawMaterial stocks
  ↓
Create FeedBatch record
  ↓
Update FinishedFeed inventory
  ↓
Calculate weighted average cost
  ↓
Database commit
```

### Getting Party Balance
```
UI (PartyFormWidget)
  ↓
LedgerManager.get_party_balance(party_id, "AFG")
  ↓
Query Ledger table for party_id
  ↓
Sum debits - credits
  ↓
Return balance
```

## Database Schema Highlights

### Key Relationships
- **Farm** ← → Shed (1:Many)
- **Shed** ← → Flock (1:Many)
- **Flock** ← → Mortality (1:Many)
- **Shed** ← → EggProduction (1:Many)
- **Shed** ← → FeedIssue (1:Many)
- **Party** ← → Ledger (1:Many)
- **Party** ← → Sales, Purchases, Payments, Expenses (1:Many)
- **FeedFormula** ← → FeedFormulation (1:Many)
- **RawMaterial** ← → FeedFormulation (1:Many)

### Foreign Key Constraints
All relationships use ON DELETE CASCADE for data integrity.

### Dual Currency Design
Every monetary transaction stores BOTH AFG and USD values plus exchange rate used. This ensures historical accuracy even if exchange rates change.

## Adding New Features

### Add a New Module

1. Create module file in `modules/`
2. Create manager class inheriting from `DatabaseManager`
3. Implement CRUD operations
4. Add automatic logging

Example:
```python
# modules/my_feature.py
from database.db import DatabaseManager
from database.models import MyModel

class MyFeatureManager:
    def __init__(self):
        self.session = DatabaseManager.get_session()
    
    def create_record(self, **kwargs):
        try:
            record = MyModel(**kwargs)
            self.session.add(record)
            self.session.commit()
            return record
        except Exception as e:
            self.session.rollback()
            raise
```

### Add a New UI Form

1. Create form widget in `ui/forms/`
2. Inherit from `QWidget`
3. Use corresponding manager for business logic
4. Add to main window navigation

Example:
```python
# ui/forms/my_form.py
from PySide6.QtWidgets import QWidget, QVBoxLayout
from modules.my_feature import MyFeatureManager

class MyFeatureWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.manager = MyFeatureManager()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        # Add widgets
        self.setLayout(layout)
```

## Testing Approach

### Manual Testing Checklist
- [ ] Create/Read/Update/Delete for each entity
- [ ] Verify ledger auto-posting on sales/purchases
- [ ] Check inventory updates on batch production
- [ ] Validate formula percentages sum to 100%
- [ ] Verify exchange rate handling
- [ ] Test low stock alerts
- [ ] Export reports to CSV

### Future: Unit Tests
```python
# tests/test_farms.py
import unittest
from modules.farms import FarmManager

class TestFarmManager(unittest.TestCase):
    def setUp(self):
        self.manager = FarmManager()
    
    def test_create_farm(self):
        farm = self.manager.create_farm("Test Farm", "Location")
        self.assertIsNotNone(farm.id)
```

## Performance Considerations

1. **Database Indexes**: Added on frequently queried fields
2. **Lazy Loading**: Relationships loaded on-demand
3. **Batch Operations**: Use for multiple inserts
4. **Session Management**: Close sessions after use

## Security Notes

1. **SQL Injection**: SQLAlchemy prevents via ORM
2. **Input Validation**: Validate in UI and business logic
3. **File Permissions**: Database readable/writable by user only
4. **No Authentication**: Single-user system assumption
5. **Data Integrity**: Foreign keys enforced at DB level

## Future Enhancements

1. **Charts**: matplotlib/pyqtgraph integration for dashboard
2. **Backup**: Automatic database backup functionality
3. **Audit Trail**: Track all changes to sensitive records
4. **Advanced Reporting**: Custom report builder
5. **Mobile App**: Companion mobile app for data entry
6. **Cloud Sync**: Optional cloud synchronization
7. **Multi-user**: Role-based access control
8. **API**: REST API for external integrations

## Common Pitfalls

1. **Forgetting session.commit()**: Changes not persisted
2. **Not closing sessions**: Resource leaks
3. **Mixed currencies**: Always specify AFG or USD
4. **Formula validation**: Ensure percentages sum to 100%
5. **Batch operations**: Don't edit same object multiple times without flush

## Debugging Tips

1. **Enable SQL logging**: Change `echo=True` in db.py
2. **Check logs**: Located in `/egg_farm_system/logs/app.log`
3. **Database inspection**: Use SQLite browser to inspect db
4. **Print statements**: Add debugging output to trace flow
5. **Breakpoints**: Use IDE debugger for step-through

## Code Style

- Follow PEP 8 conventions
- Use type hints for clarity
- Write docstrings for all classes and methods
- Keep methods focused and small
- Use meaningful variable names
- Add logging for important operations

## Deployment

### Windows Executable
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=app.ico egg_farm_system/app.py
```

### Distribution
- Single EXE file in `dist/` folder
- No installation required
- User just runs executable
- Database created automatically on first run
