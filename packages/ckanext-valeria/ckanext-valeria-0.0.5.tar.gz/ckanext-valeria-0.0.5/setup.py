# encoding: utf-8

import io
import os.path
import re

from setuptools import setup, find_packages


# Extract version
HERE = os.path.abspath(os.path.dirname(__file__))
INIT_PY = os.path.join(HERE, 'ckanext', 'valeria', '__init__.py')
version = None
with io.open(INIT_PY) as f:
    for line in f:
        m = re.match(r'__version__\s*=\s*u?[\'"](.*)[\'"]', line)
        if m:
            version = m.groups()[0]
            break
if version is None:
    raise RuntimeError('Could not extract version from "{}".'.format(INIT_PY))


setup(
    name='ckanext-valeria',
    version=version,
    description='Valeria Theme',
    long_description='',
    keywords='CKAN THEME',
    author='Dave Berthiaume',
    author_email='dave.berthiaume@dti.ulaval.ca',
    url='https://catalogue.valeria.science/',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext'],
    include_package_data=True,
    package_data={
            '': ['theme/*/*.html', 'theme/*/*/*.html', 'theme/*/*/*/*.html'],
    },
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points=\
    """
        [ckan.plugins]
        valeria=ckanext.valeria.plugin:ValeriaPlugin
        [babel.extractors]
        ckan = ckan.lib.extract:extract_ckan
    """,
    message_extractors={
        'ckanext': [
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('**/pages/theme/**.html', 'ckan', None),
        ],
    },
)