# General
setup:
	python -m pip install -r requirements.txt

# For Windows, there is one package difference...
setup-windows:
	python -m pip install -r requirements.txt
	python -m pip uninstall -y python-magic
	python -m pip install python-magic-bin==0.4.14

test:
	python -m pytest

# HECTRE
extract:
	python -m hectre.extract $(file) $(picos)

# Back-end components
be-dev:
	poetry run uvicorn backend.main:app --reload

be-create-items:
	curl -X POST localhost:8000/foo/item/   --data '{"description":"some item description", "public":false}' && echo
	curl -X POST localhost:8000/foo/item/   --data '{"description":"some item description", "public":true}'

be-get-items:
	curl -X GET localhost:8000/foo/item/1 && echo
	curl -X GET localhost:8000/foo/item/2