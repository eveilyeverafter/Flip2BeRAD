try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Flip2BeRAD',
    'author': 'Tyler Hether',
    'url': 'https://github.com/tylerhether/Flip2BeRAD',
    'download_url': 'https://github.com/tylerhether/Flip2BeRAD',
    'author_email': 'tyler [dot] hether [at] gmail [dot, ...]',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['Flip2BeRAD'],
    'scripts': [],
    'name': 'Flip2BeRAD'
}

setup(**config)
