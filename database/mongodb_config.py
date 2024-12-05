"""
Configuração do MongoDB
"""
from pymongo import MongoClient
from ..config import BLOCKCHAIN_CONFIG

def get_database():
    client = MongoClient(BLOCKCHAIN_CONFIG['MONGODB_URI'])
    return client[BLOCKCHAIN_CONFIG['MONGODB_DATABASE']]

# Coleções
def get_collections(db):
    return {
        'wallets': db.wallets,
        'transactions': db.transactions,
        'blocks': db.blocks,
        'miners': db.miners,
        'developers': db.developers,
        'compute_tasks': db.compute_tasks
    }