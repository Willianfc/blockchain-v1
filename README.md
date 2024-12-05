# CoreHiveAi Blockchain

Uma blockchain descentralizada focada em computação distribuída.

## Características

- Token: CHAI
- Supply Total: 60 milhões
- Dificuldade inicial: 4
- Sistema de carteiras integrado
- Interface para desenvolvedores
- Rede de mineração distribuída

## Instalação no Servidor AWS

1. Atualizar o sistema:
```bash
sudo apt update && sudo apt upgrade -y
```

2. Instalar MongoDB:
```bash
# Importar a chave pública do MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -

# Adicionar repositório do MongoDB
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list

# Atualizar pacotes
sudo apt update

# Instalar MongoDB
sudo apt install -y mongodb-org
```

3. Iniciar MongoDB:
```bash
sudo systemctl start mongod
sudo systemctl enable mongod
```

4. Instalar Python e dependências:
```bash
sudo apt install python3 python3-pip -y
pip3 install -r requirements.txt
```

5. Iniciar a blockchain:
```bash
python3 blockchain/api.py
```

## Estrutura do Projeto

```
blockchain/
├── api.py              # API REST
├── chain.py            # Implementação da blockchain
├── config.py           # Configurações
├── database.py         # Gerenciador do MongoDB
├── models/
│   ├── block.py       # Modelo de bloco
│   ├── transaction.py # Modelo de transação
│   └── wallet.py      # Modelo de carteira
├── wallet_manager.py   # Gerenciador de carteiras
└── requirements.txt    # Dependências
```

## API Endpoints

- POST /wallet/new - Criar nova carteira
- GET /wallet/balance/<address> - Consultar saldo
- POST /transaction/new - Nova transação
- POST /mine - Minerar bloco
- GET /chain - Consultar blockchain

## Banco de Dados

O MongoDB é usado para armazenar:
- Carteiras
- Transações
- Blocos
- Informações dos mineradores
- Dados dos desenvolvedores