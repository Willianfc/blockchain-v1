"""
Modelo de dados para carteiras
"""
from datetime import datetime
from typing import Dict, Any

class Wallet:
    def __init__(self, address: str, name: str):
        self.address = address
        self.name = name
        self.balance = 0
        self.created_at = datetime.utcnow()
        self.last_updated = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'address': self.address,
            'name': self.name,
            'balance': self.balance,
            'created_at': self.created_at,
            'last_updated': self.last_updated
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Wallet':
        wallet = Wallet(data['address'], data['name'])
        wallet.balance = data['balance']
        wallet.created_at = data['created_at']
        wallet.last_updated = data['last_updated']
        return wallet