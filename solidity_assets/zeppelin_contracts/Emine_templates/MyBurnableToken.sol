pragma solidity ^0.4.18;

import "../token/ERC20/BurnableToken.sol";

/**
 * @title E-Mine Burnable Token Template
 * @dev Very simple ERC20 Token example, where all tokens are pre-assigned to the creator.
 * Note they can later distribute these tokens as they wish using `transfer` and other
 * `StandardToken` functions.
 */
contract MyBurnableToken is BurnableToken {

  string public constant name = "%token_name%"; // solium-disable-line uppercase
  string public constant symbol = "%token_symbol%"; // solium-disable-line uppercase
  uint8 public constant decimals = %token_decimals%; // solium-disable-line uppercase
  uint256 public constant INITIAL_SUPPLY = %token_initial_supply%;

  /**
   * @dev Constructor that gives msg.sender all of existing tokens.
   */
  function MyBurnableToken() public {
    
	totalSupply_ = INITIAL_SUPPLY;    
	
	//Uncomment if msg.sender should recieve all existing tokens	
	//balances[msg.sender] = INITIAL_SUPPLY;
    //Transfer(0x0, msg.sender, INITIAL_SUPPLY);
  }

}
