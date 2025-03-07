# Simplicity Blockchain

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.7+-yellow.svg)

A lightweight, educational blockchain implementation in Python designed to help beginners understand the fundamental concepts of blockchain technology.

## 📋 Overview

Simplicity Blockchain is an intuitive implementation that demonstrates core blockchain concepts including decentralized consensus, proof-of-work mining, cryptographic verification, and distributed ledger technology. Built with Python and Firebase, it provides a hands-on learning platform for blockchain fundamentals while remaining accessible to beginners.

![Blockchain Structure](https://via.placeholder.com/800x300?text=Blockchain+Structure+Diagram)

## ✨ Key Features

- **Core Blockchain Components**: Blocks, transactions, and cryptographic linking
- **Proof of Work Mining**: Educational implementation of mining mechanics
- **Digital Signatures**: ECDSA-based transaction authentication
- **Decentralized Network**: Node discovery and peer-to-peer communication
- **Consensus Algorithm**: Chain validation and conflict resolution
- **Mining Rewards**: Coinbase transaction implementation
- **Data Persistence**: Firebase integration for reliable storage
- **Node Management**: TTL-based network coordination
- **RESTful API**: HTTP interfaces for blockchain interaction

## 🔍 Architecture

The system follows a modular architecture with three primary layers:

```
┌─────────────────────────────────────────┐
│          Simplicity Blockchain          │
└──────────────┬──────────────────────────┘
               │
     ┌─────────┴─────────┐
     ▼                   ▼                   ▼
┌──────────┐      ┌─────────────┐     ┌──────────────┐
│ Core     │      │ Network     │     │ Persistence  │
│ Layer    │      │ Layer       │     │ Layer        │
└──────────┘      └─────────────┘     └──────────────┘
```

### Blockchain Structure

Each block in the chain contains:

```
┌─────────────────────────────┐
│ Block                       │
│                             │
│ ┌─────────────────────────┐ │
│ │ Header                  │ │
│ │ - Index                 │ │
│ │ - Timestamp             │ │
│ │ - Previous Hash         │ │
│ │ - Merkle Root           │ │
│ │ - Nonce (Proof)         │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─────────────────────────┐ │
│ │ Transactions            │ │
│ │ - Transaction 1         │ │
│ │ - Transaction 2         │ │
│ │ - ...                   │ │
│ └─────────────────────────┘ │
└─────────────────────────────┘
```

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/affanshaikhsurab/simplicity-server.git
cd simplicity-blockchain

# Install required dependencies
pip install -r requirements.txt

# Configure Firebase credentials
# 1. Create a Firebase project at https://console.firebase.google.com/
# 2. Generate a service account key file
# 3. Save the JSON file to the project directory as firebase-credentials.json
```

## 📱 Usage

### Starting a Node

```bash
# Start the primary node
python app.py

# Start additional nodes on different ports
python app.py --port 5001
```

### Interacting with the Blockchain

Once your nodes are running, you can interact with them using the API:

1. **View the blockchain**:

   ```
   GET http://localhost:5000/chain
   ```
2. **Mine a new block**:

   ```
   GET http://localhost:5000/mine
   ```
3. **Submit a transaction**:

   ```
   POST http://localhost:5000/transactions/new
   ```

   With JSON body:

   ```json
   {
     "transaction": {
       "sender": "sender_address",
       "recipient": "recipient_address",
       "amount": 5.0
     },
     "digital_signature": "base64_encoded_signature",
     "public_key": "base64_encoded_public_key"
   }
   ```
4. **Register new nodes**:

   ```
   POST http://localhost:5000/nodes/register
   ```

   With JSON body:

   ```json
   {
     "nodes": ["http://localhost:5001", "http://localhost:5002"]
   }
   ```
5. **Resolve conflicts**:

   ```
   GET http://localhost:5000/nodes/resolve
   ```

## 📚 Technical Components

### Core Files


| File           | Description                                                               |
| -------------- | ------------------------------------------------------------------------- |
| blockchain.py  | Core blockchain implementation, handling blocks, transactions, and mining |
| database.py    | Firebase integration for blockchain persistence                           |
| account_db.py  | Account management and key pair operations                                |
| nodeManager.py | Network node discovery and management                                     |
| app.py         | Flask API server exposing blockchain functionality                        |

### Mining Process

The mining process follows these steps:

1. **Transaction Selection**: Pending transactions are selected from the pool
2. **Coinbase Creation**: A reward transaction is created for the miner
3. **Proof of Work**: A nonce is found that creates a block hash with the target difficulty
4. **Block Construction**: The new block is assembled with transactions and proof
5. **Network Propagation**: The new block is broadcast to all nodes
6. **Validation**: Other nodes verify the block before adding it to their chain

![Mining Process](https://via.placeholder.com/800x300?text=Mining+Process+Diagram)

### Transaction Verification

Transactions are secured using ECDSA (Elliptic Curve Digital Signature Algorithm):

1. Sender creates and signs transaction with their private key
2. Transaction and sender's public key are broadcast to the network
3. Nodes verify the signature using the provided public key
4. Valid transactions are added to the mining pool

## 💻 Development and Contributing

Contributions are welcome! Please see our contribution guidelines for details.

**Development Environment Setup**:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows:
venv\Scripts\activate
# Unix/MacOS:
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contact

For questions or support:

- **GitHub Issues**: [https://github.com/yourusername/simplicity-blockchain/issues](https://github.com/yourusername/simplicity-blockchain/issues)
- **Email**: your.email@example.com

---

<p align="center">
  <i>Built with ❤️ for blockchain education</i>
</p>
