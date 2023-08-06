import argparse
import json
import subprocess

from tabulate import tabulate
from termcolor import colored

from .module import Module


class Lxc(Module):

    def parse_args(parser: argparse.ArgumentParser):
        parser.add_argument('-c', '--compact', help='compact output', action='store_true')
        return parser

    def __str__(self):
        _proc = subprocess.Popen(['lxc', 'list', '--format', 'json'], stdout=subprocess.PIPE)
        _json = json.loads(_proc.stdout.read().decode())
#
        _out = []
        for _item in _json:
            _name = ''
            _status = ''
            _location = ''
            _addresses = []
            _profiles = []
            for _field in _item.keys():
                if _field == 'name':
                    _name = _item.get(_field)
                if _field == 'status':
                    _status = _item.get(_field)
                if _field == 'location':
                    _location = _item.get(_field)
                if _field == 'profiles' and not self._args.compact:
                    try:
                        for _profile in _item.get('profiles'):
                            if _profile != 'default':
                                _profiles.append(_profile)
                    except Exception:
                        continue
                if _field == 'state' and not self._args.compact:
                    try:
                        for _dev in _item.get('state').get('network').items():
                            if _dev[0] == 'lo':
                                continue
                            for _addr in _dev[1]['addresses']:
                                if _addr['family'] == 'inet':
                                    _addresses.append('%s (%s)' % (_addr.get('address'), _dev[0]))
                    except Exception:
                        continue

            # Color code the name by status
            _colors = {
                'Stopped': 'yellow',
                'Running': 'green'
            }

            _out.append([
                colored(_name, _colors.get(_status, 'red')),
                '\n'.join(_profiles),
                '\n'.join(_addresses),
                _location
            ])

        return(tabulate(_out, tablefmt='plain'))
