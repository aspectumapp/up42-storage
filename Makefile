## Configuration for Makefile.
USER := vision@eosda.com
UP42_DOCKERFILE := Dockerfile
DOCKER_TAG :=
DOCKER_VERSION := latest
UP42_MANIFEST := UP42Manifest.json

AWS_ACCESS_KEY :=
AWS_SECRET_ACCESS_KEY :=
AWS_REGION :=
AWS_BUCKET_NAME :=

UID :=

VALIDATE_ENDPOINT := https://api.up42.com/validate-schema/block
REGISTRY := registry.up42.com

install:
	pip install -r requirements.txt

clean:
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name ".mypy_cache" -exec rm -rf {} +
	find . -name ".pytest_cache" -exec rm -rf {} +
	find . -name ".coverage" -exec rm -f {} +

validate:
	curl -X POST -H 'Content-Type: application/json' -d @UP42Manifest.json $(VALIDATE_ENDPOINT)

build:
	cd $(SRC);
	docker build . \
	--build-arg manifest='$(shell cat ${UP42_MANIFEST})' \
	--build-arg aws_access_key='${AWS_ACCESS_KEY}' \
	--build-arg aws_secret_access_key='${AWS_SECRET_ACCESS_KEY}' \
	--build-arg aws_region='${AWS_REGION}' \
	--build-arg aws_bucket_name='${AWS_BUCKET_NAME}' \
	--build-arg aws_public_bucket_name='${AWS_PUBLIC_BUCKET_NAME}' \
	-t $(REGISTRY)/$(UID)/$(DOCKER_TAG):$(DOCKER_VERSION)

push:
	docker push $(REGISTRY)/$(UID)/$(DOCKER_TAG):$(DOCKER_VERSION)

login:
	docker login -u $(USER) https://$(REGISTRY)
https://registry.up42.com

.PHONY: build login push install push login
