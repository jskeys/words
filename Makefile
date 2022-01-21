build:
	python3 -m build

install:
	python3 -m pip install dist/*.whl

format:
	python3 -m black words

setup:
	python3 -m pip install -r requirements.txt

clean:
	rm -rf dist
	find . -name "*.egg-info" -exec rm -rv {} +


