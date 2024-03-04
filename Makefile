setup:
	@scripts/setup.sh
lint:
	@poetry run scripts/lint.sh
dev:
	@poetry run scripts/dev.sh
docker-run:
	@docker build -t ifood-token-generator .
	@docker run -it --rm -p 8000:8000 --env-file ./.env ifood-token-generator