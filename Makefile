# See file COPYING distributed with unf for copyright and license.

default : build

test : 
	python3 -m unittest -vb tests

build : dist/unf-0.6.0.tar.gz

dist/unf-0.6.0.tar.gz : 
	python3 setup.py sdist

register : 
	python3 setup.py register

upload : 
	python3 setup.py sdist upload

check : 
	python3 setup.py check

clean : 
	rm -f MANIFEST *.pyc

clobber : clean
	rm -rf dist

# eof
