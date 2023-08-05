from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='vasil',
  version='0.0.2',
  description='A very basic pussy',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Grigoriy Skovoroda',
  author_email='SuckME@g.org',
  license='MIT', 
  classifiers=classifiers,
  keywords='vasil', 
  packages=find_packages(),
  install_requires=[''] 
)
