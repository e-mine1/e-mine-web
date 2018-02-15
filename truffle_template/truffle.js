var mnemonic = "trash zero adjust delay host hamster pool away vague split chronic lake";

console.log('truffle provider called');
module.exports = {
    networks: {
        development: {
            host: "localhost",
            port: 7545,
            network_id: "*", // Match any network id
            gas: 5000000
        }
    }
};
