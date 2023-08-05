# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_splitted_input']

package_data = \
{'': ['*'],
 'django_splitted_input': ['static/django_splitted_input/css/*',
                           'static/django_splitted_input/js/*',
                           'templates/django_splitted_input/*']}

install_requires = \
['Django>=3.1,<4.0']

setup_kwargs = {
    'name': 'django-splitted-input',
    'version': '0.1.1',
    'description': 'A widget to have a django text input splitted into multiple HTML inputs.',
    'long_description': '# django_splitted_input\n\n## About\n\nThis is a django widget for multiple fixed size inputs for one form field. These could be used for those super fancy\nverification code forms. The cursor is moved to the next input field using JS/jQuery.\n\n![django_splitted_input Showcase](django_splitted_input_showcase.png)\n\n## Usage\n\n1. Install `django_splitted_input` and add it to your `INSTALLED_APPS`.\n   ```shell\n   pip install django-splitted-input\n   ```\n   In your settings.py:\n   ```python\n   "django_splitted_input",\n   ```\n2. Install `jQuery` using your preferred method (e.g.\n   [django-yarnpkg](https://pypi.org/project/django-yarnpkg/))\n   \n3. Create a form with a `CharField`.\n4. Use `SplittedInput` as a widget and supply the sizes of all input fields.\n\n```python\nfrom django import forms\nfrom django_splitted_input import SplittedInput\n\n\nclass VerificationForm(forms.Form):\n    auth_code = forms.CharField(label=\'Code\', widget=SplittedInput(sizes=(3, 3, 3)))\n```\n\n',
    'author': 'Julian Leucker',
    'author_email': 'leuckerj@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://edugit.org/AlekSIS/libs/django-splitted-input',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
