
from distutils.core import setup

# read the contents of README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
		name='foresee',
		version='0.1.0a4',
		description='Generate forecasts using several time series forecasting models in python.',
		author='Hamid Mohammadi',
		author_email='hmohammadi6545@gmail.com',
		url='https://github.com/HamidM6/foresee',
		packages=['foresee'],
		long_description=long_description,
		long_description_content_type='text/markdown',
	)