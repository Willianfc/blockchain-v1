import hashlib
import time
from typing import List
import sqlite3
import json

class Block:
    def __init__(self, index: int, transactions: List[dict], timestamp: float, previous_hash: str, nonce: int = 0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = json.dumps({
            "index": self.index,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class CoreHiveAi:
    def __init__(self):
        self.chain = []
        self.difficulty = 4
        self.pending_transactions = []
        self.mining_reward = 50
        self.total_supply = 60_000_000
        self.mined_tokens = 0
        self.initialize_db()
        self.create_genesis_block()

    def initialize_db(self):
        self.conn = sqlite3.connect('corehiveai.db')
        self.cursor = self.conn.cursor()
        
        # Create tables
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS wallets (
            address TEXT PRIMARY KEY,
            balance REAL,
            name TEXT
        )''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            from_address TEXT,
            to_address TEXT,
            amount REAL,
            timestamp REAL
        )''')
        
        self.conn.commit()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def mine_pending_transactions(self, miner_address: str):
        if self.mined_tokens >= self.total_supply:
            return False, "Total supply reached"

        block = Block(
            len(self.chain),
            self.pending_transactions,
            time.time(),
            self.get_latest_block().hash
        )

        while block.hash[:self.difficulty] != "0" * self.difficulty:
            block.nonce += 1
            block.hash = block.calculate_hash()

        print(f"Block mined! Hash: {block.hash}")
        self.chain.append(block)

        # Reward the miner
        reward_amount = min(self.mining_reward, self.total_supply - self.mined_tokens)
        self.mined_tokens += reward_amount
        self.add_transaction("System", miner_address, reward_amount)

        self.pending_transactions = []
        return True, "Block mined successfully"

    def add_transaction(self, from_address: str, to_address: str, amount: float):
        self.cursor.execute(
            "INSERT INTO transactions (from_address, to_address, amount, timestamp) VALUES (?, ?, ?, ?)",
            (from_address, to_address, amount, time.time())
        )
        self.conn.commit()
        self.pending_transactions.append({
            "from": from_address,
            "to": to_address,
            "amount": amount
        })

    def get_balance(self, address: str) -> float:
        balance = 0
        self.cursor.execute(
            "SELECT SUM(amount) FROM transactions WHERE to_address = ?",
            (address,)
        )
        incoming = self.cursor.fetchone()[0] or 0
        
        self.cursor.execute(
            "SELECT SUM(amount) FROM transactions WHERE from_address = ?",
            (address,)
        )
        outgoing = self.cursor.fetchone()[0] or 0
        
        return incoming - outgoing

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

if __name__ == "__main__":
    blockchain = CoreHiveAi()
    print("CoreHiveAi Blockchain iniciada com sucesso!")