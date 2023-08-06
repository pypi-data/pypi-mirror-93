from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='C GPU',
  version='0.0.1',
  description='Mini virtual GPU made with the curses module!',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Brandon Cannistraci',
  author_email='fixerboy2009@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='GPU', 
  packages=find_packages(),
  install_requires=[''] 
)