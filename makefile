UI = $(wildcard *.ui)

all: test

run:
	python3 main.py

test:
	python3 -m unittest discover tests

# não testei
# não sei arrumar mas os arquivos nao podem terminar em ".ui.py"
gui:
	#$(foreach file, $(UI), pyuic5 -x $(file) -o $(file).py;)
	pyuic5 -x window.ui -o window_ui.py
