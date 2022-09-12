.PHONY: setup
setup:
	pip install -r requirements.txt

.PHONY: freeze
freeze:
	pip freeze > requirements.txt

.PHONY: clean
clean:
	rm -rf __pycache__