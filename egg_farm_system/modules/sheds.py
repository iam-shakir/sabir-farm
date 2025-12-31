"""
Shed management module
"""
from database.models import Shed
from database.db import DatabaseManager
import logging

logger = logging.getLogger(__name__)

class ShedManager:
    """Manage shed operations"""
    
    def __init__(self):
        self.session = DatabaseManager.get_session()
    
    def create_shed(self, farm_id, name, capacity):
        """Create a new shed"""
        try:
            shed = Shed(farm_id=farm_id, name=name, capacity=capacity)
            self.session.add(shed)
            self.session.commit()
            logger.info(f"Shed created: {name} in farm {farm_id}")
            return shed
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error creating shed: {e}")
            raise
    
    def get_sheds_by_farm(self, farm_id):
        """Get all sheds for a farm"""
        try:
            return self.session.query(Shed).filter(Shed.farm_id == farm_id).all()
        except Exception as e:
            logger.error(f"Error getting sheds: {e}")
            return []
    
    def get_shed_by_id(self, shed_id):
        """Get shed by ID"""
        try:
            return self.session.query(Shed).filter(Shed.id == shed_id).first()
        except Exception as e:
            logger.error(f"Error getting shed: {e}")
            return None
    
    def update_shed(self, shed_id, name=None, capacity=None):
        """Update shed details"""
        try:
            shed = self.get_shed_by_id(shed_id)
            if not shed:
                raise ValueError(f"Shed {shed_id} not found")
            
            if name:
                shed.name = name
            if capacity:
                shed.capacity = capacity
            
            self.session.commit()
            logger.info(f"Shed updated: {shed_id}")
            return shed
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error updating shed: {e}")
            raise
    
    def delete_shed(self, shed_id):
        """Delete shed and related data"""
        try:
            shed = self.get_shed_by_id(shed_id)
            if not shed:
                raise ValueError(f"Shed {shed_id} not found")
            
            self.session.delete(shed)
            self.session.commit()
            logger.info(f"Shed deleted: {shed_id}")
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error deleting shed: {e}")
            raise
    
    def get_shed_summary(self, shed_id):
        """Get shed summary with statistics"""
        try:
            shed = self.get_shed_by_id(shed_id)
            if not shed:
                return None
            
            total_flocks = len(shed.flocks)
            active_flocks = len([f for f in shed.flocks])
            total_birds = sum(f.get_live_count() for f in shed.flocks)
            
            return {
                'shed': shed,
                'total_flocks': total_flocks,
                'active_flocks': active_flocks,
                'total_birds': total_birds,
                'available_capacity': shed.capacity - total_birds,
                'capacity_utilization': (total_birds / shed.capacity * 100) if shed.capacity > 0 else 0
            }
        except Exception as e:
            logger.error(f"Error getting shed summary: {e}")
            return None
    
    def close_session(self):
        """Close database session"""
        if self.session:
            self.session.close()
