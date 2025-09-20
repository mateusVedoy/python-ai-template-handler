IMAGE_NAME = ubuntu22:v1

run-api:
	uvicorn src.main:app --env-file .env --timeout-graceful-shutdown 10

run-mongo:
	@docker-compose up -d