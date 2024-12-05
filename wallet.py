import hashlib
import random
import string
import sqlite3

class Wallet:
    def __init__(self):
        self.conn = sqlite3.connect('corehiveai.db')
        self.cursor = self.conn.cursor()

    def generate_address(self, name: str) -> str:
        # Gera um endereço único de 32 caracteres
        chars = string.ascii_letters + string.digits
        unique_id = ''.join(random.choice(chars) for _ in range(32))
        address = "CHAI" + unique_id  # Prefixo CHAI para CoreHiveAi

        self.cursor.execute(
            "INSERT INTO wallets (address, balance, name) VALUES (?, ?, ?)",
            (address, 0, name)
        )
        self.conn.commit()
        return address

    def get_balance(self, address: str) -> float:
        self.cursor.execute(
            "SELECT balance FROM wallets WHERE address = ?",
            (address,)
        )
        result = self.cursor.fetchone()
        return result[0] if result else 0

if __name__ == "__main__":
    wallet = Wallet()
    print("Sistema de Wallet CoreHiveAi iniciado com sucesso!")