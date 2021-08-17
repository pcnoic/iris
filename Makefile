dev:
	cd src/ && uvicorn api:app --reload

dependencies:
	pip3 install -r requirements.txt