from asyncio import sleep, run
from subprocess import Popen
from conffu import Config
from urllib import request
from json import loads
from pywitness import FileWitness, TextParser, ConsoleChannel


class Main:
    def __init__(self):
        self.cfg = Config.from_file('resources/cfg/witness_tlf.json', no_compound_keys=True)  # deal with periods in regex keys
        self._done = False
        self.fw = None

        self.text_parsers = {}
        self.ch = ConsoleChannel()

        run(self.run())

    async def run(self):
        proc = Popen(['python.exe', r'rewriter.py',
                      # r'F:\0000\SC_Scn00_DRY_001.log',
                      r'F:\TUFLOW\models\Example_Models_QGIS\TUFLOW\runs\log\EG00\jaap_12_ab_34+56_cd+ef.tlf',
                      'test.log'], cwd='./temp')
        self.fw = FileWitness(proc.pid, r'./temp', [r'test.log'], handler=self.handler, obs_timeout=1)

        while not self._done:
            await sleep(1)

        print('waiting for process to terminate (no longer listening)')
        proc.wait()

    async def handler(self, src_path, line):
        if src_path not in self.text_parsers:
            self.text_parsers[src_path] = TextParser(self.cfg['parser'], timestamp=None)
            self.text_parsers[src_path].add_channel(self.ch)
        if line is None:
            self._done = True
        else:
            self.text_parsers[src_path].parse(line)


def update_config_from_server(cfg):
    req = request.Request(f'{cfg.server_url}/get_cfg')
    req.add_header('Cookie', f'api_key={cfg.api_key}')
    response = request.urlopen(req)
    # update with the retrieve configuration, but override with environment and then arguments
    cfg.update(loads(response.text)).update_from_environment().update_from_arguments()


def cli_entry_point():
    cfg = Config.from_file(
        'witness.json', parse_args=True, require_file=False
    ).update_from_environment().update_from_arguments()

    if cfg.server_url and cfg.api_key:
        update_config_from_server(cfg)

    Main()


if __name__ == '__main__':
    Main()
