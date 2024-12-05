"""
Modelo de dados para Bloco
"""
from datetime import datetime

class BlockModel:
    @staticmethod
    def create(hash: str, previous_hash: str, transactions: list, nonce: int, difficulty: int):
        return {
            'hash': hash,
            'previous_hash': previous_hash,
            'transactions': transactions,
            'nonce': nonce,
            'difficulty': difficulty,
            'timestamp': datetime.utcnow(),
            'size': len(transactions)
        }