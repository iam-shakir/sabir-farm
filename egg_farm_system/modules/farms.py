"""
Farm management module
"""
from database.models import Farm
from database.db import DatabaseManager
import logging

logger = logging.getLogger(__name__)

class FarmManager:
    """Manage farm operations"""
    
    def __init__(self):
        self.session = DatabaseManager.get_session()
    
    def create_farm(self, name, location=None):
        """Create a new farm"""
        try:
            farm = Farm(name=name, location=location)
            self.session.add(farm)
            self.session.commit()
            logger.info(f"Farm created: {name}")
            return farm
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error creating farm: {e}")
            raise
    
    def get_all_farms(self):
        """Get all farms"""
        try:
            return self.session.query(Farm).all()
        except Exception as e:
            logger.error(f"Error getting farms: {e}")
            return []
    
    def get_farm_by_id(self, farm_id):
        """Get farm by ID"""
        try:
            return self.session.query(Farm).filter(Farm.id == farm_id).first()
        except Exception as e:
            logger.error(f"Error getting farm: {e}")
            return None
    
    def get_farm_by_name(self, name):
        """Get farm by name"""
        try:
            return self.session.query(Farm).filter(Farm.name == name).first()
        except Exception as e:
            logger.error(f"Error getting farm: {e}")
            return None
    
    def update_farm(self, farm_id, name=None, location=None):
        """Update farm details"""
        try:
            farm = self.get_farm_by_id(farm_id)
            if not farm:
                raise ValueError(f"Farm {farm_id} not found")
            
            if name:
                farm.name = name
            if location:
                farm.location = location
            
            self.session.commit()
            logger.info(f"Farm updated: {farm_id}")
            return farm
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error updating farm: {e}")
            raise
    
    def delete_farm(self, farm_id):
        """Delete farm and related data"""
        try:
            farm = self.get_farm_by_id(farm_id)
            if not farm:
                raise ValueError(f"Farm {farm_id} not found")
            
            self.session.delete(farm)
            self.session.commit()
            logger.info(f"Farm deleted: {farm_id}")
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error deleting farm: {e}")
            raise
    
    def get_farm_summary(self, farm_id):
        """Get farm summary with stats"""
        try:
            farm = self.get_farm_by_id(farm_id)
            if not farm:
                return None
            
            total_sheds = len(farm.sheds)
            total_capacity = sum(shed.capacity for shed in farm.sheds)
            total_expenses = sum(exp.amount_afg for exp in farm.expenses)
            
            return {
                'farm': farm,
                'total_sheds': total_sheds,
                'total_capacity': total_capacity,
                'total_expenses': total_expenses,
                'sheds': farm.sheds,
                'expenses': farm.expenses
            }
        except Exception as e:
            logger.error(f"Error getting farm summary: {e}")
            return None
    
    def close_session(self):
        """Close database session"""
        if self.session:
            self.session.close()
