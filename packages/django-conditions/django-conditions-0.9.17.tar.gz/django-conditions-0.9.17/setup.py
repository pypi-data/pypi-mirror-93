# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['conditions']

package_data = \
{'': ['*'],
 'conditions': ['static/conditions/img/*',
                'static/conditions/js/*',
                'templates/conditions/*']}

install_requires = \
['Django>=2.2,<3.2a0', 'django-jsonfield>=1.1,<2.0']

setup_kwargs = {
    'name': 'django-conditions',
    'version': '0.9.17',
    'description': 'A Django app that allows creation of conditional logic in admin.',
    'long_description': '# django-conditions\n\n[![Build Status](https://travis-ci.org/RevolutionTech/django-conditions.svg?branch=master)](https://travis-ci.org/RevolutionTech/django-conditions)\n[![codecov](https://codecov.io/gh/RevolutionTech/django-conditions/branch/master/graph/badge.svg)](https://codecov.io/gh/RevolutionTech/django-conditions)\n[![Codacy Badge](https://api.codacy.com/project/badge/Grade/8fccc57f17e44c5496a912adc691fc39)](https://www.codacy.com/app/RevolutionTech/django-conditions)\n[![Dependency Status](https://www.versioneye.com/user/projects/56de7e4cdf573d0048dafc52/badge.svg?style=flat)](https://www.versioneye.com/user/projects/56de7e4cdf573d0048dafc52)\n[![Documentation Status](https://readthedocs.org/projects/django-conditions/badge/?version=latest)](http://django-conditions.readthedocs.org/en/latest/)\n\nMove conditional logic that changes often from code into models so that the logic can be easily modified in admin. Some possible use cases:\n- Segment your user base into cohorts with targeted messaging\n- Provide different rewards to users depending on their expected value\n- In a game, define the winning objectives of a mission/quest\n- and many more...\n\n## Installation\n\nFirst install the `django-conditions` package:\n\n    pip install django-conditions\n\nThen add `conditions` to your `INSTALLED_APPS` setting:\n\n```python\n## settings.py\nINSTALLED_APPS = [\n    ...\n    \'conditions\',\n]\n```\n\n## Basic Usage\n\nStart by defining a condition in code:\n\n```python\n## condition_types.py\nfrom conditions import Condition\n\nclass FullName(Condition):\n    # The name that appears in the db and represents your condition\n    condstr = \'FULL_NAME\'\n\n    # Normal conditions define eval_bool, which takes in a user\n    # and returns a boolean\n    def eval_bool(self, user, **kwargs):\n        return bool(user.first_name and user.last_name)\n```\n\nThen add a ConditionsField to your model:\n\n```python\n## models.py\nfrom django.db import models\nfrom conditions import ConditionsField, conditions_from_module\nimport condition_types\n\nclass Campaign(models.Model):\n    text = models.TextField()\n\n    # The ConditionsField requires the definitions of all possible conditions\n    # conditions_from_module can take an imported module and sort this out for you\n    target = ConditionsField(definitions=conditions_from_module(condition_types))\n```\n\nIn the model\'s change form on admin, you can enter JSON to represent when you want your condition to be satisfied.\n\n```javascript\n{\n    "all": ["FULL_NAME"]\n}\n```\n\nNow you can use the logic you created in admin to determine the outcome of an event:\n\n```python\n## views.py\nfrom django.http import HttpResponse\nfrom conditions import eval_conditions\nfrom models import Campaign\n\ndef profile(request):\n    for campaign in Campaign.objects.all():\n        if eval_conditions(campaign, \'target\', request.user):\n            return HttpReponse(campaign.text)\n\n    return HttpResponse("Nothing new to see.")\n```\n\nUse django-conditions in your Django projects to change simple logic without having to re-deploy, and pass on the power to product managers and other non-engineers.\n\n## More Information\n\nFull documentation is available [on Read The Docs](http://django-conditions.readthedocs.org/).\n',
    'author': 'Lucas Connors',
    'author_email': 'lucas@revolutiontech.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/RevolutionTech/django-conditions',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
