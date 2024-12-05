"""
Gerenciador de banco de dados
"""
import sqlite3
from typing import Dict, Any, List, Optional
from .schema import SCHEMA_DEFINITIONS
from ..config import BLOCKCHAIN_CONFIG

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect(BLOCKCHAIN_CONFIG['DATABASE_PATH'])
        self.cursor = self.conn.cursor()
        self.initialize_database()

    def initialize_database(self):
        """Cria todas as tabelas necessárias"""
        for table_schema in SCHEMA_DEFINITIONS.values():
            self.cursor.execute(table_schema)
        self.conn.commit()

    def execute_query(self, query: str, params: tuple = ()) -> Optional[sqlite3.Cursor]:
        """Executa uma query SQL com parâmetros"""
        try:
            result = self.cursor.execute(query, params)
            self.conn.commit()
            return result
        except sqlite3.Error as e:
            print(f"Erro na execução da query: {e}")
            return None

    def fetch_one(self, query: str, params: tuple = ()) -> Optional[tuple]:
        """Busca um único resultado"""
        result = self.execute_query(query, params)
        return result.fetchone() if result else None

    def fetch_all(self, query: str, params: tuple = ()) -> List[tuple]:
        """Busca todos os resultados"""
        result = self.execute_query(query, params)
        return result.fetchall() if result else []

    def insert_wallet(self, address: str, name: str) -> bool:
        """Insere uma nova carteira"""
        query = "INSERT INTO wallets (address, balance, name) VALUES (?, 0, ?)"
        result = self.execute_query(query, (address, name))
        return result is not None

    def update_wallet_balance(self, address: str, new_balance: float) -> bool:
        """Atualiza o saldo de uma carteira"""
        query = "UPDATE wallets SET balance = ?, last_updated = CURRENT_TIMESTAMP WHERE address = ?"
        result = self.execute_query(query, (new_balance, address))
        return result is not None

    def insert_transaction(self, transaction: Dict[str, Any]) -> bool:
        """Insere uma nova transação"""
        query = """
            INSERT INTO transactions 
            (id, from_address, to_address, amount, timestamp, status) 
            VALUES (?, ?, ?, ?, ?, ?)
        """
        result = self.execute_query(query, (
            transaction['id'],
            transaction['from'],
            transaction['to'],
            transaction['amount'],
            transaction['timestamp'],
            'pending'
        ))
        return result is not None

    def insert_block(self, block: Dict[str, Any]) -> bool:
        """Insere um novo bloco"""
        query = """
            INSERT INTO blocks 
            (hash, previous_hash, timestamp, nonce, difficulty, miner_address, reward)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        result = self.execute_query(query, (
            block['hash'],
            block['previous_hash'],
            block['timestamp'],
            block['nonce'],
            block['difficulty'],
            block['miner_address'],
            block['reward']
        ))
        return result is not None

    def close(self):
        """Fecha a conexão com o banco de dados"""
        self.conn.close()