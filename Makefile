
.PHONY: all, format

app=NoFileYet

all:
	echo make f | p | c

p:
	python ${app}

c:
	cq-editor ${app}

t:
	pytest

f:
	isort *.py
	black *.py
	flake8 *.py
	mypy *.py
