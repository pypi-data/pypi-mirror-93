# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gapi_helper',
 'gapi_helper.drive',
 'gapi_helper.mail',
 'gapi_helper.sheets',
 'gapi_helper.tasks']

package_data = \
{'': ['*']}

install_requires = \
['Flask-SQLAlchemy>=2.4.4,<3.0.0',
 'Flask>=1.1.2,<2.0.0',
 'google-api-python-client>=1.11.0,<2.0.0',
 'oauth2client>=4.1.3,<5.0.0',
 'simpletasks-data>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'gapi-helper',
    'version': '0.2.0',
    'description': 'Helpers around Google APIs',
    'long_description': '# gapi-helper\n\nHelpers around Google APIs:\n- [Google Drive API](gapi_helper/drive/README.md)\n- [Google Mail API](gapi_helper/mail/README.md)\n- [Google Sheets API](gapi_helper/sheets/README.md)\n\nAlso provides new classes for [simpletasks-data](https://github.com/upOwa/simpletasks-data):\n- `DumpTask` to dump a [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) model into a Google Sheet\n- `TransferTask` to write arbitrary data to a Google Sheet\n  - `TransferCsvTask` to write CSV data to a Google Sheet\n  - `TransferSheetTask` to write a Google Sheet to another Google Sheet\n- `ImportSheet` to use a Google Sheet as source for `ImportTask`\n\n## Contributing\n\nTo initialize the environment:\n```\npoetry install --no-root\n```\n\nTo run tests (including linting and code formatting checks), please run:\n```\npoetry run pytest --mypy --flake8 && poetry run black --check .\n```\n',
    'author': 'Thomas Muguet',
    'author_email': 'thomas.muguet@upowa.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/upOwa/gapi-helper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
