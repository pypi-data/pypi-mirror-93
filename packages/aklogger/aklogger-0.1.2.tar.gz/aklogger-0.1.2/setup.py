# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aklogger']

package_data = \
{'': ['*']}

install_requires = \
['slacker>=0.14.0,<0.15.0']

setup_kwargs = {
    'name': 'aklogger',
    'version': '0.1.2',
    'description': 'A generic logging package for python projects',
    'long_description': "# aklogger\n\nKeep track of all the events happening in your project: A generic logging package for python projects.\n\n## [Features]\n\n- Logging to console\n- Logging to file\n- Push logs to slack\n\n## Installation\n\n```\n$ pip install aklogger\n```\n\n## Usage\n\nFollowing script will log messages to slack, file and console:\n\n```python\nfrom aklogger import logger\n\nlogger.set_name('mycroft')\nlogger.setLevel('DEBUG')\n\n# This will log to console\nlogger.info('Some Dummy log', 'Some dummy details of the dummy log')\n\n# Enable File log\nlogger.log_to_file('file.log')\n\n# This will log to file and console\nlogger.info('Some Dummy log', 'Some dummy details of the dummy log')\n\n# Enable Slack\nlogger.enable_slack(SLACK_TOKEN)\n\n# Set slack level\nlogger.set_slack_level('WARNING')\n\n# Now the logs will be log to slack\nlogger.warning('Some Dummy log', 'Some dummy details of the dummy log')\n\n# You can also do a force push to slack no matter what the slack level is set.\nlogger.info('Dummy log', 'Details of the dummy log', force_push_slack=True)\n```\n\nSee [python logging docs](https://docs.python.org/3/library/logging.html) for more uses.\n",
    'author': 'Appknox',
    'author_email': 'engineering@appknox.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/appknox/aklogger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
