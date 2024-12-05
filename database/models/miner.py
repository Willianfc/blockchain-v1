"""
Modelo de dados para Minerador
"""
from datetime import datetime

class MinerModel:
    @staticmethod
    def create(wallet_address: str):
        return {
            'wallet_address': wallet_address,
            'total_mined': 0,
            'active': True,
            'last_mining': None,
            'rewards': 0,
            'hash_power': 0,
            'joined_at': datetime.utcnow()
        }

    @staticmethod
    def update_mining(miner: dict, reward: float):
        miner['total_mined'] += 1
        miner['rewards'] += reward
        miner['last_mining'] = datetime.utcnow()
        return miner