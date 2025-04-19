build:
	@docker build -t raspberry-pi-stats .
run:
	@docker run -d -p 9002:8000 --restart always --name pi-stats --privileged raspberry-pi-stats