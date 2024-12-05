"""
Implementação do bloco da blockchain
"""
import hashlib
import json
import time
from typing import List, Dict, Any

class Block:
    def __init__(self, index: int, transactions: List[Dict[str, Any]], 
                 timestamp: float, previous_hash: str, nonce: int = 0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """Calcula o hash do bloco"""
        block_string = json.dumps({
            "index": self.index,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        """Converte o bloco para dicionário"""
        return {
            "index": self.index,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Block':
        """Cria um bloco a partir de um dicionário"""
        block = Block(
            data['index'],
            data['transactions'],
            data['timestamp'],
            data['previous_hash'],
            data['nonce']
        )
        block.hash = data['hash']
        return block