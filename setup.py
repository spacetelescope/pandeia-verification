from setuptools import setup, find_packages

setup(name='pandeia_verification',
      version='1.7',
      description='Pandeia verification tools',
      author='Klaus Pontoppidan, Adric Riedel',
      author_email='pontoppi@stsci.edu',
      url='http://www.stsci.edu/~pontoppi',
      packages=find_packages(),
      package_data={'verification_tools': ['inputs/*.fits','inputs/*.txt','inputs/*.tab', 'tests/niriss/*.py', 'tests/nircam/*.py', 'tests/miri/*.py', 'tests/nirspec/*.py']}
      )
