import os

TEMPLATE_LOCATION = 'solidity_assets/contract_template.sol'
TRUFFLE_PATH = '/usr/local/bin/truffle'


def generateSolFile(tokenName, symbol, maxSupply, decimals, genesisSupply):
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), TEMPLATE_LOCATION)
    source = open(path, 'r').read()
    source = source.replace('%placeHolder%', 'someValue')
    return source


def compileSol(solCode):
    pass
