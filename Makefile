container:
	docker build . -t dputzolu/tou-exporter:latest

push: container
	docker push dputzolu/tou-exporter:latest
