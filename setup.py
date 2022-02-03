from setuptools import setup

setup(
  name='panadata_api_sdk',
  version='1.0',
  description='SDK for the panadata API',
  author='Gabriel Kardonski',
  author_email='gabriel@panadata.net',
  packages=['panadata_api_sdk'],
  install_requires=['requests', 'unidecode'],
)
