from setuptools import setup

setup(name='TMCL',
      version='1.0',
      description='Talk to Trinamic Stepper Motors using TMCL over serial',
      url='https://github.com/NativeDesign/python-tmcl',
      author='Alan Pich',
      author_email='alanp@native.com',
      license='MIT',
      packages=['TMCL'],
      install_requires=[
        'pyserial'
      ],
      zip_safe=False)
