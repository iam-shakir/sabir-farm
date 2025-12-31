"""
Currency utilities and conversion functions
"""
from config import BASE_CURRENCY, SECONDARY_CURRENCY, DEFAULT_EXCHANGE_RATE

class CurrencyConverter:
    """Handle currency conversions"""
    
    def __init__(self, exchange_rate=DEFAULT_EXCHANGE_RATE):
        """
        Initialize converter with exchange rate.
        Default: 1 USD = 78 AFG
        """
        self.exchange_rate = exchange_rate
    
    def afg_to_usd(self, amount_afg):
        """Convert AFG to USD"""
        if self.exchange_rate == 0:
            return 0
        return amount_afg / self.exchange_rate
    
    def usd_to_afg(self, amount_usd):
        """Convert USD to AFG"""
        return amount_usd * self.exchange_rate
    
    def set_exchange_rate(self, rate):
        """Update exchange rate"""
        if rate > 0:
            self.exchange_rate = rate
        else:
            raise ValueError("Exchange rate must be positive")
    
    def format_amount(self, amount, currency="AFG", decimal_places=2):
        """Format amount with currency"""
        formatted = f"{amount:,.{decimal_places}f}"
        symbol = "Afs" if currency == "AFG" else "$"
        return f"{symbol} {formatted}"

def calculate_weighted_average_cost(transactions):
    """
    Calculate weighted average cost from list of transactions.
    Each transaction should have 'quantity' and 'unit_cost' keys.
    """
    if not transactions:
        return 0
    
    total_qty = sum(t['quantity'] for t in transactions)
    if total_qty == 0:
        return 0
    
    total_value = sum(t['quantity'] * t['unit_cost'] for t in transactions)
    return total_value / total_qty
