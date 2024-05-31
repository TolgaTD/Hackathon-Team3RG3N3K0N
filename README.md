# Hackathon-Team3RG3N3K0N
# Decentralized Storage System

## Description
This system allows decentralized data storage across different nodes, with blockchain for security and integrity.

## Setup
1. Install required dependencies:
    - Docker
    - Docker Compose
    - Hyperledger Fabric tools

2. Start the Fabric network:
    ```bash
    cryptogen generate --config=./crypto-config.yaml
    configtxgen -profile TwoOrgsOrdererGenesis -outputBlock ./channel-artifacts/genesis.block
    docker-compose -f docker-compose-cli.yaml up -d
    ```

3. Create and join channel:
    ```bash
    docker exec -it cli bash
    peer channel create -o orderer.example.com:7050 -c mychannel -f ./channel-artifacts/channel.tx
    peer channel join -b mychannel.block
    ```

4. Install and instantiate chaincode:
    ```bash
    peer chaincode install -n storage -v 1.0 -p github.com/chaincode/storage/go
    peer chaincode instantiate -o orderer.example.com:7050 -C mychannel -n storage -v 1.0 -c '{"Args":[]}'
    ```

5. Run the backend:
    ```bash
    cd app/backend
    flask run
    ```

6. Access the frontend at `http://localhost:5000`.

## Usage
Detail how to use the system, with examples of interactions with the system.
