"""
Gerenciador de banco de dados MongoDB
"""
from pymongo import MongoClient
from typing import Dict, Any, List, Optional
from datetime import datetime
from .config import BLOCKCHAIN_CONFIG

class Database:
    def __init__(self):
        self.client = MongoClient(BLOCKCHAIN_CONFIG['MONGODB_URI'])
        self.db = self.client[BLOCKCHAIN_CONFIG['MONGODB_DATABASE']]
        self._init_collections()

    def _init_collections(self):
        """Inicializa as coleções do MongoDB"""
        self.wallets = self.db.wallets
        self.transactions = self.db.transactions
        self.blocks = self.db.blocks
        self.miners = self.db.miners
        self.developers = self.db.developers

    def insert_wallet(self, wallet_data: Dict[str, Any]) -> bool:
        try:
            self.wallets.insert_one(wallet_data)
            return True
        except Exception as e:
            print(f"Erro ao inserir wallet: {e}")
            return False

    def get_wallet(self, address: str) -> Optional[Dict[str, Any]]:
        return self.wallets.find_one({"address": address})

    def update_wallet_balance(self, address: str, new_balance: float) -> bool:
        try:
            self.wallets.update_one(
                {"address": address},
                {
                    "$set": {
                        "balance": new_balance,
                        "last_updated": datetime.utcnow()
                    }
                }
            )
            return True
        except Exception as e:
            print(f"Erro ao atualizar saldo: {e}")
            return False

    def insert_transaction(self, transaction_data: Dict[str, Any]) -> bool:
        try:
            self.transactions.insert_one(transaction_data)
            return True
        except Exception as e:
            print(f"Erro ao inserir transação: {e}")
            return False

    def insert_block(self, block_data: Dict[str, Any]) -> bool:
        try:
            self.blocks.insert_one(block_data)
            return True
        except Exception as e:
            print(f"Erro ao inserir bloco: {e}")
            return False

    def get_all_blocks(self) -> List[Dict[str, Any]]:
        return list(self.blocks.find().sort("index", 1))

    def get_pending_transactions(self) -> List[Dict[str, Any]]:
        return list(self.transactions.find({"block_hash": None}))

    def close(self):
        """Fecha a conexão com o MongoDB"""
        self.client.close()