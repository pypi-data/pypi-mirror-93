from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'Operating System :: POSIX :: Linux',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3',
  'Programming Language :: Python :: 3.4',
  'Programming Language :: Python :: 3.5',
  'Programming Language :: Python :: 3.6',
  'Programming Language :: Python :: 3.7',
  'Programming Language :: Python :: 3.8',
  
]
 
setup(
  name='pythonatinsta',
  version='0.0.1',
  description='A very basic instagram robot',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Nasser B. Al-Ostath',
  author_email='nasser@dotslashhack.io',
  license='MIT', 
  classifiers=classifiers,
  keywords='pythonat', 
  packages=find_packages(),
  )
