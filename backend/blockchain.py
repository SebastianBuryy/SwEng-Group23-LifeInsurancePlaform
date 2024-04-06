from web3 import Web3 # requires you to run `pip install web3`
import os
import subprocess as sp
import json
import requests
import time
from secret import * #ALCHEMY_API_KEY, ETHERSCAN_API_KEY, CREATOR_ADDRESS # , WALLET_PRIVATE_KEY
# API_KEY = os.environ['API_KEY']
project_root_folder = os.path.dirname(os.path.dirname(__file__))

# USER_CONTRACT_ABI = abi = [{ "inputs": [{ "internalType": "bool", "name": "newSmokerStatus", "type": "bool" }, { "internalType": "bool", "name": "newGymStatus", "type": "bool" }, { "internalType": "uint256", "name": "newWeight", "type": "uint256" }, { "internalType": "uint256", "name": "newAge", "type": "uint256" }], "name": "updateProfile", "outputs": [{ "internalType": "string", "name": "", "type": "string" }], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "name": "getUserProfile", "outputs": [{ "components": [{ "internalType": "string", "name": "userName", "type": "string" }, { "internalType": "bool", "name": "isSmoker", "type": "bool" }, { "internalType": "bool", "name": "goesToGym", "type": "bool" }, { "internalType": "uint256", "name": "weight", "type": "uint256" }, { "internalType": "uint256", "name": "age", "type": "uint256" }, { "internalType": "uint256", "name": "payout", "type": "uint256" }, { "internalType": "uint256", "name": "premium", "type": "uint256" }, { "internalType": "uint256", "name": "contractCreationDate", "type": "uint256" }, { "internalType": "uint256", "name": "contractAnullment", "type": "uint256" }, { "internalType": "uint256", "name": "nextPaymentDate", "type": "uint256" }], "internalType": "struct Insurance.UserProfile", "name": "", "type": "tuple" }], "stateMutability": "view", "type": "function" }, { "inputs": [{ "internalType": "bool", "name": "premiumPaid", "type": "bool" }], "name": "verifyPremiumPayment", "outputs": [], "stateMutability": "nonpayable", "type": "function" }]
contract_path = project_root_folder + "/Blockchain/artifacts/contracts/userContract.sol/Insurance.json"

USER_CONTRACT_ABI = json.load(open(contract_path))['abi']

# Alchemy API URL
alchemy_url = f"https://eth-sepolia.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
web3 = Web3(Web3.HTTPProvider(alchemy_url))

def check_connection():
  # Verify if the connection is successful
  if web3.is_connected():
      print("-" * 50)
      print("Connection Successful")
      print("-" * 50)
      latest_block = web3.eth.get_block("latest")
      print(latest_block)
  else:
      print("Connection Failed")
  
# def get_contract_abi():
#   # URL for the Etherscan API endpoint to get contract ABI
#   etherscan_url = f"https://api-sepolia.etherscan.io/api?module=contract&action=getabi&address={CONTRACT_ADDRESS}&apikey={ETHERSCAN_API_KEY}"

#   # Make an API request to Etherscan
#   response = requests.get(etherscan_url)

#   # Parse the response JSON
#   data = response.json()

#   # Check if the request was successful
#   if data['status'] == '1' and data['message'] == 'OK':
#       # ABI is returned as a JSON-encoded string, so we need to parse it
#       cONTRACT_ABI = json.loads(data['result'])
#       print("Contract ABI:")
#       print(json.dumps(cONTRACT_ABI, indent=2))
#   else:
#       print("Error fetching contract ABI:", data['result'])

def deploy():
    # requires hardhat installed, `npm install hardhat`
    # and existing compiled contract (do this with `npx hardhat compile`)

    result = sp.run(args=["npx", "hardhat", "run", "scripts/deploy.js", "--network", "sepolia"], cwd=project_root_folder+"/Blockchain", capture_output=True, text=True)
    print(result.stderr)
    cont_addr = result.stdout.removeprefix("Contract Deployed to Address: ")
    return cont_addr

