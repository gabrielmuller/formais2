all: py
pl:
	swipl -s regular.pl nda.pl
py:
	python3 main.py
