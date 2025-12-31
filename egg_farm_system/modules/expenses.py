"""
Expenses and payments module
"""
from datetime import datetime
from database.models import Expense, Payment
from database.db import DatabaseManager
from modules.ledger import LedgerManager
import logging

logger = logging.getLogger(__name__)

class ExpenseManager:
    """Manage farm expenses"""
    
    def __init__(self):
        self.session = DatabaseManager.get_session()
        self.ledger_manager = LedgerManager()
    
    def record_expense(self, farm_id, category, amount_afg, amount_usd, 
                      party_id=None, exchange_rate_used=78.0, date=None, description=None):
        """Record farm expense"""
        try:
            if date is None:
                date = datetime.utcnow()
            
            expense = Expense(
                farm_id=farm_id,
                party_id=party_id,
                date=date,
                category=category,
                description=description,
                amount_afg=amount_afg,
                amount_usd=amount_usd,
                exchange_rate_used=exchange_rate_used
            )
            self.session.add(expense)
            self.session.flush()
            
            # Post to ledger if party is linked
            if party_id:
                self.ledger_manager.post_entry(
                    party_id=party_id,
                    date=date,
                    description=f"Expense: {category} - {description or ''}",
                    credit_afg=amount_afg,
                    credit_usd=amount_usd,
                    exchange_rate_used=exchange_rate_used,
                    reference_type="Expense",
                    reference_id=expense.id
                )
            
            self.session.commit()
            logger.info(f"Expense recorded: {category} - Afs {amount_afg}")
            return expense
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error recording expense: {e}")
            raise
    
    def get_expenses(self, farm_id=None, start_date=None, end_date=None, category=None):
        """Get expense records"""
        try:
            query = self.session.query(Expense)
            
            if farm_id:
                query = query.filter(Expense.farm_id == farm_id)
            
            if start_date:
                query = query.filter(Expense.date >= start_date)
            
            if end_date:
                query = query.filter(Expense.date <= end_date)
            
            if category:
                query = query.filter(Expense.category == category)
            
            return query.order_by(Expense.date.desc()).all()
        except Exception as e:
            logger.error(f"Error getting expenses: {e}")
            return []
    
    def get_expenses_summary(self, farm_id=None, start_date=None, end_date=None):
        """Get expenses summary"""
        try:
            expenses = self.get_expenses(farm_id, start_date, end_date)
            
            total_afg = sum(e.amount_afg for e in expenses)
            total_usd = sum(e.amount_usd for e in expenses)
            
            by_category = {}
            for expense in expenses:
                if expense.category not in by_category:
                    by_category[expense.category] = {'count': 0, 'afg': 0, 'usd': 0}
                
                by_category[expense.category]['count'] += 1
                by_category[expense.category]['afg'] += expense.amount_afg
                by_category[expense.category]['usd'] += expense.amount_usd
            
            return {
                'total_expenses': len(expenses),
                'total_afg': total_afg,
                'total_usd': total_usd,
                'by_category': by_category
            }
        except Exception as e:
            logger.error(f"Error getting expenses summary: {e}")
            return None


class PaymentManager:
    """Manage payments to/from parties"""
    
    def __init__(self):
        self.session = DatabaseManager.get_session()
        self.ledger_manager = LedgerManager()
    
    def record_payment(self, party_id, amount_afg, amount_usd, payment_type,
                      payment_method="Cash", reference=None, exchange_rate_used=78.0, 
                      date=None, notes=None):
        """Record payment and post to ledger"""
        try:
            if date is None:
                date = datetime.utcnow()
            
            if payment_type not in ["Received", "Paid"]:
                raise ValueError("Payment type must be 'Received' or 'Paid'")
            
            payment = Payment(
                party_id=party_id,
                date=date,
                amount_afg=amount_afg,
                amount_usd=amount_usd,
                payment_type=payment_type,
                payment_method=payment_method,
                reference=reference,
                exchange_rate_used=exchange_rate_used,
                notes=notes
            )
            self.session.add(payment)
            self.session.flush()
            
            # Post to ledger
            if payment_type == "Received":
                # Debit cash, Credit party
                self.ledger_manager.post_entry(
                    party_id=party_id,
                    date=date,
                    description=f"Payment received: {reference or 'Cash'}",
                    credit_afg=amount_afg,
                    credit_usd=amount_usd,
                    exchange_rate_used=exchange_rate_used,
                    reference_type="Payment",
                    reference_id=payment.id
                )
            else:  # Paid
                # Debit party, Credit cash
                self.ledger_manager.post_entry(
                    party_id=party_id,
                    date=date,
                    description=f"Payment paid: {reference or 'Cash'}",
                    debit_afg=amount_afg,
                    debit_usd=amount_usd,
                    exchange_rate_used=exchange_rate_used,
                    reference_type="Payment",
                    reference_id=payment.id
                )
            
            self.session.commit()
            logger.info(f"Payment recorded: {payment_type} Afs {amount_afg} from/to party {party_id}")
            return payment
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error recording payment: {e}")
            raise
    
    def get_payments(self, party_id=None, start_date=None, end_date=None):
        """Get payment records"""
        try:
            query = self.session.query(Payment)
            
            if party_id:
                query = query.filter(Payment.party_id == party_id)
            
            if start_date:
                query = query.filter(Payment.date >= start_date)
            
            if end_date:
                query = query.filter(Payment.date <= end_date)
            
            return query.order_by(Payment.date.desc()).all()
        except Exception as e:
            logger.error(f"Error getting payments: {e}")
            return []
    
    def close_session(self):
        """Close database session"""
        if self.session:
            self.session.close()
