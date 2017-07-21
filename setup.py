from setuptools import setup
import codecs
import os


dependencies = [
	'pyserial'
]

dev_dependencies = [
	'pytest',
	'mock',
	'twine',
	'wheel',
	'setuptools'
]

HERE = os.path.abspath(os.path.dirname(__file__))


def read ( *parts ):
	"""
	Build an absolute path from *parts* and and return the contents of the
	resulting file.  Assume UTF-8 encoding.
	"""
	content = ''
	with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
		content = f.read()

	print(content)
	return content


setup(
	name='TMCL',
	version='2.0-alpha.2',
	description='Talk to Trinamic Stepper Motors using TMCL over serial',
	long_description=read("README.rst"),
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

	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
		'Topic :: Communications',
		'Topic :: Software Development :: Libraries',
		'Topic :: Software Development :: Libraries :: Python Modules',
	],

	packages=['TMCL'],

	install_requires=dependencies,

	extras_require={
		'dev': dev_dependencies
	},

	zip_safe=False
)
