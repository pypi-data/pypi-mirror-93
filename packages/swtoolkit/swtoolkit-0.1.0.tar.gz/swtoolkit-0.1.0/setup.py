# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swtoolkit',
 'swtoolkit.api',
 'swtoolkit.api.enums',
 'swtoolkit.api.errors',
 'swtoolkit.api.interfaces',
 'swtoolkit.api.utils',
 'swtoolkit.utils']

package_data = \
{'': ['*']}

install_requires = \
['psutil>=5.8.0,<6.0.0', 'pywin32>=300,<301']

setup_kwargs = {
    'name': 'swtoolkit',
    'version': '0.1.0',
    'description': 'A SolidWorks Toolkit for Python',
    'long_description': ".. image:: docs/images/logo_swtoolkit.png\n        :alt: SW ToolKit\n        :align: center\n        :width: 600\n\n.. This '|' generates a blank line to avoid sticking the logo to the\n   section.\n\n\n.. image:: https://img.shields.io/pypi/v/swtoolkit.svg?style=flat-square\n        :target: https://pypi.python.org/pypi/swtoolkit\n        :width: 150\n        :alt: PyPi Version\n\n.. image:: docs/images/intro_code.png\n        :alt:\n        :width: 600\n        :align: center\n\nSolidWorks Toolkit for Python\n=============================\n**SW ToolKit** allows you to leverage Python to quickly develop powerful scripts and programs to automate your SolidWorks workflow.\n\n* Free software: MIT license\n\n|Made With Python|\n\n.. |Made With Python| image:: http://ForTheBadge.com/images/badges/made-with-python.svg\n        :target: https://www.python.org/\n        :width: 200\n        :alt: |\n\n|Works on My Machine|\n\n.. |Works on My Machine| image:: https://forthebadge.com/images/badges/works-on-my-machine.svg\n        :target: https://forthebadge.com\n        :width: 200\n        :alt: |\n\n",
    'author': 'Glutenberg',
    'author_email': 'josh@colescanada.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Glutenberg/swtoolkit.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
