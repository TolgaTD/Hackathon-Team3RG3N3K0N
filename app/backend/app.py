from flask import Flask, jsonify, request
import subprocess
import json

app = Flask(__name__)

@app.route('/store', methods=['POST'])
def store_data():
    data = request.json
    data_hash = data['dataHash']
    node_id = data['nodeId']

    # Hyperledger Fabric chaincode invoke
    command = f'peer chaincode invoke -o orderer.example.com:7050 -C mychannel -n storage -c \'{{"Args":["StoreData", "{data_hash}", "{node_id}"]}}\''
    subprocess.run(command, shell=True)
    
    return jsonify({"success": True, "data": data})

if __name__ == '__main__':
    app.run(debug=True)
