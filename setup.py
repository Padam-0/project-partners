try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Allocate project partners based on diversity',
    'author': 'Peter Adam',
    'url': 'https://github.com/Padam-0/project-partners',
    'download_url': 'Where to download it.',
    'author_email': 'peter.adam02@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'projectname'
}

setup(**config)
