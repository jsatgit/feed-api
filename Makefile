.PHONY: start test

start:
	python src/feed.py

test:
	python -m unittest discover
