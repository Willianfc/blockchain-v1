"""
Gerenciador de carteiras
"""
import random
import string
from .models.wallet import Wallet
from .database import Database

class WalletManager:
    def __init__(self):
        self.db = Database()

    def create_wallet(self, name: str) -> str:
        """Cria uma nova carteira"""
        # Gera um endereço único
        chars = string.ascii_letters + string.digits
        unique_id = ''.join(random.choice(chars) for _ in range(32))
        address = "CHAI" + unique_id

        wallet = Wallet(address, name)
        if self.db.insert_wallet(wallet.to_dict()):
            return address
        return ""

    def get_balance(self, address: str) -> float:
        """Obtém o saldo de uma carteira"""
        wallet = self.db.get_wallet(address)
        return wallet['balance'] if wallet else 0

    def get_transaction_history(self, address: str) -> list:
        """Obtém o histórico de transações de uma carteira"""
        return list(self.db.transactions.find({
            "$or": [
                {"from_address": address},
                {"to_address": address}
            ]
        }).sort("timestamp", -1))