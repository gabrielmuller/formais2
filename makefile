UI = $(wildcard *.ui)

all: test

run:
	python3 main.py

test:
	python3 -m unittest discover tests

# não testei
gui:
	$(foreach file, $(UI), pyuic5 -x $(file) -o $(file).py;)
