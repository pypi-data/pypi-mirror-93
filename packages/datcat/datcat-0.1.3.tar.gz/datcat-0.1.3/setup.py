# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datcat', 'datcat.adapters', 'datcat.domain', 'datcat.entrypoints']

package_data = \
{'': ['*']}

install_requires = \
['Flask-API>=2.0,<3.0', 'Flask>=1.1.2,<2.0.0', 'python-decouple>=3.4,<4.0']

entry_points = \
{'console_scripts': ['create_mappings = helpers:create_mappings',
                     'datcat = datcat.entrypoints.flask_app:main']}

setup_kwargs = {
    'name': 'datcat',
    'version': '0.1.3',
    'description': 'Simple Data Catalogue API',
    'long_description': '## DatCat\nSimple data catalogue api.\nPlease note this is an alpha version and still in active development.\n\n###Convensions\nLocation: /datcat/catalogue/schemas \\\nFiletype: .json \\\nNaming: your_schema_name_v1.json \\\nPlatform: bigquery\n\n###Format of a Simple Schema\n```json\n[\n  {\n    "description": "Unique Identifier",\n    "mode": "REQUIRED",\n    "name": "MY_UNIQUE_ID",\n    "type": "INT64"\n  },  {\n    "description": "Favourite Colour",\n    "mode": "REQUIRED",\n    "name": "MY_FAVOURITE_COLOUR",\n    "type": "STRING"\n  }\n]\n```\n\n### .env.example\n```bash\n#settings\nSCHEMAS_PATH=catalogue/schemas\nMETADATA_PATH=catalogue/metadata\nMAPPINGS_FILEPATH=catalogue/mappings/schema_topic_subscription.json\n\nCATALOGUE_SCHEME=http\nCATALOGUE_HOST=0.0.0.0\nCATALOGUE_PORT=50000\nCATALOGUE_DEBUG=False\n```\n### Build and Run it Inside a Docker Container Example\n\n```bash\nsource .env\npoetry build --format wheel\ndocker build --tag dc .\ndocker run --hostname datcat \\\n  --env-file .env \\\n  --publish "${CATALOGUE_PORT}":"${CATALOGUE_PORT}" \\\n  --detach dc:latest\n```\n\nNow go to: http://0.0.0.0.8080 to see it\n\n### Test Coverage\n```bash\npytest --cov=. tests/ | grep -v .env\n```\n',
    'author': 'Antonio',
    'author_email': 'antonio.one@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/antonio-one/datcat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
