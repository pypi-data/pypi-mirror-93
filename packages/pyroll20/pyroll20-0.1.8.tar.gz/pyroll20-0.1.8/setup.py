from setuptools import setup, find_packages

f = open("README.md", "r")
setup(
    name='pyroll20',
    version='0.1.8',
    packages=find_packages(),
    url='https://github.com/NoPantsCrash/pydice',
    license='GNU GENERAL PUBLIC LICENSE v3',
    author='george',
    author_email='abtziangiorgos@gmail.com',
    description='A light, Roll20 syntax compatible, python dice roller',
    long_description=f.read(),
    long_description_content_type='text/markdown'
)
