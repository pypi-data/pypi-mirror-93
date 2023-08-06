# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apminsight',
 'apminsight.collector',
 'apminsight.config',
 'apminsight.contrib',
 'apminsight.contrib.django',
 'apminsight.instrumentation',
 'apminsight.instrumentation.packages',
 'apminsight.metric']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'apminsight-site24x7-py',
    'version': '1.0.0',
    'description': 'site24x7 monitoring package',
    'long_description': "Python Application Performance Monitoring\n=========================================\n\nMonitor and optimize your Python application performance with a Site24x7 APM Insight Python agent. The agent provides you information on your application's response time, throughput, database operations, and errors. Track these metrics over time to identify where to optimize them for enhanced performance.\n\nBefore you can use an APM Insight agent to monitor metrics, ensure that you have a Site24x7 account.\n\nRequirements : Python version 3.8 and above\n\nSupported frameworks : Django, Flask\nSupported components : pymysql, psycopg2, pymemcache, redis, sqlite, jinja\n\n**Installation**\n\n* Install APM Insight Python agent using pip or poetry\n\n        pip install apminsight-site24x7-py\n        poetry add apminsight-site24x7-py\n\n* For Django applications, add **apminsight.contrib.django** as the first of **INSTALLED_APPS** in django settings.py\n\n* For Flask applications, add **import apminsight** in the first line of main file\n\n* Add the license key in environment **S247_LICENSE_KEY** as well as **APM_APP_NAME** and **APM_APP_PORT**\n\n        export S247_LICENSE_KEY=<license-key>\n        export APM_APP_NAME=<your-app-name>\n        export APM_APP_PORT=<your-app-port>\n",
    'author': 'Wealize',
    'author_email': 'ops@wealize.digital',
    'maintainer': 'Wealize',
    'maintainer_email': 'ops@wealize.digital',
    'url': 'https://github.com/Wealize/apminsight-site24x7-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
