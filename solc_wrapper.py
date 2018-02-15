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
    print('contract deployed')
    pass


def compile_sol(contract_template_path, contract_name, contrat_template_map):
    t = CompileThread(contract_template_path, contract_name, contrat_template_map, on_compiled)
    t.thread.start()
    pass


class CompileThread:
    def __init__(self, contract_template_path, contract_name, contract_template_map, callback_on_done):
        self.contract_template_path = contract_template_path
        self.contract_name = contract_name
        self.callback_on_done = callback_on_done
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

        contract_path = os.path.join(working_dir, './zeppelin_contracts/Emine_templates/{}.sol'
                                     .format(self.contract_name))

        replace_placeholders_file(self.contract_template_map,
                                  self.contract_template_path, contract_path)

        # with open(os.path.join(working_dir, 'contracts/{}.sol'.format(self.source_name)), 'w') as f:
        #     f.write(self.source)
        # pass

        raise Exception()


        compile_code = os.system("{} compile >> {}/log.txt".format(TRUFFLE_BIN, working_dir))
        print('complation finished with code ' + str(compile_code))

        deploy_code = os.system("{} migrate --reset >> {}/log.txt".format(TRUFFLE_BIN, working_dir))
        print('migration finished with code ' + str(deploy_code))

        addr_file = os.path.join(working_dir, 'contract-addr.txt')

        with open(addr_file, 'r') as f:
            addr = f.read()

        success = False
        if addr and addr.startswith('0x'):
            success = True

        if self.callback_on_done is not None:
            self.callback_on_done(success=success, contract_addr=addr)


if __name__ == '__main__':
    tokenName = 'emine'
    symbol = 'emine'
    maxSupply = 1000
    decimals = 0
    genesisSupply = 1000

    map = {"tokenName": str(tokenName),
           'symbol': str(symbol),
           'maxSupply': str(maxSupply),
           'decimals': str(decimals),
           'genesisSupply': str(genesisSupply)
           }

    contract_template_name = 'MyStandardToken'
    contract_template_path = os.path.join(SOLIDITY_TEMPLATE_ROOT, 'MyStandardToken.sol')
    compile_sol(contract_template_path, contract_template_name, map)

# compile_sol(src)



# ts = int(time.time())
# compilation_dir = 'truffle_' + str(ts)
# working_dir = os.path.join(TRUFFLE_WORKDIR, compilation_dir)
# copy_tree(TRUFFLE_TEMPLATE, working_dir)
# print('copying to ' + working_dir)
#
# with open(os.path.join(working_dir, 'contracts/Contract.sol'), 'w') as f:
#     f.write(sol_code)
#
#     os.chdir(working_dir)
#     print(working_dir)
#
#     # cmd = 'truffle compile'.format(TRUFFLE_BIN)
#     # p = subprocess.Popen([TRUFFLE_BIN, 'compile'], stdout=subprocess.PIPE)
#
#     # print(p.communicate())
#
#     # process = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE)
#     # output, error = process.communicate()
#     # print(output)
#
# pool = Pool(max_workers=1)
# compile_thread = pool.submit(subprocess.call, "{} compile".format(TRUFFLE_BIN), shell=True)
#
# def on_migration_done(future):
#     print('migration done')
#     pass
#
# def on_compile_done(future):
#     print('compilation done')
#     migration_thread = pool.submit(subprocess.call, "{} migrate".format(TRUFFLE_BIN), shell=True)
#     migration_thread.add_done_callback(on_migration_done)
#     pass
#
# compile_thread.add_done_callback(on_compile_done)
