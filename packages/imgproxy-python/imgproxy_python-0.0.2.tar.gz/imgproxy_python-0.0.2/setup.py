# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imgproxy_python']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'imgproxy-python',
    'version': '0.0.2',
    'description': 'A tiny library to simplify generation of imgproxy urls',
    'long_description': "[![Build Status](https://travis-ci.com/rapIsKal/imgproxy-python.svg?branch=main)](https://travis-ci.com/rapIsKal/imgproxy-python)\n![PyPI](https://img.shields.io/pypi/v/imgproxy_python)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/imgproxy_python)](https://pypi.org/project/imgproxy_python/)\n\n\n# imgproxy_python\nA tiny library to simplify generation of imgproxy urls\n\n# installation\n```\npip install imgproxy_python\n```\n\n# usage\nFor example you want to simply resize your image to other height and width using imgproxy. To get proper imgproxy url you need the following\n```\nfrom imgproxy_python.urls import UrlGenerator\nconfig = {\n        'imgproxy_key': '943b421c9eb07c830af81030552c86009268de4e532ba2ee2eab8247c6da0881',\n        'imgproxy_salt': '520f986b998545b4785e0defbc4f3c1203f22de2374a3d53cb7a7fe9fea309c5',\n        'imgproxy_host': 'http://localhost:8000',\n        'options': {\n            'resize': 'fill',\n            'width': 300,\n            'height': 300,\n        }\n    }\n    url = 'http://img.example.com/pretty/image.jpg'\n    urlgen = UrlGenerator(url, config)\n    print(urlgen.get_full_signed_url())\n```\nYou will get a ready-to-go imgproxy link\n```\nhttp://localhost:8000/6cy4IRuQ1nQW8qGVmNvPdynjmkuwUEx-XhGw_C_kQmA/fill/300/300/ce/0/aHR0cDovL2ltZy5l/eGFtcGxlLmNvbS9w/cmV0dHkvaW1hZ2Uu/anBn\n```\n\n# warning\n\nIf you want to have generated link working you need to have imgproxy instance up and running on ```config['imgproxy_host']```, in our example it is ```http://localhost:8000```\n\n# diclaimer\n\nfor now only basic urls are supported in version 0.0.1. Advanced url generation is coming\n",
    'author': 'Vladislav_Gorelov',
    'author_email': 'rap-is-kal-again@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
