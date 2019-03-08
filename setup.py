# !/uer/bin/env python3

import re
import ast
from setuptools import setup, find_packages

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('base/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='AT-M',
    version=version,
    url='https://github.com/medivhXu/AT-interface',
    license='Apache License 2.0',
    author='Medivh Xu',
    author_email='medivh_xu@outlook.com',
    description='接口自动化框架',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['requests', 'pymysql', 'pyyaml', 'parameterized', 'pyDes', 'ruamel.yaml'],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.7.1',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries ::Testing'
    ]
)
