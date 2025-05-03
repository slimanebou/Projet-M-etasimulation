.PHONY: tests clean all run_example

all: run_example

tests:
	python tests.py

test_q1:
	python tests.py q1

test_q2:
	python tests.py q2

test_q3:
	python tests.py q3

test_q4:
	python tests.py q4

test_q5:
	python tests.py q5

test_q6:
	python tests.py q6

test_q7:
	python tests.py q7

test_q8:
	python tests.py q8

test_q9:
	python tests.py q9

test_q10:
	python tests.py q10

test_q11:
	python tests.py q11

test_q12:
	python tests.py q12



run_example:
	@echo "Exemple d'execution"
	python automate.py

clean:
	@if exist *.pyc (del /s /q *.pyc 2> nul)
	@if exist __pycache__ (rmdir /s /q __pycache__ 2> nul)
	@if exist regles_test.txt (del /q regles_test.txt 2> nul)
	@echo "Nettoyage termine."