# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pigeon', 'pigeon.url']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2']

setup_kwargs = {
    'name': 'django-pigeon',
    'version': '0.4.0',
    'description': 'Test utilities for Django projects.',
    'long_description': "# django-pigeon\n#### Test utilities for Django projects\n\n[![Build Status](https://travis-ci.org/RevolutionTech/django-pigeon.svg?branch=master)](https://travis-ci.org/RevolutionTech/django-pigeon)\n[![codecov](https://codecov.io/gh/RevolutionTech/django-pigeon/branch/master/graph/badge.svg)](https://codecov.io/gh/RevolutionTech/django-pigeon)\n[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c1add1fd523c4bb48a6e5158cdffa1dd)](https://www.codacy.com/app/RevolutionTech/django-pigeon)\n\n## Installation\n\n```\n$ pip install django-pigeon\n```\n\n## Usage\n\ndjango-pigeon comes equipped with a `RenderTestCase` which provides an assortment of methods on top of Django's `TestCase` that assist with end-to-end testing of views in Django. Writing a test that verifies a view renders correctly is as simple as:\n\n```python\nfrom pigeon.test import RenderTestCase\n\n\nclass FooTestCase(RenderTestCase):\n\n    def testFooView(self):\n        self.assertResponseRenders('/foo/')\n```\n\nYou can also inspect the rendered response:\n\n```python\ndef testFooView(self):\n    response = self.assertResponseRenders('/foo/')\n    self.assertIn('FOO', response.content)\n```\n\nBy default, `assertResponseRenders` verifies that the status code of the response is 200, but you can change this by specifying the `status_code` keyword argument:\n\n```python\ndef testBarView404(self):\n    self.assertResponseRenders('/bar/', status_code=404)\n```\n\nYou can also make POST and PUT requests using `assertResponseRenders` by providing the `method` and `data` keywords arguments:\n\n```python\ndef testCreateFooView(self):\n    payload = {'text': 'Hello World!'}\n    self.assertResponseRenders('/foo/create/', status_code=201, method='POST', data=payload)\n```\n\nIf you are using HTML generated from Django forms, you can set `has_form_error=True` as a shortcut to check for `errorlist` in the resulting HTML:\n\n```python\ndef testCreateFooViewWithoutText(self):\n    response = self.assertResponseRenders('/foo/create/', method='POST', has_form_error=True)\n    self.assertIn('This field is required.', response.content)\n```\n\nUse `assertAPIResponseRenders` for JSON responses. `json.loads` is automatically called on the response, so the object returned is ready for inspection:\n\n```python\ndef testFooAPIView(self):\n    payload = {'text': 'Hello!'}\n    response = self.assertAPIResponseRenders('/foo/', method='POST', data=payload)\n    self.assertEquals(response['text'], 'Hello!')\n```\n\nYou can use `assertResponseRedirects` to test redirects:\n\n```python\ndef testFooRedirects(self):\n    # /foo/ redirects to /bar/\n    self.assertResponseRedirects('/foo/', '/bar/')\n```\n\nIf you have a list of views that you want to verify are rendering as 200 without adding any special assertion logic, you can simply override the `get200s` and `getAPI200s` methods, which should return a list of URLs. django-pigeon will construct test methods that check that rendering all of these URLs results in a 200:\n\n```python\nclass FooTestCase(RenderTestCase):\n\n    def get200s(self):\n        return [\n            '/foo/',\n            '/bar/',\n            '/foobar/',\n        ]\n\n    def getAPI200s(self):\n        return [\n            '/api/foo/',\n        ]\n```\n\nMost of the features in `RenderTestCase` are actually implemented in the mixin class `RenderTestCaseMixin`. You can combine `RenderTestCaseMixin` with other TestCase classes to get additional functionality:\n\n```python\nfrom django.test import TransactionTestCase\nfrom pigeon.test import RenderTestCaseMixin\n\n\nclass FooTransactionTestCase(RenderTestCaseMixin, TransactionTestCase):\n\n    def testFooView(self):\n        ...\n```\n\ndjango-pigeon supports Python 3.5+ and Django 2.2+.\n",
    'author': 'Lucas Connors',
    'author_email': 'lucas@revolutiontech.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/RevolutionTech/django-pigeon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
