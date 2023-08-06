# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mongoengine_arrow']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.17.0,<0.18.0', 'mongoengine>=0.22.1,<0.23.0']

setup_kwargs = {
    'name': 'mongoengine-arrow',
    'version': '0.1.2',
    'description': 'Arrow datetime support for MongoEngine',
    'long_description': '# mongoengine-arrow\n\n## Description\n\n[Arrow](https://github.com/arrow-py/arrow) datetime support for [MongoEngine](https://github.com/MongoEngine/mongoengine)\n\n## Install\n\n```bash\npip3 install --upgrade mongoengine-arrow\n```\n\n## How it works\n\nFeed it datetime with or without timezone info in any format Arrow supports.\nTo confirm whether it will work, feed it to `arrow.get()` function.\n\n## Usage example\n\n```python3\n# Import the field\nfrom mongoengine_arrow import ArrowDateTimeField\n\n...\n\n# Define model\nclass MyModel(Document):\n    timestamp = ArrowDateTimeField(required=True)\n\n...\n\n# Get instance\nmyinstance = MyModel.objects.first()\n\n# Get timestamp in local time\ntimestamp = myinstance.timestamp.to("local")\n\n# Set timestamp in any timezone\nmyinstance.timestamp = arrow.get(2021, 1, 1, tzinfo="UTC")\n\n# Set timestamp from datetime\nfrom datetime import datetime\nmyinstance.timestamp = datetime(2021, 1, 1)\n\n# Set timestamp from datetime that has tzinfo\nfrom datetime import datetime\nfrom dateutil.tz import gettz\nmyinstance.timestamp = datetime(2021, 1, 1, tzinfo=gettz("UTC+5"))\n```\n',
    'author': 'Niko Järvinen',
    'author_email': 'nbjarvinen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/b10011/arrow-mongoengine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
