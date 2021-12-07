# See file COPYING distributed with unf for copyright and license.

.PHONY : build

default : build

test : 
	python3 -m unittest -vb tests

build : 
	python3 -m build

upload : build
	python3 -m twine upload dist/*

upload-test : build
	python3 -m twine upload --repository testpypi dist/*

clean : 
	rm -rf __pycache__ unf.egg-info *.pyc

clobber : clean
	rm -rf dist

# eof
