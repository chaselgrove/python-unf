# See file COPYING distributed with unf for copyright and license.

default : build

test : 
	python3 -m unittest -vb tests

build : 
	python3 -m build

clean : 
	rm -rf __pycache__ unf.egg-info

clobber : clean
	rm -rf dist

# eof
