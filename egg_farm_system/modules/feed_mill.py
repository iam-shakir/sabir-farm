"""
Feed manufacturing and management module
"""
from datetime import datetime
from database.models import (
    RawMaterial, FeedFormula, FeedFormulation, FeedBatch, FinishedFeed, FeedIssue, FeedType
)
from database.db import DatabaseManager
from utils.currency import CurrencyConverter
import logging

logger = logging.getLogger(__name__)

class RawMaterialManager:
    """Manage raw materials"""
    
    def __init__(self):
        self.session = DatabaseManager.get_session()
    
    def create_material(self, name, cost_afg, cost_usd, supplier_id=None, low_stock_alert=50):
        """Create raw material"""
        try:
            material = RawMaterial(
                name=name,
                cost_afg=cost_afg,
                cost_usd=cost_usd,
                supplier_id=supplier_id,
                low_stock_alert=low_stock_alert
            )
            self.session.add(material)
            self.session.commit()
            logger.info(f"Raw material created: {name}")
            return material
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error creating raw material: {e}")
            raise
    
    def get_all_materials(self):
        """Get all raw materials"""
        try:
            return self.session.query(RawMaterial).all()
        except Exception as e:
            logger.error(f"Error getting materials: {e}")
            return []
    
    def get_material_by_id(self, material_id):
        """Get material by ID"""
        try:
            return self.session.query(RawMaterial).filter(RawMaterial.id == material_id).first()
        except Exception as e:
            logger.error(f"Error getting material: {e}")
            return None
    
    def update_material_stock(self, material_id, quantity_change):
        """Update material stock"""
        try:
            material = self.get_material_by_id(material_id)
            if not material:
                raise ValueError(f"Material {material_id} not found")
            
            material.current_stock += quantity_change
            self.session.commit()
            logger.info(f"Material stock updated: {material_id}, change: {quantity_change}")
            return material
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error updating material stock: {e}")
            raise
    
    def get_low_stock_alerts(self):
        """Get materials below low stock threshold"""
        try:
            return self.session.query(RawMaterial).filter(
                RawMaterial.current_stock <= RawMaterial.low_stock_alert
            ).all()
        except Exception as e:
            logger.error(f"Error getting low stock alerts: {e}")
            return []


class FeedFormulaManager:
    """Manage feed formulas"""
    
    def __init__(self):
        self.session = DatabaseManager.get_session()
    
    def create_formula(self, name, feed_type):
        """Create feed formula"""
        try:
            formula = FeedFormula(
                name=name,
                feed_type=feed_type
            )
            self.session.add(formula)
            self.session.commit()
            logger.info(f"Feed formula created: {name}")
            return formula
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error creating formula: {e}")
            raise
    
    def add_ingredient(self, formula_id, material_id, percentage):
        """Add ingredient to formula"""
        try:
            formula = self.session.query(FeedFormula).filter(FeedFormula.id == formula_id).first()
            if not formula:
                raise ValueError(f"Formula {formula_id} not found")
            
            # Check total won't exceed 100%
            current_total = formula.get_total_percentage()
            if current_total + percentage > 100.01:  # Allow small rounding error
                raise ValueError(f"Total percentage would exceed 100%: {current_total + percentage}%")
            
            formulation = FeedFormulation(
                formula_id=formula_id,
                material_id=material_id,
                percentage=percentage
            )
            self.session.add(formulation)
            self.session.commit()
            logger.info(f"Ingredient added to formula {formula_id}")
            return formulation
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error adding ingredient: {e}")
            raise
    
    def get_formulas(self, active_only=True):
        """Get feed formulas"""
        try:
            query = self.session.query(FeedFormula)
            if active_only:
                query = query.filter(FeedFormula.is_active == True)
            return query.all()
        except Exception as e:
            logger.error(f"Error getting formulas: {e}")
            return []
    
    def get_formula_by_id(self, formula_id):
        """Get formula by ID"""
        try:
            return self.session.query(FeedFormula).filter(FeedFormula.id == formula_id).first()
        except Exception as e:
            logger.error(f"Error getting formula: {e}")
            return None
    
    def validate_formula(self, formula_id):
        """Validate formula (must equal 100%)"""
        try:
            formula = self.get_formula_by_id(formula_id)
            if not formula:
                return False, "Formula not found"
            
            total = formula.get_total_percentage()
            if abs(total - 100.0) < 0.01:  # Allow small rounding error
                return True, f"Valid (Total: {total:.2f}%)"
            else:
                return False, f"Invalid: Total is {total:.2f}%, must be 100%"
        except Exception as e:
            logger.error(f"Error validating formula: {e}")
            return False, str(e)


