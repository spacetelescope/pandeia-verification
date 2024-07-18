from setuptools import setup, find_packages

setup(name='pandeia_verification',
      version='4.0',
      description='Pandeia verification tools',
      author='Klaus Pontoppidan, Adric Riedel',
      author_email='etc_team@stsci.edu',
      url='http://www.stsci.edu/~pontoppi',
      packages=find_packages(),
      package_data={'verification_tools': ['inputs/*.fits','inputs/*.txt','inputs/*.tab', 'tests/niriss/*.py', 'tests/nircam/*.py', 'tests/miri/*.py', 'tests/nirspec/*.py']},
      install_requires = [
          "astropy",
          "bokeh",
          "matplotlib",
          "numpy",
          "pandas",
          "pandeia.engine",
          "scipy",
          "setuptools"
      ]
      )
