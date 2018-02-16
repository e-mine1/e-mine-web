import os
import logging
import time
import threading
from distutils.dir_util import copy_tree

TEMPLATE_SRC_LOCATION = 'solidity_assets/contract_template.sol'

HOME = os.path.dirname(os.path.realpath(__file__))

SOLIDITY_TEMPLATE_ROOT = os.path.join(HOME, './solidity_assets/zeppelin_contracts/Emine_templates')

TRUFFLE_BIN = '/usr/local/bin/truffle'
TRUFFLE_TEMPLATE_DIR = os.path.join(HOME, 'truffle_template')
TRUFFLE_WORK_DIR = os.path.join(HOME, 'truffle_workdir')
TRUFFLE_DEPLOY_SCRIPT = os.path.join(HOME, 'solidity_assets/1_initial_migration.js')

SUPPORTED_TEMPLATES = ['MyBasicToken', 'MyBurnableToken', 'MyCappedToken', 'MyERC721Token',
                       'MyERC827Token', 'MyMintableToken', 'MyPausableToken', 'MyStandardToken']


def replace_placeholders(keyword_map, source_path):
    source = ''

    print('reading file: ' + source_path)
    with open(source_path, 'r') as f:
        source = f.read()
    pass

    for placeholder in keyword_map.keys():
        value = keyword_map.get(placeholder)
        source = source.replace('%{}%'.format(placeholder), value)
        print('replacing {} with {} in {}'.format(placeholder, value, source_path))

    return source


def replace_placeholders_file(keyword_map, source_path, target_path):
    source = replace_placeholders(keyword_map, source_path)

    print('writing file: ' + target_path)
    with open(target_path, 'w') as f:
        f.write(source)
    pass


def on_compiled(success, contract_addr):
    print('contract deployed, status: ' + str(success) + ', addr: ' + contract_addr)
    pass


def compile_sol(contract_template_path, contract_name, contrat_template_map, callback_on_done, request_id):
    t = CompileThread(contract_template_path, contract_name,
                      contrat_template_map, callback_on_done, request_id)
    t.thread.start()
    pass


class CompileThread:
    def __init__(self, contract_template_path, contract_name, contract_template_map, callback_on_done,
                 request_id):
        self.contract_template_path = contract_template_path
        self.contract_name = contract_name
        self.callback_on_done = callback_on_done
        self.request_id = request_id
        self.contract_template_map = contract_template_map

        self.thread = threading.Thread(target=self.run, args=())

    def run(self):
        ts = int(time.time())
        compilation_dir = 'truffle_' + str(ts)
        working_dir = os.path.join(TRUFFLE_WORK_DIR, compilation_dir)

        print('copying to ' + working_dir)
        copy_tree(TRUFFLE_TEMPLATE_DIR, working_dir)
        os.chdir(working_dir)

        deploy_script = os.path.join(working_dir, 'migrations/1_initial_migration.js')
        replace_placeholders_file({
            'fileName': self.contract_name
        }, deploy_script, deploy_script)

        contract_path = os.path.join(working_dir, 'contracts/zeppelin_contracts/Emine_templates/{}.sol'
                                     .format(self.contract_name))

        replace_placeholders_file(self.contract_template_map,
                                  self.contract_template_path, contract_path)

        compile_code = os.system("{} compile >> {}/log.txt".format(TRUFFLE_BIN, working_dir))
        print('complation finished with code ' + str(compile_code))

        deploy_code = os.system("{} migrate --reset >> {}/log.txt".format(TRUFFLE_BIN, working_dir))
        print('migration finished with code ' + str(deploy_code))

        addr_file = os.path.join(working_dir, 'contract-addr.txt')

        with open(addr_file, 'r') as f:
            addr = f.read()

        abi_file = os.path.join(working_dir, 'build/contracts/{}.json'.format(self.contract_name))
        with open(abi_file, 'r') as f:
            abi = f.read()

        success = False
        if addr and addr.startswith('0x'):
            success = True

        if self.callback_on_done is not None:
            self.callback_on_done(success, addr, abi, self.request_id)


if __name__ == '__main__':
    #
    # this is just test code
    #
    tokenName = 'emine'
    symbol = 'emine'
    maxSupply = 1000
    decimals = 0
    genesisSupply = 1000

    map = {"token_name": str(tokenName),
           'token_symbol': str(symbol),
           'token_decimals': str(decimals),
           'token_initial_supply': str(genesisSupply)
           }

    contract_template_name = 'MyStandardToken'
    contract_template_path = os.path.join(SOLIDITY_TEMPLATE_ROOT, 'MyStandardToken.sol')
    compile_sol(contract_template_path, contract_template_name, map, on_compiled)
