.PHONY: build publish

TAG=eamonnfaherty83/aws-cloudtrail-events-schema

build:
	docker build . -t $(TAG)

publish:
	docker push $(TAG)

upload:
	python setup.py sdist
	pip install twine
	python -m twine upload --verbose dist/*

clean:
	rm -rf aws_cloudtrail_events_schema.egg-info
	rm -rf build
	rm -rf dist