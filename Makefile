build:
	python3 -m build

install:
	python3 -m pip install dist/*.whl

setup:
	python3 -m pip install -r requirements.txt

clean:
	rm -rf dist *.egg-info
