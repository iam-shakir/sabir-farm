"""
Inventory management module
"""
from database.models import RawMaterial, FinishedFeed
from database.db import DatabaseManager
import logging

logger = logging.getLogger(__name__)

class InventoryManager:
    """Manage inventory operations"""
    
    def __init__(self):
        self.session = DatabaseManager.get_session()
    
    def get_raw_materials_inventory(self):
        """Get all raw materials with inventory"""
        try:
            materials = self.session.query(RawMaterial).all()
            inventory = []
            
            for material in materials:
                inventory_value_afg = material.current_stock * material.cost_afg
                inventory_value_usd = material.current_stock * material.cost_usd
                is_low = material.current_stock <= material.low_stock_alert
                
                inventory.append({
                    'id': material.id,
                    'name': material.name,
                    'stock': material.current_stock,
                    'unit': material.unit,
                    'cost_afg': material.cost_afg,
                    'cost_usd': material.cost_usd,
                    'inventory_value_afg': inventory_value_afg,
                    'inventory_value_usd': inventory_value_usd,
                    'low_stock_alert': material.low_stock_alert,
                    'is_low': is_low,
                    'supplier_id': material.supplier_id
                })
            
            return inventory
        except Exception as e:
            logger.error(f"Error getting raw materials inventory: {e}")
            return []
    
    def get_finished_feed_inventory(self):
        """Get finished feed inventory"""
        try:
            feeds = self.session.query(FinishedFeed).all()
            inventory = []
            
            for feed in feeds:
                inventory_value_afg = feed.current_stock * feed.cost_per_kg_afg
                inventory_value_usd = feed.current_stock * feed.cost_per_kg_usd
                is_low = feed.current_stock <= feed.low_stock_alert
                
                inventory.append({
                    'id': feed.id,
                    'feed_type': feed.feed_type.value,
                    'stock_kg': feed.current_stock,
                    'cost_per_kg_afg': feed.cost_per_kg_afg,
                    'cost_per_kg_usd': feed.cost_per_kg_usd,
                    'inventory_value_afg': inventory_value_afg,
                    'inventory_value_usd': inventory_value_usd,
                    'low_stock_alert': feed.low_stock_alert,
                    'is_low': is_low
                })
            
            return inventory
        except Exception as e:
            logger.error(f"Error getting finished feed inventory: {e}")
            return []
    
    def get_total_inventory_value(self):
        """Get total inventory value"""
        try:
            total_afg = 0
            total_usd = 0
            
            # Raw materials
            materials = self.session.query(RawMaterial).all()
            for material in materials:
                total_afg += material.current_stock * material.cost_afg
                total_usd += material.current_stock * material.cost_usd
            
            # Finished feed
            feeds = self.session.query(FinishedFeed).all()
            for feed in feeds:
                total_afg += feed.current_stock * feed.cost_per_kg_afg
                total_usd += feed.current_stock * feed.cost_per_kg_usd
            
            return {
                'total_afg': total_afg,
                'total_usd': total_usd
            }
        except Exception as e:
            logger.error(f"Error calculating inventory value: {e}")
            return {'total_afg': 0, 'total_usd': 0}
    
    def get_low_stock_alerts(self):
        """Get all low stock alerts"""
        try:
            alerts = []
            
            # Raw materials
            low_materials = self.session.query(RawMaterial).filter(
                RawMaterial.current_stock <= RawMaterial.low_stock_alert
            ).all()
            
            for material in low_materials:
                alerts.append({
                    'type': 'Raw Material',
                    'name': material.name,
                    'stock': material.current_stock,
                    'alert_level': material.low_stock_alert,
                    'unit': material.unit
                })
            
            # Finished feed
            low_feeds = self.session.query(FinishedFeed).filter(
                FinishedFeed.current_stock <= FinishedFeed.low_stock_alert
            ).all()
            
            for feed in low_feeds:
                alerts.append({
                    'type': 'Finished Feed',
                    'name': feed.feed_type.value,
                    'stock': feed.current_stock,
                    'alert_level': feed.low_stock_alert,
                    'unit': 'kg'
                })
            
            return alerts
        except Exception as e:
            logger.error(f"Error getting low stock alerts: {e}")
            return []
    
    def close_session(self):
        """Close database session"""
        if self.session:
            self.session.close()
