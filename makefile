all: test gui

run:
	python3 main.py

test:
	python3 -m unittest discover tests

gui:
	pyuic5 -x window.ui -o window_ui.py
	pyuic5 -x dialog_af.ui -o dialog_af_ui.py
	pyuic5 -x dialog_gr.ui -o dialog_gr_ui.py
	python3 main.py
