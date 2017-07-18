from setuptools import setup

setup(name='TMCL',
	version='1.2',
	description='Talk to Trinamic Stepper Motors using TMCL over serial',
	url='https://github.com/NativeDesign/python-tmcl',
	author='Alan Pich',
	author_email='alanp@native.com',
	license='MIT',
	packages=['TMCL'],
	install_requires=[
		'pyserial'
	],
	keywords = [
		'tmcl',
	    'trinamic',
		'rs485',
		'stepper',
		'motor',
		'tmcm'
	],
	zip_safe=False)
