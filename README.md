# E-Mine Token Generator

E-Mine Token Genarator is a web service through which users can submit requests for creation and deployment of their smart contracts on the [Ethereum](https://www.ethereum.org/) network. It is built using [Flask](http://flask.pocoo.org/) and can be accessed through a REST API. User makes a request for a smart contract and provides relevant parameters. E-Mine Token Generator then prepares an actual smart contract by filling a template of [Solidity](https://solidity.readthedocs.io/en/develop/) code, compiles it and broadcasts it on Ethereum network. Currently it supports compilation and deployment of several standard tokens which are available in [OpenZeppelin](https://openzeppelin.org/) framework. For compilation and deployment on the server side we used [Truffle](http://truffleframework.com/) - a [Node.js](https://nodejs.org/en/) based development framework for Ethereum smart contracts. In order to test our system we set up a local Ethereum network using [Ganache](http://truffleframework.com/ganache/), a tool which is a part of the Truffle framework. Ganache features an internal Javascript implementation of Ethereum blockchain, as well as built-in blockchain explorer that allows easy testing and debugging of distributed applications.

<img src="docs/e-mine-web architecture.png" width="700">

## Token Templates

As a basis for token creation we use [OpenZeppelin](https://github.com/OpenZeppelin/zeppelin-solidity), a framework to build secure smart contracts on Ethereum.
For each token type a template is provided, implemented as an extended class of corresponding OpenZeppelin token implementation.
Following [token templates](https://github.com/e-mine1/e-mine-web/tree/master/solidity_assets/zeppelin_contracts/Emine_templates) are provided:

| Standard |      Token              | Description                                                                  |
|:-------- |:----------------------- |:---------------------------------------------------------------------------- | 
| ERC20    | Standard token          | Implementation of the basic standard token                                   |
|          | Basic token             | Standard token with no allowances                                            |
|          | Pausable token          | Standard token modified with pausable transfers                              |
|          | Mintable token          | A Simple ERC20 with mintable token creation                                  |
|          | Capped token            | Mintable token with a token cap                                              |
|          | Burnable token          | Token that can be irreversibly burned (destroyed)                            |
| ERC721   | Generic ERC721 token    | Generic implementation for the required functionality of the ERC721 standard |
| ERC827   | Generic ERC827 token    | ERC827 implementation - ERC20 standard with extra methods to transfer value  | 
|          |                         | and data and execute calls in transfers and approvals                        |

Each template contains placeholders for custom user parameters provided by the client application. Currently, the 
following parameters are supported
* *Token name* - Name of a token.
* *Token symbol* - Symbol representing the token.
* *Decimals* - Divisibility of a token, i.e. number of decimal places when displaying token value.
* *Initial supply* - Initial supply of tokens.

E.g. following code snippet shows placeholders for the Standard token template:

```
string public constant name = "%token_name%";
string public constant symbol = "%token_symbol%"; 
uint8 public constant decimals = %token_decimals%;
uint256 public constant INITIAL_SUPPLY = %token_initial_supply%;
```

Provided values can then be used in smart contract functions, such as in the following example of *MyStandardToken()* constructor that gives initial coin supply to *msg.sender*:

```
function MyStandardToken() public {
   totalSupply_ = INITIAL_SUPPLY;
   balances[msg.sender] = INITIAL_SUPPLY;
   Transfer(0x0, msg.sender, INITIAL_SUPPLY);
}
```

Each template can be easily extended to introduce new smart contract (token) parameters and functions according to the specific user requirements.

## REST API

REST API is implemented as a [python script](https://github.com/e-mine1/e-mine-web/blob/master/emine_web.py) with the following supported operations:

| API URL            | Method  | Required/Optional variables | Expected response                                             |
|:------------------ |:-------:|:--------------------------- |:------------------------------------------------------------- | 
| /api/requests/<id> | GET     | id=[integer]                |  **<TO-DO>**                                                              |
| /api/tokens/types  | GET     |                             | { "types": [                                                  |
|                    |         |                             |    &nbsp; &nbsp; "MyBasicToken",                              |
|                    |         |                             |    &nbsp; &nbsp; "MyBurnableToken",                           |
|                    |         |                             |    &nbsp; &nbsp; "MyCappedToken",                             |
|                    |         |                             |    &nbsp; &nbsp; "MyERC721Token",                             |
|                    |         |                             |    &nbsp; &nbsp; "MyERC827Token",                             |
|                    |         |                             |    &nbsp; &nbsp; "MyMintableToken",                           |
|                    |         |                             |    &nbsp; &nbsp; "MyPausableToken",                           |
|                    |         |                             |    &nbsp; &nbsp; "MyStandardToken" ]}                         |
| /api/tokens/create | POST    | tokenName=[string]          | { &nbsp; "created": [datetime],                               |
|                    |         | symbol=[string]             |  &nbsp; &nbsp; "key": [uuid],                                 |
|                    |         | maxSupply=[integer]         |  &nbsp; &nbsp; "status": "success" or "pending" or "failure", |
|                    |         | decimals=[integer]          |  &nbsp; &nbsp; "token_abi": [base64 encoded JSON value ]}     |                                              | 
|                    |         | genesisSupply=[integer]     |                                                               |


## Installation

# Installing prerequisites

`$ pip install -r requirements.txt`

# Install Truffle

`$ npm install -g truffle`

## Running the examples

**TO-DO**

## Useful links
- https://ethereum.stackexchange.com/questions/23279/steps-to-deploy-a-contract-using-metamask-and-truffle