def example():
   # Initialize address nonce
  nonce = web3.eth.get_transaction_count(CALLER_ADDRESS)

  try:
      # Parse the ABI string to a Python object
      parsed_abi = json.loads(cONTRACT_ABI)
      print("ABI is valid JSON.")
  except json.JSONDecodeError as e:
      print(f"Invalid JSON: {e}")

  # Then use the parsed ABI to create the contract instance
  contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=parsed_abi)

  # Now, parsed_abi should be a list of dictionaries
  if isinstance(parsed_abi, list):
      # Extract functions from the ABI
      functions = [item for item in parsed_abi if item.get('type') == 'function']

      # Iterate over the functions and print details
      for func in functions:
          func_name = func.get('name', 'Unnamed function')
          inputs = func.get('inputs', [])
          input_details = ', '.join([f"{inp['type']} {inp['name']}" for inp in inputs])
          print(f"Function name: {func_name}({input_details})")
  else:
      print("The ABI was not parsed into a list as expected.")


  # Create the contract instance
  contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=parsed_abi)

  # Example function call (Make sure the function exists in your ABI)
#   try:
#       # Replace 'getSentence' with an actual function from your contract's ABI
#       quote = contract.functions.getSentence().call()
#       print("\nThe famous quote is:\n", quote)
#       pass  # Replace or remove this pass statement with your function call
#   except Exception as e:
#       print(f"Error calling function: {e}")

def list_abi_functions():
  # Now, parsed_abi should be a list of dictionaries
  if isinstance(USER_CONTRACT_ABI, list):
      # Extract functions from the ABI
      functions = [item for item in USER_CONTRACT_ABI if item.get('type') == 'function']

      # Iterate over the functions and print details
      for func in functions:
          func_name = func.get('name', 'Unnamed function')
          inputs = func.get('inputs', [])
          input_details = ', '.join([f"{inp['type']} {inp['name']}" for inp in inputs])
          print(f"Function name: {func_name}({input_details})")
  else:
      print("The ABI was not parsed into a list as expected.")

def get_contract_details(contract_address):
  nonce = web3.eth.get_transaction_count(CREATOR_ADDRESS)

  # Then use the parsed ABI to create the contract instance
  contract = web3.eth.contract(address=contract_address, abi=USER_CONTRACT_ABI)

  try:
      # ret = contract.functions.updateProfile(True, False, 70, 30).call()
      ret = contract.functions.getUserProfile().call()
      name, isSmoker, isGymBro, weight, age, max_payout, monthy_premium, creation, expiry, nextpay = ret #('John', True, True, 70, 30, 75000, 450, 1711061088, 1742597088, 1713653088)
      creation = time.ctime(creation)
      print(creation)
      expiry = time.ctime(expiry)
      print(expiry)
      nextpay = time.ctime(nextpay)
      print(nextpay)
      print(ret)
  except Exception as e:
    print(f"Error calling function: {e}")


startBlock = 0
endBlock = 12878196
def get_contract_events(contract_address):
    url = f"https://api-sepolia.etherscan.io/api?module=logs&action=getLogs&address={contract_address}&fromBlock={startBlock}&toBlock={endBlock}&page=1&offset=1000&apikey={ETHERSCAN_API_KEY}"
    events = requests.get(url).json().get('result', [])
    # 'timeStamp' 'data'
    risk_timeline = []
    for e in events:
        timestamp = int(e['timeStamp'], 16) # time.ctime() to turn to string
        risk = int(e['data'], 16)
        risk_timeline.append((timestamp,risk))
    risk_timeline.sort(key=lambda x : x[0], reverse=True)
    print(risk_timeline)
    return risk_timeline

if __name__=="__main__":
    # get_contract_abi()
    
    # example()
    list_abi_functions()
    # get_contract_details(CONTRACT_ADDRESS)
    # get_contract_events(CONTRACT_ADDRESS)
    # print(deploy())
    pass