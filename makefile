UI = $(wildcard *.ui)

all: run

run:
	python3 main.py

test:
	python3 -m unittest discover tests

gui:
	pyuic5 -x window.ui -o window_ui.py
