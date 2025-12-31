"""
Party management module (unified customer/supplier)
"""
from database.models import Party
from database.db import DatabaseManager
import logging

logger = logging.getLogger(__name__)

class PartyManager:
    """Manage parties (customers and suppliers)"""
    
    def __init__(self):
        self.session = DatabaseManager.get_session()
    
    def create_party(self, name, phone=None, address=None, notes=None):
        """Create a new party"""
        try:
            party = Party(
                name=name,
                phone=phone,
                address=address,
                notes=notes
            )
            self.session.add(party)
            self.session.commit()
            logger.info(f"Party created: {name}")
            return party
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error creating party: {e}")
            raise
    
    def get_all_parties(self):
        """Get all parties"""
        try:
            return self.session.query(Party).order_by(Party.name).all()
        except Exception as e:
            logger.error(f"Error getting parties: {e}")
            return []
    
    def get_party_by_id(self, party_id):
        """Get party by ID"""
        try:
            return self.session.query(Party).filter(Party.id == party_id).first()
        except Exception as e:
            logger.error(f"Error getting party: {e}")
            return None
    
    def get_party_by_name(self, name):
        """Get party by name"""
        try:
            return self.session.query(Party).filter(Party.name == name).first()
        except Exception as e:
            logger.error(f"Error getting party: {e}")
            return None
    
    def update_party(self, party_id, name=None, phone=None, address=None, notes=None):
        """Update party details"""
        try:
            party = self.get_party_by_id(party_id)
            if not party:
                raise ValueError(f"Party {party_id} not found")
            
            if name:
                party.name = name
            if phone:
                party.phone = phone
            if address:
                party.address = address
            if notes is not None:
                party.notes = notes
            
            self.session.commit()
            logger.info(f"Party updated: {party_id}")
            return party
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error updating party: {e}")
            raise
    
    def delete_party(self, party_id):
        """Delete party and related data"""
        try:
            party = self.get_party_by_id(party_id)
            if not party:
                raise ValueError(f"Party {party_id} not found")
            
            self.session.delete(party)
            self.session.commit()
            logger.info(f"Party deleted: {party_id}")
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error deleting party: {e}")
            raise
    
    def get_party_statement(self, party_id):
        """Get party ledger statement with balance"""
        try:
            party = self.get_party_by_id(party_id)
            if not party:
                return None
            
            balance_afg = party.get_balance("AFG")
            balance_usd = party.get_balance("USD")
            
            return {
                'party': party,
                'balance_afg': balance_afg,
                'balance_usd': balance_usd,
                'owes_us': balance_afg > 0,
                'we_owe': balance_afg < 0,
                'ledger_entries': sorted(party.ledger_entries, key=lambda x: x.date)
            }
        except Exception as e:
            logger.error(f"Error getting party statement: {e}")
            return None
    
    def close_session(self):
        """Close database session"""
        if self.session:
            self.session.close()
