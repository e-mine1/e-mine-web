pragma solidity ^0.4.18;

import "../token/ERC20/StandardToken.sol";

/**
 * @title E-Mine Standard Token Template
 */
contract MyStandardToken is StandardToken {

  string public constant name = "%token_name%"; // solium-disable-line uppercase
  string public constant symbol = "%token_symbol%"; // solium-disable-line uppercase
  uint8 public constant decimals = %token_decimals%; // solium-disable-line uppercase
  uint256 public constant INITIAL_SUPPLY = %token_initial_supply%;

  /**
   * @dev Constructor that gives msg.sender all of existing tokens.
   */
  function MyStandardToken() public {
    totalSupply_ = INITIAL_SUPPLY;
    balances[msg.sender] = INITIAL_SUPPLY;
    Transfer(0x0, msg.sender, INITIAL_SUPPLY);
  }
}
