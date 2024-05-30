package main

import (
	"encoding/json"
	"fmt"
	"time"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

type StorageContract struct {
	contractapi.Contract
}

type DataLog struct {
	DataHash  string `json:"dataHash"`
	NodeID    string `json:"nodeId"`
	Timestamp string `json:"timestamp"`
}

// StoreData adds a new data log to the ledger
func (s *StorageContract) StoreData(ctx contractapi.TransactionContextInterface, dataHash string, nodeId string) error {
	timestamp := time.Now().Format(time.RFC3339)
	log := DataLog{
		DataHash:  dataHash,
		NodeID:    nodeId,
		Timestamp: timestamp,
	}
	logKey := fmt.Sprintf("LOG_%s_%s", dataHash, nodeId)
	logJSON, err := json.Marshal(log)
	if err != nil {
		return err
	}
	return ctx.GetStub().PutState(logKey, logJSON)
}

// GetLog retrieves a data log from the ledger by its key
func (s *StorageContract) GetLog(ctx contractapi.TransactionContextInterface, logKey string) (*DataLog, error) {
	logJSON, err := ctx.GetStub().GetState(logKey)
	if err != nil {
		return nil, err
	}
	if logJSON == nil {
		return nil, fmt.Errorf("log not found: %s", logKey)
	}
	var log DataLog
	err = json.Unmarshal(logJSON, &log)
	if err != nil {
		return nil, err
	}
	return &log, nil
}

func main() {
	chaincode, err := contractapi.NewChaincode(new(StorageContract))
	if err != nil {
		fmt.Printf("Error creating StorageContract chaincode: %s", err.Error())
		return
	}
	if err := chaincode.Start(); err != nil {
		fmt.Printf("Error starting StorageContract chaincode: %s", err.Error())
	}
}
