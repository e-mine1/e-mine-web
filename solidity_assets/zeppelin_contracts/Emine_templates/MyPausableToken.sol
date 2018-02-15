pragma solidity ^0.4.18;

import "../token/ERC20/PausableToken.sol";

/**
 * @title E-Mine Pausable Token Template
 */
contract MyPausableToken is StandardToken {

  string public constant name = "%token_name%"; // solium-disable-line uppercase
  string public constant symbol = "%token_symbol%"; // solium-disable-line uppercase
  uint8 public constant decimals = %token_decimals%; // solium-disable-line uppercase
  uint256 public constant INITIAL_SUPPLY = %token_initial_supply%;

  /**
   * @dev Constructor
   */
  function MyPausableToken() public {
    totalSupply_ = INITIAL_SUPPLY;
	//Uncomment if msg.sender should recieve all existing tokens	
	//balances[msg.sender] = INITIAL_SUPPLY;
    //Transfer(0x0, msg.sender, INITIAL_SUPPLY);
  }

}
