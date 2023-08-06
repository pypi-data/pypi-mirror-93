from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='karmared-api',
      version='0.0.3',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/Karma-blockchain/karmared-api',
      author='Nozdrin-Plotnitsky Nikolay',
      author_email='nozdrin.plotnitsky@karma.red',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          "aiohttp",
          "graphql-core>=3"
      ])
