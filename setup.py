from setuptools import setup

setup(
  name='panadata-api-sdk',
  version='1.0',
  description='SDK for the panadata API',
  author='Gabriel Kardonski',
  author_email='gabriel@panadata.net',
  packages=['panadata-api-sdk'],
  install_requires=['requests', 'unidecode'],
)
