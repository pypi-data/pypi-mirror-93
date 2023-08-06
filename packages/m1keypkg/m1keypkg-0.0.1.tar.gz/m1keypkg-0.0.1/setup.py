from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='m1keypkg',
  version='0.0.1',
  description='A very basic introduction',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Mithilesh Tiwari',
  author_email='shubhamtiwari.tiwari84@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='OneML', 
  packages=find_packages(),
  install_requires=[''] 
)