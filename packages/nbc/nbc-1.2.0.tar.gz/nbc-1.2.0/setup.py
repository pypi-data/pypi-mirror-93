from setuptools import setup, find_packages


with open('README.md') as fin:
    long_description = fin.read()


setup(
    name='nbc',
    version='1.2.0',
    author='v01d',
    author_email='v01dmain@aol.com',
    description='Number Base Converter',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/v01d-gl/number-base-converter',
    license='MIT',
    packages=find_packages(),
)
