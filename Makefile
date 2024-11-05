# See file COPYING distributed with python-unf for copyright and license.

.PHONY : default test test_all test_local build upload upload-test spell clean clobber

default : build

test : build
	tox -e py3,no-optional-packages run

test_all : build
	tox run

test_local : 
	python3 -m unittest -vb tests

build : 
	python3 -m build

upload : build
	python3 -m twine upload dist/*

upload-test : build
	python3 -m twine upload --repository testpypi dist/*

spell : 
	spell README.md ROUNDING.md CHANGES

clean : 
	rm -rf __pycache__ unf.egg-info *.pyc

clobber : clean
	rm -rf dist .tox

# eof
