Python Application Performance Monitoring
=========================================

Monitor and optimize your Python application performance with a Site24x7 APM Insight Python agent. The agent provides you information on your application's response time, throughput, database operations, and errors. Track these metrics over time to identify where to optimize them for enhanced performance.

Before you can use an APM Insight agent to monitor metrics, ensure that you have a Site24x7 account.

Requirements : Python version 3.8 and above

Supported frameworks : Django, Flask
Supported components : pymysql, psycopg2, pymemcache, redis, sqlite, jinja

**Installation**

* Install APM Insight Python agent using pip or poetry

        pip install apminsight-site24x7-py
        poetry add apminsight-site24x7-py

* For Django applications, add **apminsight.contrib.django** as the first of **INSTALLED_APPS** in django settings.py

* For Flask applications, add **import apminsight** in the first line of main file

* Add the license key in environment **S247_LICENSE_KEY** as well as **APM_APP_NAME** and **APM_APP_PORT**

        export S247_LICENSE_KEY=<license-key>
        export APM_APP_NAME=<your-app-name>
        export APM_APP_PORT=<your-app-port>
