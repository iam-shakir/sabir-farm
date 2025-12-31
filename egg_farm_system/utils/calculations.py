"""
Calculation utilities for egg farm system
"""
from datetime import datetime, timedelta

class EggCalculations:
    """Egg production calculations"""
    
    @staticmethod
    def egg_production_percentage(total_eggs, live_bird_count, days=1):
        """Calculate egg production percentage"""
        if live_bird_count == 0 or days == 0:
            return 0
        return (total_eggs / (live_bird_count * days)) * 100
    
    @staticmethod
    def eggs_per_bird(total_eggs, live_bird_count):
        """Calculate eggs per bird"""
        if live_bird_count == 0:
            return 0
        return total_eggs / live_bird_count
    
    @staticmethod
    def usable_egg_percentage(usable_eggs, total_eggs):
        """Calculate percentage of usable eggs"""
        if total_eggs == 0:
            return 0
        return (usable_eggs / total_eggs) * 100


class FeedCalculations:
    """Feed-related calculations"""
    
    @staticmethod
    def cost_per_egg(total_feed_cost, total_eggs):
        """Calculate feed cost per egg"""
        if total_eggs == 0:
            return 0
        return total_feed_cost / total_eggs
    
    @staticmethod
    def feed_efficiency_ratio(total_feed_kg, total_eggs):
        """Calculate feed efficiency (kg feed per 1000 eggs)"""
        if total_eggs == 0:
            return 0
        return (total_feed_kg / total_eggs) * 1000
    
    @staticmethod
    def daily_feed_requirement(live_bird_count, daily_consumption_per_bird_kg=0.12):
        """Calculate daily feed requirement"""
        return live_bird_count * daily_consumption_per_bird_kg


class FinancialCalculations:
    """Financial calculations"""
    
    @staticmethod
    def calculate_profit(revenue, expenses):
        """Calculate profit"""
        return revenue - expenses
    
    @staticmethod
    def calculate_profit_percentage(profit, revenue):
        """Calculate profit percentage"""
        if revenue == 0:
            return 0
        return (profit / revenue) * 100
    
    @staticmethod
    def calculate_margin(profit, revenue):
        """Calculate profit margin"""
        if revenue == 0:
            return 0
        return (profit / revenue) * 100
    
    @staticmethod
    def weighted_average_cost(purchases):
        """
        Calculate weighted average cost from purchases.
        purchases: list of dicts with 'quantity' and 'unit_cost'
        """
        if not purchases:
            return 0
        
        total_qty = sum(p['quantity'] for p in purchases)
        if total_qty == 0:
            return 0
        
        total_cost = sum(p['quantity'] * p['unit_cost'] for p in purchases)
        return total_cost / total_qty


class MortalityCalculations:
    """Mortality and bird count calculations"""
    
    @staticmethod
    def live_bird_count(initial_count, cumulative_mortality):
        """Calculate live bird count"""
        return max(0, initial_count - cumulative_mortality)
    
    @staticmethod
    def mortality_percentage(initial_count, cumulative_mortality):
        """Calculate mortality percentage"""
        if initial_count == 0:
            return 0
        return (cumulative_mortality / initial_count) * 100
    
    @staticmethod
    def flock_age_days(start_date, end_date=None):
        """Calculate flock age in days"""
        if end_date is None:
            end_date = datetime.utcnow()
        return (end_date - start_date).days
    
    @staticmethod
    def flock_age_weeks(start_date, end_date=None):
        """Calculate flock age in weeks"""
        days = MortalityCalculations.flock_age_days(start_date, end_date)
        return days / 7


class InventoryCalculations:
    """Inventory valuation and calculations"""
    
    @staticmethod
    def inventory_value(quantity, unit_cost):
        """Calculate inventory value"""
        return quantity * unit_cost
    
    @staticmethod
    def average_cost_method(opening_stock, opening_cost, purchases):
        """
        Calculate average cost using weighted average method.
        Returns: average cost per unit
        """
        total_qty = opening_stock + sum(p['quantity'] for p in purchases)
        if total_qty == 0:
            return 0
        
        total_cost = (opening_stock * opening_cost) + sum(p['quantity'] * p['unit_cost'] for p in purchases)
        return total_cost / total_qty
