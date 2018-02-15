var Deploy = artifacts.require("./Migrations.sol");
var fs = require('fs');

module.exports = function (deployer) {
    deployer.deploy(Deploy)
        .then(() => Deploy.deployed())
        .then(_instance => {
            console.log('address is ' + _instance.address);
            fs.writeFile(__dirname + "/../contract-addr.txt", _instance.address,
                function (err) {
                    if (err) {
                        return console.log(err);
                    }
                    console.log("The file was saved!");
                });
        });
};
