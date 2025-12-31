"""
SQLAlchemy models for Egg Farm Management System
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from database.db import Base

# Enums
class FeedType(enum.Enum):
    STARTER = "Starter"
    GROWER = "Grower"
    LAYER = "Layer"

class EggGrade(enum.Enum):
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"
    BROKEN = "Broken"

class TransactionType(enum.Enum):
    DEBIT = "Debit"
    CREDIT = "Credit"

# Database Models

class Farm(Base):
    """Farm entity"""
    __tablename__ = "farms"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    location = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sheds = relationship("Shed", back_populates="farm", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="farm", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Farm {self.name}>"


class Shed(Base):
    """Shed within a farm"""
    __tablename__ = "sheds"
    
    id = Column(Integer, primary_key=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    name = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=False)  # Maximum bird capacity
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    farm = relationship("Farm", back_populates="sheds")
    flocks = relationship("Flock", back_populates="shed", cascade="all, delete-orphan")
    egg_productions = relationship("EggProduction", back_populates="shed", cascade="all, delete-orphan")
    feed_issues = relationship("FeedIssue", back_populates="shed", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Shed {self.name}>"


class Flock(Base):
    """Bird flock in a shed"""
    __tablename__ = "flocks"
    
    id = Column(Integer, primary_key=True)
    shed_id = Column(Integer, ForeignKey("sheds.id"), nullable=False)
    name = Column(String(100), nullable=False)
    start_date = Column(DateTime, nullable=False)
    initial_count = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    shed = relationship("Shed", back_populates="flocks")
    mortalities = relationship("Mortality", back_populates="flock", cascade="all, delete-orphan")
    
    def get_live_count(self, as_of_date=None):
        """Calculate live bird count"""
        if as_of_date is None:
            as_of_date = datetime.utcnow()
        
        total_deaths = 0
        for mortality in self.mortalities:
            if mortality.date <= as_of_date:
                total_deaths += mortality.count
        
        return self.initial_count - total_deaths
    
    def get_age_days(self, as_of_date=None):
        """Get flock age in days"""
        if as_of_date is None:
            as_of_date = datetime.utcnow()
        
        return (as_of_date - self.start_date).days
    
    def get_mortality_percentage(self, as_of_date=None):
        """Calculate mortality percentage"""
        live = self.get_live_count(as_of_date)
        if self.initial_count == 0:
            return 0
        return ((self.initial_count - live) / self.initial_count) * 100
    
    def __repr__(self):
        return f"<Flock {self.name}>"


class Mortality(Base):
    """Daily mortality tracking"""
    __tablename__ = "mortalities"
    
    id = Column(Integer, primary_key=True)
    flock_id = Column(Integer, ForeignKey("flocks.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    count = Column(Integer, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    flock = relationship("Flock", back_populates="mortalities")
    
    def __repr__(self):
        return f"<Mortality {self.flock_id} - {self.date}>"


class EggProduction(Base):
    """Daily egg production record"""
    __tablename__ = "egg_productions"
    
    id = Column(Integer, primary_key=True)
    shed_id = Column(Integer, ForeignKey("sheds.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    small_count = Column(Integer, default=0)
    medium_count = Column(Integer, default=0)
    large_count = Column(Integer, default=0)
    broken_count = Column(Integer, default=0)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    shed = relationship("Shed", back_populates="egg_productions")
    
    @property
    def total_eggs(self):
        """Total eggs produced"""
        return self.small_count + self.medium_count + self.large_count + self.broken_count
    
    @property
    def usable_eggs(self):
        """Eggs excluding broken"""
        return self.small_count + self.medium_count + self.large_count
    
    def __repr__(self):
        return f"<EggProduction {self.shed_id} - {self.date}>"


class RawMaterial(Base):
    """Raw materials for feed production"""
    __tablename__ = "raw_materials"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    unit = Column(String(50), default="kg")
    current_stock = Column(Float, default=0)
    cost_afg = Column(Float, nullable=False)  # Cost per unit in AFG
    cost_usd = Column(Float, nullable=False)  # Cost per unit in USD
    supplier_id = Column(Integer, ForeignKey("parties.id"))
    low_stock_alert = Column(Float, default=50)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    supplier = relationship("Party", back_populates="raw_materials")
    formulations = relationship("FeedFormulation", back_populates="material")
    
    def __repr__(self):
        return f"<RawMaterial {self.name}>"


class FeedFormula(Base):
    """Feed formulation master"""
    __tablename__ = "feed_formulas"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    feed_type = Column(Enum(FeedType), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ingredients = relationship("FeedFormulation", back_populates="formula")
    batches = relationship("FeedBatch", back_populates="formula")
    
    def get_total_percentage(self):
        """Get total ingredient percentage"""
        return sum(ing.percentage for ing in self.ingredients)
    
    def calculate_cost_per_kg(self, exchange_rate=78.0):
        """Calculate cost per kg of finished feed"""
        total_cost_afg = 0
        for ingredient in self.ingredients:
            total_cost_afg += ingredient.material.cost_afg * (ingredient.percentage / 100)
        return total_cost_afg
    
    def __repr__(self):
        return f"<FeedFormula {self.name}>"


class FeedFormulation(Base):
    """Ingredient in a feed formula"""
    __tablename__ = "feed_formulations"
    
    id = Column(Integer, primary_key=True)
    formula_id = Column(Integer, ForeignKey("feed_formulas.id"), nullable=False)
    material_id = Column(Integer, ForeignKey("raw_materials.id"), nullable=False)
    percentage = Column(Float, nullable=False)  # Percentage by weight
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    formula = relationship("FeedFormula", back_populates="ingredients")
    material = relationship("RawMaterial", back_populates="formulations")
    
    def __repr__(self):
        return f"<FeedFormulation {self.formula_id}-{self.material_id}>"


class FeedBatch(Base):
    """Feed production batch"""
    __tablename__ = "feed_batches"
    
    id = Column(Integer, primary_key=True)
    formula_id = Column(Integer, ForeignKey("feed_formulas.id"), nullable=False)
    batch_date = Column(DateTime, nullable=False)
    quantity_kg = Column(Float, nullable=False)
    cost_afg = Column(Float, nullable=False)
    cost_usd = Column(Float, nullable=False)
    exchange_rate_used = Column(Float, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    formula = relationship("FeedFormula", back_populates="batches")
    
    @property
    def cost_per_kg_afg(self):
        """Cost per kg in AFG"""
        return self.cost_afg / self.quantity_kg if self.quantity_kg > 0 else 0
    
    def __repr__(self):
        return f"<FeedBatch {self.id} - {self.batch_date}>"


class FinishedFeed(Base):
    """Finished feed inventory"""
    __tablename__ = "finished_feeds"
    
    id = Column(Integer, primary_key=True)
    feed_type = Column(Enum(FeedType), nullable=False)
    current_stock = Column(Float, default=0)  # in kg
    cost_per_kg_afg = Column(Float, nullable=False)
    cost_per_kg_usd = Column(Float, nullable=False)
    low_stock_alert = Column(Float, default=100)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    feed_issues = relationship("FeedIssue", back_populates="feed")
    
    def __repr__(self):
        return f"<FinishedFeed {self.feed_type.value}>"


class FeedIssue(Base):
    """Daily feed issued to shed"""
    __tablename__ = "feed_issues"
    
    id = Column(Integer, primary_key=True)
    shed_id = Column(Integer, ForeignKey("sheds.id"), nullable=False)
    feed_id = Column(Integer, ForeignKey("finished_feeds.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    quantity_kg = Column(Float, nullable=False)
    cost_afg = Column(Float, nullable=False)
    cost_usd = Column(Float, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    shed = relationship("Shed", back_populates="feed_issues")
    feed = relationship("FinishedFeed", back_populates="feed_issues")
    
    def __repr__(self):
        return f"<FeedIssue {self.shed_id} - {self.date}>"


class Party(Base):
    """Unified customer/supplier entity"""
    __tablename__ = "parties"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    phone = Column(String(20))
    address = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ledger_entries = relationship("Ledger", back_populates="party", cascade="all, delete-orphan")
    raw_materials = relationship("RawMaterial", back_populates="supplier")
    sales = relationship("Sale", back_populates="party")
    purchases = relationship("Purchase", back_populates="party")
    payments = relationship("Payment", back_populates="party")
    expenses = relationship("Expense", back_populates="party")
    
    def get_balance(self, currency="AFG"):
        """Get party balance (debit - credit)"""
        balance = 0
        for entry in self.ledger_entries:
            if currency == "AFG":
                balance += (entry.debit_afg - entry.credit_afg)
            else:  # USD
                balance += (entry.debit_usd - entry.credit_usd)
        return balance
    
    def __repr__(self):
        return f"<Party {self.name}>"


class Ledger(Base):
    """Party ledger for financial tracking"""
    __tablename__ = "ledgers"
    
    id = Column(Integer, primary_key=True)
    party_id = Column(Integer, ForeignKey("parties.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    description = Column(String(255), nullable=False)
    debit_afg = Column(Float, default=0)
    credit_afg = Column(Float, default=0)
    debit_usd = Column(Float, default=0)
    credit_usd = Column(Float, default=0)
    exchange_rate_used = Column(Float, nullable=False)
    reference_type = Column(String(50))  # Sale, Purchase, Payment, Expense
    reference_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    party = relationship("Party", back_populates="ledger_entries")
    
    def __repr__(self):
        return f"<Ledger {self.party_id} - {self.date}>"


class Sale(Base):
    """Egg sales"""
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True)
    party_id = Column(Integer, ForeignKey("parties.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    quantity = Column(Integer, nullable=False)  # Number of eggs
    rate_afg = Column(Float, nullable=False)  # Price per egg in AFG
    rate_usd = Column(Float, nullable=False)  # Price per egg in USD
    total_afg = Column(Float, nullable=False)
    total_usd = Column(Float, nullable=False)
    exchange_rate_used = Column(Float, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    party = relationship("Party", back_populates="sales")
    
    def __repr__(self):
        return f"<Sale {self.party_id} - {self.date}>"


class Purchase(Base):
    """Raw material purchases"""
    __tablename__ = "purchases"
    
    id = Column(Integer, primary_key=True)
    party_id = Column(Integer, ForeignKey("parties.id"), nullable=False)
    material_id = Column(Integer, ForeignKey("raw_materials.id"))
    date = Column(DateTime, nullable=False)
    quantity = Column(Float, nullable=False)  # in kg
    rate_afg = Column(Float, nullable=False)  # Price per unit in AFG
    rate_usd = Column(Float, nullable=False)  # Price per unit in USD
    total_afg = Column(Float, nullable=False)
    total_usd = Column(Float, nullable=False)
    exchange_rate_used = Column(Float, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    party = relationship("Party", back_populates="purchases")
    
    def __repr__(self):
        return f"<Purchase {self.party_id} - {self.date}>"


class Payment(Base):
    """Payments to/from parties"""
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True)
    party_id = Column(Integer, ForeignKey("parties.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    amount_afg = Column(Float, nullable=False)
    amount_usd = Column(Float, nullable=False)
    payment_type = Column(String(50))  # Received, Paid
    payment_method = Column(String(50))  # Cash, Bank
    reference = Column(String(100))
    exchange_rate_used = Column(Float, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    party = relationship("Party", back_populates="payments")
    
    def __repr__(self):
        return f"<Payment {self.party_id} - {self.date}>"


class Expense(Base):
    """Farm expenses"""
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    party_id = Column(Integer, ForeignKey("parties.id"))  # Optional
    date = Column(DateTime, nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(Text)
    amount_afg = Column(Float, nullable=False)
    amount_usd = Column(Float, nullable=False)
    exchange_rate_used = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    farm = relationship("Farm", back_populates="expenses")
    party = relationship("Party", back_populates="expenses")
    
    def __repr__(self):
        return f"<Expense {self.farm_id} - {self.date}>"
