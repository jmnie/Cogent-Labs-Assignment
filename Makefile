PROGRAM_NAME = image_service_app
PROGRAM_BINARY = ./bin/$(PROGRAM_NAME)

.PHONY: build
build: $(PROGRAM_BINARY)

.PHONY: clean
clean:
	rm -rf $(PROGRAM_BINARY)
	rm -rf ./build
	rm -rf ./bin

.PHONY: rebuild
rebuild: clean
	$(MAKE) build

.PHONY: install_requirements
install_requirements:
	pip3 install -r requirements.txt


$(PROGRAM_BINARY): install_requirements
	pyinstaller --onefile ./image_convert_service.py --name $(PROGRAM_NAME) --distpath ./bin 

docker-%:
	docker run \
	  -it \
		--rm \
		-v $(dir $(realpath $(firstword $(MAKEFILE_LIST)))):/src \
		-w /src \
		python:3.8-slim-buster \
		bash -c "apt update; apt install -y make binutils build-essential; make rebuild"

.PHONY: image
image: docker-rebuild
	docker build -t $(PROGRAM_CONTAINER) .
