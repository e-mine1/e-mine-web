"strict mode"

const fs = require('fs');
const solc = require('solc');
const Web3 = require('web3');
const process = require('process');

const nodeAddr = 'http://localhost:8545'

var argv = require('minimist')(process.argv.slice(2));

if (!argv.file) {
    console.log('no --file argument given');
    process.exit(1)
}

const sourceFilePath = argv.file;
if (!fs.existsSync(sourceFilePath)) {
    console.log('file ' + file + ' does not exist');
}


const web3 = new Web3(new Web3.providers.HttpProvider(nodeAddr));
const input = fs.readFileSync(sourceFilePath);


const output = solc.compile(input.toString(), 1);
const bytecode = output.contracts['Token'].bytecode;
const abi = JSON.parse(output.contracts['Token'].interface);
const contract = web3.eth.contract(abi);

console.log(' size: '+ program.source);

var callback = function(err, res) {
    if (err) {
        console.log(err);
        return;
    }
    // Log the tx, you can explore status with eth.getTransaction()
    console.log(res.transactionHash);

    // If we have an address property, the contract was deployed
    if (res.address) {
        console.log('Contract address: ' + res.address);
        // Let's test the deployed contract
        testContract(res.address);
    }
};
const contractInstance = contract.new({
    data: '0x' + bytecode,
    from: web3.eth.coinbase,
    gas: 90000 * 2
}, callback);

