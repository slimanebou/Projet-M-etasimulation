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

run_example:
	@echo "Exemple d'exécution"
	python automate.py

clean:
	@if exist *.pyc (del /s /q *.pyc 2> nul)
	@if exist __pycache__ (rmdir /s /q __pycache__ 2> nul)
	@if exist regles_test.txt (del /q regles_test.txt 2> nul)
	@echo "Nettoyage termine."