from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
   name='KrishnaCalculator',
   version='0.0.1',
   description='A useful calculator',
   Long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
   url='',
   author ='Krishna Koirala',
   author_email='koiralakp5@gmail.com',
   License = 'MIT',
   classifiers = classifiers,
   keywords='calculation',
   packages=find_packages(),
   install_requires=[''], #external packages as dependencies
)