# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

PACKAGE_NAME = 'ds-billing-app'
with open('version') as f:
    PACKAGE_VERSION = f.read().strip()

REQUIRED_PACKAGES = [
    'boto',
    'pandas==1.0.1',
    'starlette==0.13.2',
    'numpy==1.18.1',
    'google-cloud-bigquery==1.24.0',
    'python-multipart==0.0.5',
    'xlrd==1.2.0',
    'xlsxwriter==1.2.8'
    #
]

setup(name=PACKAGE_NAME,
      version=PACKAGE_VERSION,
      author='Abhijit Joshi',
      author_email='abhijit.joshi@cbs.com',
      url='https://github.com/cbs-data/k8s-di-apps/ds-backend-billing',
      description='Backend for data science billing app standalone',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      install_requires=REQUIRED_PACKAGES,
      entry_points={
          'console_scripts': [
              'ds-billing-app = app:main',
          ],
      })
# vim: ts=4:sw=4:ft=python
