# General
vsetup:
	python3 -m venv .venv
	source .venv/bin/activate
	python3 -m pip install -r requirements.txt

setup:
	python3 -m pip install -r requirements.txt

test:
	python3 -m pytest

measure-accuracy:
	python3 -m hectre.metrics.accuracy \
		$(path_to_pdf) \
		$(picos_string) \
		$(path_to_cdf)

measure-ad-accuracy:
	python3 -m hectre.metrics.accuracy \
		"hectre/tests/test_data/305_deBruin_2018.pdfdata" \
		"EASI-50;EASI-75;EASI-90" \
		"hectre/tests/test_data/cdfs/305_deBruin_2018.csv"

# HECTRE
extract:
	python3 -m hectre.extract "$(file)" "$(picos)"

# Back-end components
be-dev:
	poetry run uvicorn backend.main:app --port=5000 --reload

# cd to ui folder 
ui-dev: 
	cd ui && npm install && ng serve

# Run web application via (May need to include "sudo" if running in wsl)
compose:
	docker compose -f ./docker/docker-compose.yaml up -d

# Build docker images, useful after new code is added
build:
	docker compose -f ./docker/docker-compose.yaml up --build -d

# End points for testing basic CRUD. Serves as a template for future endpoints
be-create-items:
	curl -X POST localhost:8000/foo/item/   --data '{"description":"some item description", "public":false}' && echo
	curl -X POST localhost:8000/foo/item/   --data '{"description":"some item description", "public":true}'

be-get-items:
	curl -X GET localhost:8000/foo/item/1 && echo
	curl -X GET localhost:8000/foo/item/2