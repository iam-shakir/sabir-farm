# Technical Specification - Egg Farm Management System

## System Overview

**Project**: Egg Farm Management System  
**Version**: 1.0.0  
**Type**: Single-user Windows desktop application  
**Target Users**: Egg farm managers and owners  
**Platform**: Windows 10+, Python 3.11+  

## Functional Requirements

### 1. Farm Management (Complete)
- [x] Create/Read/Update/Delete farms (max 4)
- [x] Store farm name and location
- [x] Auto-calculate farm statistics (sheds, capacity, expenses)
- [x] Display farm summary on dashboard

### 2. Shed & Flock Management (Complete)
- [x] Create sheds per farm
- [x] Define shed capacity
- [x] Create flocks in sheds
- [x] Track flock start date and initial bird count
- [x] Record daily mortality
- [x] Auto-calculate: live birds, age, mortality %
- [x] Support multiple flocks per shed

### 3. Egg Production (Complete)
- [x] Daily egg collection per shed
- [x] Grading: Small, Medium, Large, Broken
- [x] Auto-calculate: total, usable eggs
- [x] Production percentage tracking
- [x] Daily/monthly/farm-wise reports

### 4. Feed Manufacturing (Complete)
- [x] Raw material management
  - [x] Stock tracking
  - [x] Cost in AFG and USD
  - [x] Supplier linking
  - [x] Low stock alerts
- [x] Feed formulation
  - [x] Types: Starter, Grower, Layer
  - [x] Ingredient percentage formula
  - [x] Validation (must equal 100%)
  - [x] Automatic cost calculation
- [x] Feed batch production
  - [x] Input material deduction
  - [x] Finished feed stock creation
  - [x] Cost per kg calculation
  - [x] Batch tracking
- [x] Feed consumption
  - [x] Daily issue to sheds
  - [x] Feed balance tracking
  - [x] Cost per egg calculation

### 5. Inventory Management (Complete)
- [x] Raw materials inventory
- [x] Finished feed inventory
- [x] Low stock alerts
- [x] Inventory valuation (AFG & USD)
- [x] Stock level reporting

### 6. Party Management (Complete)
- [x] Unified customer/supplier table
- [x] Party CRUD operations
- [x] Phone, address, notes
- [x] Party-wise statistics
- [x] Outstanding balance tracking

### 7. Ledger & Accounting (Complete)
- [x] One ledger per party
- [x] Debit/Credit entries
- [x] Balance calculation
- [x] Running balance tracking
- [x] Dual currency support
- [x] Exchange rate tracking

### 8. Sales Module (Complete)
- [x] Egg sales linked to party
- [x] Quantity and rate tracking
- [x] Auto ledger posting
- [x] Sales reports
- [x] Dual currency

### 9. Purchase Module (Complete)
- [x] Material purchases
- [x] Supplier linking
- [x] Inventory updates
- [x] Auto ledger posting
- [x] Purchase history

### 10. Payment Module (Complete)
- [x] Payment received
- [x] Payment paid
- [x] Party linking
- [x] Auto ledger posting
- [x] Reference tracking

### 11. Expense Management (Complete)
- [x] Expense categories (Labor, Medicine, Electricity, Water, Transport, Misc)
- [x] Farm-wise expenses
- [x] Optional party linking
- [x] Dual currency support
- [x] Expense reports

### 12. Dashboard (Complete)
- [x] Eggs produced today
- [x] Feed used today
- [x] Sales today
- [x] Low stock alerts
- [x] Farm comparison
- [x] Key metrics display

### 13. Reports (Complete)
- [x] Daily egg production
- [x] Monthly egg production
- [x] Feed usage report
- [x] Party ledger statement
- [x] Outstanding balances
- [x] CSV export

### 14. Dual Currency (Complete)
- [x] AFG as base currency
- [x] USD as secondary
- [x] Store both values
- [x] Exchange rate per transaction
- [x] No historical recalculation

## Non-Functional Requirements

### Performance
- [x] Fast startup (< 5 seconds)
- [x] Responsive UI (< 500ms per action)
- [x] SQLite for local, fast access
- [x] No external network calls

### Reliability
- [x] Data persistence in SQLite
- [x] Transaction integrity
- [x] Foreign key constraints
- [x] Error handling and logging

### Maintainability
- [x] Modular architecture
- [x] Clean separation of concerns
- [x] Well-documented code
- [x] Easy to extend

### Security
- [x] Local-only storage
- [x] No user authentication (single-user assumption)
- [x] SQL injection prevention (SQLAlchemy ORM)
- [x] Data validation

## Technology Specifications

### Frontend
- **Framework**: PySide6 (Qt for Python)
- **Language**: Python 3.11+
- **UI Pattern**: Multi-window with sidebar navigation
- **Charts**: matplotlib/pyqtgraph (extensible)

### Backend
- **Database**: SQLite 3
- **ORM**: SQLAlchemy 2.0+
- **Database Location**: `./egg_farm_system/data/egg_farm.db`

### Build & Deployment
- **Packaging**: PyInstaller
- **Output**: Single .exe file
- **Distribution**: Standalone Windows application

### Logging
- **Level**: INFO (configurable)
- **Output**: Console + File (`./egg_farm_system/logs/app.log`)
- **Format**: ISO 8601 timestamp, module name, level, message

## Database Schema

