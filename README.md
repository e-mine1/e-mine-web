# E-Mine Token Generator

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
* Token name
* Token symbol
* Decimals
* Initial supply

E.g. following code snippet shows placeholders for the Standard token template:

```python
string public constant name = "%token_name%";
string public constant symbol = "%token_symbol%"; 
uint8 public constant decimals = %token_decimals%;
uint256 public constant INITIAL_SUPPLY = %token_initial_supply%;
```

Provided values can then be used in smart contract functions, such as in the following example of *MyStandardToken()* constructor that gives initial coin supply to *msg.sender*:

```python
function MyStandardToken() public {
   totalSupply_ = INITIAL_SUPPLY;
   balances[msg.sender] = INITIAL_SUPPLY;
   Transfer(0x0, msg.sender, INITIAL_SUPPLY);
}
```

Each template can be easily extended to introduce new smart contract (token) parameters and functions according to the specific user requirements.

#REST API

REST API is implemented as a [python script](https://github.com/e-mine1/e-mine-web/blob/master/emine_web.py) with the following supported operations:

| API URL            | Method  | Required/Optional variables | Expected response                            |
|:------------------ |:-------:|:--------------------------- |:-------------------------------------------  | 
| /api/requests/<id> | GET     | id=[integer]                |                                              |
| /api/tokens/types  | GET     |                             | { "types": [                                 |
|                    |         |                             |    "MyBasicToken",                           |
|                    |         |                             |    "MyBurnableToken",                        |
|                    |         |                             |    "MyCappedToken",                          |
|                    |         |                             |    "MyERC721Token",                          |
|                    |         |                             |    "MyERC827Token",                          |
|                    |         |                             |    "MyMintableToken",                        |
|                    |         |                             |    "MyPausableToken",                        |
|                    |         |                             |    "MyStandardToken" ]}                      |
|                    |         |                             |                                              |
|                    |         |                             |                                              |
| /api/tokens/create | POST    | tokenName=[string]          | {"created": [datetime],                      |
|                    |         | symbol=[string]             |  "key": [uuid],                              |
|                    |         | maxSupply=[integer]         |  "status":                                   |
|                    |         | decimals=[integer]          |     "success" or "pending" or "failure",     | 
|                    |         | genesisSupply=[integer]     |  "token_abi": [base64 encoded JSON value]}   |
|                    |         |                             |                                              |


## Useful links
- https://ethereum.stackexchange.com/questions/23279/steps-to-deploy-a-contract-using-metamask-and-truffle
