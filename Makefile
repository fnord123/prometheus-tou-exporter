.DEFAULT_GOAL := push

container: check-env
	docker build . -t dputzolu/tou-exporter:${TAG}

push: container
	docker push dputzolu/tou-exporter

check-env:
ifndef TAG
	$(error TAG is undefined)
endif
