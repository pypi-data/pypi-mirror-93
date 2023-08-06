# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['frontman']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.3,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['frontman = frontman.main:app']}

setup_kwargs = {
    'name': 'frontman',
    'version': '0.1.0',
    'description': 'Frontend libraries manager',
    'long_description': '# FrontMan\n\nTool to help manage frontend dependencies (javascript, css)\n\nInspired by dotnet LibMan\n\n## Usage\n\n1. Create the manifest file `frontman.json`\n\n```json\n{\n  "provider": "jsdelivr",\n  "destination": "assets",\n  "packages": [\n    {\n      "name": "jquery",\n      "version": "3.5.1",\n      "provider": "cdnjs",\n      "files": [\n        {\n          "name": "jquery.min.js",\n          "destination": "jquery"\n        }\n      ]\n    },\n    {\n      "name": "@popperjs/core",\n      "version": "2.6.0",\n      "path": "dist/umd",\n      "destination":"popper",\n      "files": [\n        {\n          "name": "popper.min.js",\n          "rename": "popper.js"\n        }\n      ]\n    },\n    {\n      "name": "bootstrap",\n      "version": "4.6.0",\n      "path": "dist",\n      "destination": "bootstrap",\n      "files": [\n        "js/bootstrap.min.js",\n        "css/bootstrap.min.css"\n      ]\n    }\n  ]\n}\n```\n\n2. Execute FrontMan\n\n```shell\nfrontman\n```\n\nYou should see an output like this:\n\n```\nOK  https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js -> frontman/assets/jquery/jquery.min.js\nOK  https://cdn.jsdelivr.net/npm/@popperjs/core@2.6.0/dist/umd/popper.min.js -> assets/popper/popper.js\nOK  https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/js/bootstrap.min.js -> assets/bootstrap/js/bootstrap.min.js\nOK  https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css -> assets/bootstrap/css/bootstrap.min.css\n```',
    'author': 'Livio Ribeiro',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