### Core Tables
1. **farms** - Farm entities
2. **sheds** - Sheds within farms
3. **flocks** - Bird flocks in sheds
4. **mortalities** - Daily mortality tracking
5. **egg_productions** - Daily egg collection records
6. **raw_materials** - Raw material inventory
7. **feed_formulas** - Feed formulation templates
8. **feed_formulations** - Formula ingredients
9. **feed_batches** - Produced feed batches
10. **finished_feeds** - Finished feed inventory
11. **feed_issues** - Feed issued to sheds
12. **parties** - Customers and suppliers
13. **ledgers** - Party accounting entries
14. **sales** - Egg sales transactions
15. **purchases** - Material purchase transactions
16. **payments** - Payment records
17. **expenses** - Farm expenses

### Relationships
- Farm → Sheds → Flocks
- Flock → Mortalities
- Shed → EggProductions
- Shed → FeedIssues
- FeedFormula → FeedFormulations → RawMaterials
- FeedBatch → FinishedFeed
- Party → Ledger, Sales, Purchases, Payments, Expenses

## Configuration Parameters

```python
MAX_FARMS = 4
BASE_CURRENCY = "AFG"
SECONDARY_CURRENCY = "USD"
DEFAULT_EXCHANGE_RATE = 78.0
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
LOG_LEVEL = "INFO"
```

## User Interface

### Main Window
- Sidebar navigation (250px wide)
- Content area (responsive)
- Farm selector dropdown
- Status indicators

### Navigation Items
1. Dashboard - Key metrics
2. Farm Management - CRUD farms
3. Egg Production - Track production
4. Feed Management - Feed operations
5. Inventory - Inventory view
6. Parties - Party management
7. Sales - Sales transactions
8. Purchases - Purchase transactions
9. Expenses - Expense tracking
10. Reports - Report generation

### Forms Include
- Date/Time selection
- Currency input (AFG/USD)
- Quantity spinners
- Dropdown selectors
- Text areas for notes
- Validation on save

## API/Module Interfaces

### FarmManager
```python
create_farm(name, location) → Farm
get_all_farms() → List[Farm]
get_farm_by_id(farm_id) → Farm
update_farm(farm_id, name, location) → Farm
delete_farm(farm_id) → None
get_farm_summary(farm_id) → Dict
```

### PartyManager
```python
create_party(name, phone, address, notes) → Party
get_all_parties() → List[Party]
get_party_by_id(party_id) → Party
get_party_statement(party_id) → Dict
```

### LedgerManager
```python
post_entry(party_id, date, description, ...) → Ledger
get_party_ledger(party_id) → List[Ledger]
get_party_balance(party_id, currency) → Float
get_balance_with_running(party_id, currency) → List[Dict]
```

### SalesManager
```python
record_sale(party_id, quantity, rate_afg, rate_usd, ...) → Sale
get_sales(party_id, start_date, end_date) → List[Sale]
get_sales_summary(...) → Dict
```

## Data Validation Rules

1. **Farm**: Name must be unique and non-empty
2. **Shed**: Capacity > 0
3. **Flock**: Initial count > 0, start date valid
4. **Mortality**: Count > 0, date <= today
5. **EggProduction**: All grades >= 0
6. **FeedFormula**: All ingredients must sum to 100% (±0.01%)
7. **Party**: Name must be unique and non-empty
8. **Ledger**: Debit XOR Credit (not both)
9. **Exchange Rate**: Must be > 0
10. **Prices**: Must be >= 0

## Error Handling

### Database Errors
- Catch SQLAlchemy exceptions
- Rollback on error
- Log error details
- Show user-friendly message

### Validation Errors
- Check on form save
- Show validation message
- Prevent invalid data entry

### Business Logic Errors
- Check constraints before operations
- Provide helpful error messages
- Maintain data consistency

## Backup & Recovery

### Backup Strategy
- SQLite database file can be backed up directly
- Recommended: Daily backups of data/ folder
- User responsibility (not automated in v1.0)

### Recovery
- Replace corrupted database with backup
- Application auto-creates if missing
- Backup/restore via file copy

## Audit Trail

### Logged Events
- Application start/stop
- Database initialization
- Create/Update/Delete operations
- Transaction posting
- Errors and exceptions

### Log Location
- `./egg_farm_system/logs/app.log`
- Rotating logs (optional in future)

## Performance Benchmarks

### Target Metrics
- Application start: < 5 seconds
- Database query: < 100ms (average)
- UI response: < 500ms
- Report generation: < 2 seconds
- CSV export: < 5 seconds

### Scalability Limits
- Max 4 farms: By design
- Max ~50,000 records per farm: Before noticeable slowdown
- Database file size: < 100 MB for normal operations

## Testing Strategy

### Unit Tests (Future)
- Test each manager class
- Test calculations
- Test validations

### Integration Tests (Future)
- Test data flow
- Test ledger posting
- Test inventory updates

### Manual Tests (Current)
- CRUD operations
- Ledger auto-posting
- Inventory calculations
- Report generation

## Build & Deployment

### Development Environment
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python egg_farm_system/app.py
```

### Production Build
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=app.ico egg_farm_system/app.py
```

### Distribution
- Single .exe file in dist/ folder
- No installation required
- Works on Windows 10+

## Future Roadmap

### v1.1
- Advanced charting (matplotlib/pyqtgraph)
- Database backup utility
- Custom report builder

### v1.2
- Multi-user support with roles
- Audit trail enhancements
- Data import/export tools

### v2.0
- Cloud synchronization
- Mobile companion app
- REST API for integrations

## Support & Maintenance

### Known Limitations
- Single-user only
- Windows primary target
- Limited to 4 farms
- No cloud backup (v1.0)

### Troubleshooting
- See QUICKSTART.md
- See DEVELOPER.md
- Check app.log for errors

## Compliance & Standards

- **PEP 8**: Code style compliance
- **SQLAlchemy**: ORM best practices
- **Qt**: Widget development standards
- **Version Control**: Git with semantic versioning
