from setuptools import setup
f = open("README.md", "r")
setup(
    name='pyroll20',
    version='0.1.3',
    packages=[],
    url='https://github.com/NoPantsCrash/pydice',
    license='GNU GENERAL PUBLIC LICENSE v3',
    author='george',
    author_email='abtziangiorgos@gmail.com',
    description='A light, Roll20 syntax compatible, python dice roller',
    long_description=f.read(),
    long_description_content_type='text/markdown'
)
