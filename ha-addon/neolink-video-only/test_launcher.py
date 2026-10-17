"""Isolated launcher checks using synthetic options and no network access."""
import json
import os
from pathlib import Path
import runpy
import stat
import tempfile
import tomllib
from unittest.mock import patch

module = runpy.run_path('/run.py')
options = {
    'bind': '127.0.0.1', 'bind_port': 8558, 'disable_audio': True,
    'cameras': [{'name': 'example', 'address': 'example.invalid:9000',
                 'username': 'example', 'password': 'quote"backslash\\newline\n'}],
}
config = tomllib.loads(module['make_config'](options))
assert config['cameras'][0]['password'] == options['cameras'][0]['password']
assert config['cameras'][0]['stream'] == 'mainStream'

for cameras in [[], options['cameras'] * 2]:
    try:
        module['make_config']({'cameras': cameras})
    except ValueError:
        pass
    else:
        raise AssertionError('Expected missing/duplicate camera validation')

with tempfile.TemporaryDirectory() as directory:
    data = Path(directory)
    (data / 'options.json').write_text(json.dumps(options))
    def mapped_path(value):
        return data / Path(value).name
    with patch.dict(module['main'].__globals__, {'Path': mapped_path}), patch('os.execv') as execute:
        module['main']()
        assert os.environ['NEOLINK_DISABLE_AUDIO'] == '1'
        assert stat.S_IMODE((data / 'neolink.toml').stat().st_mode) == 0o600
        execute.assert_called_once()
        options['disable_audio'] = False
        (data / 'options.json').write_text(json.dumps(options))
        module['main']()
        assert 'NEOLINK_DISABLE_AUDIO' not in os.environ
print('Launcher checks passed.')
