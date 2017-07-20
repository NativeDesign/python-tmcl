from setuptools import setup


dependencies = [
	'pyserial'
]

dev_dependencies = [
	'pytest',
	'mock'
]


setup(
	name='TMCL',
	version='2.0',
	description='Talk to Trinamic Stepper Motors using TMCL over serial',
	url='https://github.com/NativeDesign/python-tmcl',
	author='Alan Pich',
	author_email='alanp@native.com',
	license='MIT',
	keywords=[
		'tmcl',
		'trinamic',
		'rs485',
		'stepper',
		'motor',
		'tmcm'
	],

	packages=['TMCL'],

	install_requires = dependencies,

	extras_require={
		'dev': dev_dependencies
	},

	zip_safe=False
)
