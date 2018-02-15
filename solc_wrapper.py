import os
import logging
import time
import threading
from distutils.dir_util import copy_tree

TEMPLATE_SRC_LOCATION = 'solidity_assets/contract_template.sol'

TRUFFLE_BIN = '/usr/local/bin/truffle'
TRUFFLE_TEMPLATE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'truffle_template')
TRUFFLE_WORKDIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'truffle_workdir')


def generateSolFile(tokenName, symbol, maxSupply, decimals, genesisSupply):
    map = {"tokenName": str(tokenName),
           'symbol': str(symbol),
           'maxSupply': str(maxSupply),
           'decimals': str(decimals),
           'genesisSupply': str(genesisSupply)
           }

    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), TEMPLATE_SRC_LOCATION)
    source = open(path, 'r').read()

    for placeholder in map.keys():
        value = map.get(placeholder)
        source = source.replace('%%{}%%'.format(placeholder), value)
        logging.info('replacing {} with {} in {}'.format(placeholder, value, path))

    return source

    pass

def on_compiled(success, contract_addr):
    print('contract deployed')
    pass

def compile_sol(sol_code):
    t = CompileThread(sol_code, on_compiled)
    t.thread.start()
    pass


class CompileThread:
    def __init__(self, solcode, callback_on_done):
        self.source = solcode
        self.callback_on_done = callback_on_done
        self.thread = threading.Thread(target=self.run, args=())

    def run(self):
        ts = int(time.time())
        compilation_dir = 'truffle_' + str(ts)
        working_dir = os.path.join(TRUFFLE_WORKDIR, compilation_dir)
        copy_tree(TRUFFLE_TEMPLATE, working_dir)
        print('copying to ' + working_dir)

        with open(os.path.join(working_dir, 'contracts/Migrations.sol'), 'w') as f:
            f.write(self.source)
        pass

        os.chdir(working_dir)

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
    src = generateSolFile('name', 'symbol', 1000, 0, 10)

    compile_sol(src)



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
