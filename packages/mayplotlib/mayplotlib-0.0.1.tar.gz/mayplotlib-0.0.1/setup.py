from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='mayplotlib',
  version='0.0.1',
  description='A very basic exam library',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type='text/markdown',
  url='https://github.com/singh-yashwant/mayplotlib',  
  author='Binod Kumar',
  author_email='ilikehits1999@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='exams', 
  packages=find_packages(),
  install_requires=[''] 
)