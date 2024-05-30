import subprocess

def invoke_chaincode(function, args):
    command = f'peer chaincode invoke -o orderer.example.com:7050 -C mychannel -n storage -c \'{{"Args":["{function}", {args}]}}\''
    subprocess.run(command, shell=True)

def query_chaincode(function, args):
    command = f'peer chaincode query -C mychannel -n storage -c \'{{"Args":["{function}", {args}]}}\''
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return json.loads(result.stdout)
