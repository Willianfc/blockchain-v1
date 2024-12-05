"""
Gerenciador de carteiras
"""
import hashlib
import random
import string
from ..database.manager import DatabaseManager
from ..config import BLOCKCHAIN_CONFIG

class WalletManager:
    def __init__(self):
        self.db = DatabaseManager()

    def create_wallet(self, name: str) -> str:
        """Cria uma nova carteira"""
        # Gera um endereço único
        chars = string.ascii_letters + string.digits
        unique_id = ''.join(random.choice(chars) for _ in range(32))
        address = "CHAI" + unique_id

        if self.db.insert_wallet(address, name):
            return address
        return ""

    def get_balance(self, address: str) -> float:
        """Obtém o saldo de uma carteira"""
        result = self.db.fetch_one(
            "SELECT balance FROM wallets WHERE address = ?",
            (address,)
        )
        return result[0] if result else 0

    def get_transaction_history(self, address: str) -> list:
        """Obtém o histórico de transações de uma carteira"""
        query = """
            SELECT * FROM transactions 
            WHERE from_address = ? OR to_address = ?
            ORDER BY timestamp DESC
        """
        return self.db.fetch_all(query, (address, address))