# Makefile
.PHONY: build run test clean version deploy help

# Default image name - can be overridden with make IMAGE=your-image-name
IMAGE ?= krasaee/alethic-ism-ai-model-pricing:latest

# Build the Docker image
build:
	docker build -t $(IMAGE) .

# Run locally with docker-compose
run:
	docker-compose up

# Run in detached mode
run-detached:
	docker-compose up -d

# Stop and remove containers
stop:
	docker-compose down

# Run tests locally
test:
	docker-compose up postgres -d
	sleep 5
	DB_HOST=localhost DB_PORT=5432 DB_NAME=pricing DB_USER=postgres DB_PASSWORD=postgres python main.py
	docker-compose down

# Version bump (patch version)
version:
	@echo "Bumping patch version..."
	@git fetch --tags
	@LATEST_TAG=$$(git describe --tags --abbrev=0 2>/dev/null || echo ""); \
	if [[ -z "$$LATEST_TAG" ]]; then \
		MAJOR=0; MINOR=1; PATCH=0; \
		OLD_TAG="<none>"; \
	else \
		OLD_TAG="$$LATEST_TAG"; \
		VERSION="$${LATEST_TAG#v}"; \
		IFS='.' read -r MAJOR MINOR PATCH <<< "$$VERSION"; \
		PATCH=$$((PATCH + 1)); \
	fi; \
	NEW_TAG="v$${MAJOR}.$${MINOR}.$${PATCH}"; \
	git tag -a "$$NEW_TAG" -m "Release $$NEW_TAG"; \
	git push origin "$$NEW_TAG"; \
	echo "➜ bumped $${OLD_TAG} → $${NEW_TAG}"

# Deploy to Kubernetes
deploy:
	kubectl apply -f k8s/secret.yaml
	kubectl apply -f k8s/job.yaml

# Deploy CronJob to Kubernetes
deploy-cron:
	kubectl apply -f k8s/secret.yaml
	kubectl apply -f k8s/cronjob.yaml

# Check deployment status
status:
	kubectl get jobs -n alethic | grep pricing
	kubectl get pods -n alethic -l app=alethic-ism-ai-model-pricing

# View logs
logs:
	kubectl logs -n alethic -l app=alethic-ism-ai-model-pricing --tail=50

# Clean up Docker resources
clean:
	docker-compose down -v
	docker system prune -f

# Show help
help:
	@echo "Available targets:"
	@echo "  build        - Build Docker image"
	@echo "  run          - Run locally with docker-compose"
	@echo "  run-detached - Run in background with docker-compose"
	@echo "  stop         - Stop docker-compose services"
	@echo "  test         - Test the script locally"
	@echo "  version      - Bump patch version and create git tag"
	@echo "  deploy       - Deploy Job to Kubernetes"
	@echo "  deploy-cron  - Deploy CronJob to Kubernetes"
	@echo "  status       - Check Kubernetes deployment status"
	@echo "  logs         - View pod logs"
	@echo "  clean        - Clean up Docker resources"
	@echo "  help         - Show this help message"
	@echo ""
	@echo "Variables:"
	@echo "  IMAGE        - Docker image name (default: krasaee/alethic-ism-ai-model-pricing:latest)"