import json

fuels = None
# saving fuels to memory
def load_fuels():
    with open('../library/fuels.json', 'r') as f:
        fuels = json.load(f)

