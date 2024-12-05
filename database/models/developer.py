"""
Modelo de dados para Desenvolvedor
"""
from datetime import datetime

class DeveloperModel:
    @staticmethod
    def create(wallet_address: str, api_key: str):
        return {
            'wallet_address': wallet_address,
            'api_key': api_key,
            'active': True,
            'compute_usage': 0,
            'tasks_submitted': 0,
            'joined_at': datetime.utcnow(),
            'last_activity': datetime.utcnow()
        }