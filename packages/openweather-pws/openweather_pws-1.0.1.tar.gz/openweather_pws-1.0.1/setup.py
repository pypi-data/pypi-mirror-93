from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='openweather_pws',
    version='1.0.1',
    description='Open Weather PWS API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['openweather_pws'],
    install_requires=['requests'],
    author='Ilya Vereshchagin',
    author_email='i.vereshchagin@gamil.com',
    url='https://github.com/wwakabobik/openweather_pws',
    zip_safe=False
)