class FeedProductionManager:
    """Manage feed batch production"""
    
    def __init__(self):
        self.session = DatabaseManager.get_session()
        self.converter = CurrencyConverter()
    
    def produce_batch(self, formula_id, quantity_kg, exchange_rate, notes=None):
        """Produce a batch of feed"""
        try:
            formula = self.session.query(FeedFormula).filter(FeedFormula.id == formula_id).first()
            if not formula:
                raise ValueError(f"Formula {formula_id} not found")
            
            # Validate formula
            if abs(formula.get_total_percentage() - 100.0) > 0.01:
                raise ValueError("Formula is not valid (total percentage != 100%)")
            
            # Calculate cost
            cost_afg = 0
            for ingredient in formula.ingredients:
                material = ingredient.material
                amount_kg = (quantity_kg * ingredient.percentage) / 100
                cost_afg += amount_kg * material.cost_afg
                
                # Update raw material stock
                material.current_stock -= amount_kg
                self.session.add(material)
            
            # Convert to USD
            self.converter.set_exchange_rate(exchange_rate)
            cost_usd = self.converter.afg_to_usd(cost_afg)
            
            # Create batch record
            batch = FeedBatch(
                formula_id=formula_id,
                batch_date=datetime.utcnow(),
                quantity_kg=quantity_kg,
                cost_afg=cost_afg,
                cost_usd=cost_usd,
                exchange_rate_used=exchange_rate,
                notes=notes
            )
            self.session.add(batch)
            
            # Update finished feed stock
            finished_feed = self.session.query(FinishedFeed).filter(
                FinishedFeed.feed_type == formula.feed_type
            ).first()
            
            if not finished_feed:
                finished_feed = FinishedFeed(
                    feed_type=formula.feed_type,
                    current_stock=quantity_kg,
                    cost_per_kg_afg=cost_afg / quantity_kg if quantity_kg > 0 else 0,
                    cost_per_kg_usd=cost_usd / quantity_kg if quantity_kg > 0 else 0
                )
                self.session.add(finished_feed)
            else:
                # Update weighted average cost
                old_value = finished_feed.current_stock * finished_feed.cost_per_kg_afg
                new_value = quantity_kg * (cost_afg / quantity_kg)
                total_kg = finished_feed.current_stock + quantity_kg
                
                finished_feed.cost_per_kg_afg = (old_value + new_value) / total_kg if total_kg > 0 else 0
                finished_feed.cost_per_kg_usd = self.converter.afg_to_usd(finished_feed.cost_per_kg_afg)
                finished_feed.current_stock = total_kg
                self.session.add(finished_feed)
            
            self.session.commit()
            logger.info(f"Feed batch produced: {quantity_kg}kg from formula {formula_id}")
            return batch
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error producing batch: {e}")
            raise


class FeedIssueManager:
    """Manage feed issuance to sheds"""
    
    def __init__(self):
        self.session = DatabaseManager.get_session()
    
    def issue_feed(self, shed_id, feed_id, quantity_kg, date, notes=None):
        """Issue feed to a shed"""
        try:
            feed = self.session.query(FinishedFeed).filter(FinishedFeed.id == feed_id).first()
            if not feed:
                raise ValueError(f"Feed {feed_id} not found")
            
            if feed.current_stock < quantity_kg:
                raise ValueError(f"Insufficient stock. Available: {feed.current_stock}kg")
            
            cost_afg = quantity_kg * feed.cost_per_kg_afg
            cost_usd = quantity_kg * feed.cost_per_kg_usd
            
            issue = FeedIssue(
                shed_id=shed_id,
                feed_id=feed_id,
                date=date,
                quantity_kg=quantity_kg,
                cost_afg=cost_afg,
                cost_usd=cost_usd,
                notes=notes
            )
            
            feed.current_stock -= quantity_kg
            self.session.add(issue)
            self.session.commit()
            
            logger.info(f"Feed issued: {quantity_kg}kg to shed {shed_id}")
            return issue
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error issuing feed: {e}")
            raise
    
    def get_shed_feed_issues(self, shed_id, start_date, end_date):
        """Get feed issues for a shed in date range"""
        try:
            return self.session.query(FeedIssue).filter(
                FeedIssue.shed_id == shed_id,
                FeedIssue.date >= start_date,
                FeedIssue.date <= end_date
            ).all()
        except Exception as e:
            logger.error(f"Error getting feed issues: {e}")
            return []
