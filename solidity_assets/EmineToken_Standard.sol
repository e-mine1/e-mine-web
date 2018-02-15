pragma solidity ^0.4.18;


import "./ERC20/StandardToken.sol";


/**
 * @title EmineToken_Standard
 * @dev Very simple ERC20 Token example, where all tokens are pre-assigned to the creator.
 * Note they can later distribute these tokens as they wish using `transfer` and other
 * `StandardToken` functions.
 */
contract EmineToken_Standard is StandardToken {

  string public constant name = "Emine_standard"; // solium-disable-line uppercase
  string public constant symbol = "EMN"; // solium-disable-line uppercase
  uint8 public constant decimals = 0; // solium-disable-line uppercase

  //uint256 public constant INITIAL_SUPPLY = 10000 * (10 ** uint256(decimals));
  uint256 public constant INITIAL_SUPPLY = 10;

  /**
   * @dev Constructor that gives msg.sender all of existing tokens.
   */
  function SimpleToken() public {
    totalSupply_ = INITIAL_SUPPLY;
    balances[msg.sender] = INITIAL_SUPPLY;
    Transfer(0x0, msg.sender, INITIAL_SUPPLY);
  }

}
