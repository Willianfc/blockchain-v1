"""
Modelo de dados para Wallet
"""
from datetime import datetime

class WalletModel:
    @staticmethod
    def create(address: str, name: str):
        return {
            'address': address,
            'name': name,
            'balance': 0,
            'created_at': datetime.utcnow(),
            'last_updated': datetime.utcnow(),
            'transactions': []
        }

    @staticmethod
    def update_balance(wallet: dict, amount: float):
        wallet['balance'] += amount
        wallet['last_updated'] = datetime.utcnow()
        return wallet