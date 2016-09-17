try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Allocate project partners based on diversity',
    'author': 'Peter Adam',
    'url': 'https://github.com/Padam-0/project-partners',
    'download_url': 'https://github.com/Padam-0/project-partners',
    'author_email': 'peter.adam@ucdconnect.ie',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['projpartners'],
    'scripts': [],
    'name': 'Project Partners'
}

setup(**config)
