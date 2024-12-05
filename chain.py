"""
Implementação da blockchain
"""
from typing import List, Dict, Any, Tuple
import time
from .models.block import Block
from .models.transaction import Transaction
from .database import Database
from .config import BLOCKCHAIN_CONFIG

class Blockchain:
    def __init__(self):
        self.db = Database()
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.difficulty = BLOCKCHAIN_CONFIG['INITIAL_DIFFICULTY']
        self.mining_reward = BLOCKCHAIN_CONFIG['MINING_REWARD']
        self.total_supply = BLOCKCHAIN_CONFIG['TOTAL_SUPPLY']
        self.mined_tokens = 0
        self._load_chain()

    def _load_chain(self):
        """Carrega a blockchain do banco de dados"""
        blocks = self.db.get_all_blocks()
        if not blocks:
            self.create_genesis_block()
        else:
            for block_data in blocks:
                block = Block.from_dict(block_data)
                self.chain.append(block)

    def create_genesis_block(self):
        """Cria o bloco gênesis"""
        genesis_block = Block(0, [], time.time(), "0")
        self.chain.append(genesis_block)
        self.db.insert_block(genesis_block.to_dict())

    def get_latest_block(self) -> Block:
        """Retorna o último bloco da cadeia"""
        return self.chain[-1]

    def add_transaction(self, from_address: str, to_address: str, amount: float) -> bool:
        """Adiciona uma nova transação pendente"""
        transaction = Transaction(from_address, to_address, amount)
        if self.db.insert_transaction(transaction.to_dict()):
            self.pending_transactions.append(transaction)
            return True
        return False

    def mine_pending_transactions(self, miner_address: str) -> Tuple[bool, str]:
        """Minera as transações pendentes"""
        if self.mined_tokens >= self.total_supply:
            return False, "Total supply reached"

        new_block = Block(
            len(self.chain),
            [t.to_dict() for t in self.pending_transactions],
            time.time(),
            self.get_latest_block().hash
        )

        # Proof of Work
        while new_block.hash[:self.difficulty] != "0" * self.difficulty:
            new_block.nonce += 1
            new_block.hash = new_block.calculate_hash()

        # Adiciona o bloco à cadeia
        self.chain.append(new_block)
        self.db.insert_block(new_block.to_dict())

        # Recompensa o minerador
        reward_amount = min(self.mining_reward, self.total_supply - self.mined_tokens)
        self.mined_tokens += reward_amount
        self.add_transaction("System", miner_address, reward_amount)

        self.pending_transactions = []
        return True, "Block mined successfully"

    def get_balance(self, address: str) -> float:
        """Retorna o saldo de uma carteira"""
        wallet = self.db.get_wallet(address)
        return wallet['balance'] if wallet else 0

    def is_chain_valid(self) -> bool:
        """Verifica se a blockchain é válida"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True