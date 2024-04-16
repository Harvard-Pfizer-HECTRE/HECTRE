# General
setup:
	python -m pip install -r requirements.txt

test:
	python -m pytest

measure-accuracy:
	python -m hectre.metrics.accuracy \
		$(path_to_pdf) \
		$(picos_string) \
		$(path_to_cdf)

measure-ad-accuracy:
	python -m hectre.metrics.accuracy \
		"hectre/tests/test_data/305_deBruin_2018.pdfdata" \
		"EASI-50;EASI-75;EASI-90" \
		"hectre/tests/test_data/cdfs/305_deBruin_2018.csv"

# HECTRE
extract:
	python -m hectre.extract "$(file)" "$(picos)"

# Back-end components
be-dev:
	poetry run uvicorn backend.main:app --port=5000 --reload

be-create-items:
	curl -X POST localhost:8000/foo/item/   --data '{"description":"some item description", "public":false}' && echo
	curl -X POST localhost:8000/foo/item/   --data '{"description":"some item description", "public":true}'

be-get-items:
	curl -X GET localhost:8000/foo/item/1 && echo
	curl -X GET localhost:8000/foo/item/2