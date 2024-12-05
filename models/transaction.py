"""
Modelo de dados para transações
"""
from datetime import datetime
from typing import Dict, Any

class Transaction:
    def __init__(self, from_address: str, to_address: str, amount: float):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.timestamp = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'from_address': self.from_address,
            'to_address': self.to_address,
            'amount': self.amount,
            'timestamp': self.timestamp
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Transaction':
        transaction = Transaction(
            data['from_address'],
            data['to_address'],
            data['amount']
        )
        transaction.timestamp = data['timestamp']
        return transaction