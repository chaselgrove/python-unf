# See file COPYING distributed with unf for copyright and license.

from distutils.core import setup

long_description = open('README.rst').read()

setup(name='unf', 
      version='0.5.1', 
      description='Universal Numeric Fingerprints', 
      author='Christian Haselgrove', 
      author_email='christian.haselgrove@umassmed.edu', 
      url='https://github.com/chaselgrove/python-unf', 
      py_modules=['unf'], 
      classifiers=['Development Status :: 3 - Alpha', 
                   'Environment :: Console', 
                   'Intended Audience :: Science/Research', 
                   'License :: OSI Approved :: BSD License', 
                   'Operating System :: OS Independent', 
                   'Programming Language :: Python', 
                   'Topic :: Scientific/Engineering'], 
      license='BSD license', 
      long_description=long_description
     )

# eof
