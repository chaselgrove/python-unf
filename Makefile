# See file COPYING distributed with python-unf for copyright and license.

.PHONY : build

default : build

test : build
	tox -e py3

test_all : build
	tox

build : 
	python3 -m build

upload : build
	python3 -m twine upload dist/*

upload-test : build
	python3 -m twine upload --repository testpypi dist/*

clean : 
	rm -rf __pycache__ unf.egg-info *.pyc

clobber : clean
	rm -rf dist .tox

# eof
