# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['http_log_parser']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['http-log-parser = http_log_parser:main']}

setup_kwargs = {
    'name': 'http-log-parser',
    'version': '0.2.0',
    'description': 'Cli tool to parse stream of http access events into json formatted events.',
    'long_description': 'http-log-parser\n===\n\nPackage supports "nginx-combined" format for now.\n\n```\nusage: http-log-parser [-h] [--no-query] [--skip-errors] [files [files ...]]\n\npositional arguments:\n  files\n\noptional arguments:\n  -h, --help     show this help message and exit\n  --no-query\n  --skip-errors\n```\n\n**Example**\n\n```\n$ http-log-parser /var/log/http/access.log | jq .  # jq used for pretty printing \n{\n  "ip": "1.2.3.4",\n  "ts": 1592427669,\n  "method": "GET",\n  "path": "/path/",\n  "status": 204,\n  "size": 0,\n  "referer": "https://example.com/",\n  "user_agent": "Chrome/1 Firefox/2 IE/3 Edge/4",\n  "query": {\n    "greetings": "hello world"\n  }\n}\n...\n```\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
