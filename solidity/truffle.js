var HDWalletProvider = require("truffle-hdwallet-provider");

var infura_apikey = "9JcJLIaVEaZ7KQrnrJSj";
var mnemonic = "trash zero adjust delay host hamster pool away vague split chronic lake";

console.log('truffle provider called');
module.exports = {
  networks: {
    development: {
      host: "localhost",
      port: 8545,
      network_id: "*" // Match any network id
    },
    ropsten: {
      provider: new HDWalletProvider(mnemonic, "https://ropsten.infura.io/"+ infura_apikey),
      network_id: 3
    }
  }
};
