"""
Modelo de dados para Transação
"""
from datetime import datetime

class TransactionModel:
    @staticmethod
    def create(from_address: str, to_address: str, amount: float):
        return {
            'from_address': from_address,
            'to_address': to_address,
            'amount': amount,
            'timestamp': datetime.utcnow(),
            'status': 'pending',
            'block_hash': None
        }