all: test

run:
	python3 main.py

test:
	python3 -m unittest discover tests

gui:
	pyuic5 -x window.ui -o window_ui.py
	python3 main.py
