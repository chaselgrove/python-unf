# See file COPYING distributed with unf for copyright and license.

default : build

test : 
	python -m unittest -vb tests

build : dist/unf-0.1.0.tar.gz

dist/unf-0.1.0.tar.gz : 
	python setup.py sdist

register : 
	python setup.py register

upload : 
	python setup.py sdist upload

check : 
	python setup.py check

clean : 
	rm -f MANIFEST *.pyc

clobber : clean
	rm -rf dist

# eof
