# Alethic ISM AI Model Pricing Fetcher

A Kubernetes Job that fetches and stores AI model pricing information from Anthropic, OpenAI, and Google Gemini into a PostgreSQL database.

## Overview

This service fetches the latest pricing information for AI models from:
- **Anthropic**: Claude models (Opus, Sonnet, Haiku, Instant)
- **OpenAI**: GPT models (GPT-4, GPT-4o, GPT-3.5, o1 models)
- **Google**: Gemini models (Gemini 1.5 Pro, Flash, Gemini 1.0 Pro, Gemini 2.0)

The pricing data includes:
- Input token pricing (per 1K tokens)
- Output token pricing (per 1K tokens)
- Context window size
- Maximum output tokens
- Last updated timestamp

## Database Schema

```sql
CREATE TABLE model_pricing (
    id SERIAL PRIMARY KEY,
    provider VARCHAR(50) NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    input_price_per_1k_tokens DECIMAL(10, 6),
    output_price_per_1k_tokens DECIMAL(10, 6),
    context_window INTEGER,
    max_output_tokens INTEGER,
    last_updated TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(provider, model_name)
);
```

## Local Development

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- PostgreSQL (optional, can use Docker)

### Running Locally

1. **Using Docker Compose** (recommended):
```bash
docker-compose up
```

2. **Using Python directly**:
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=pricing
export DB_USER=postgres
export DB_PASSWORD=postgres

# Run the script
python main.py
```

## Building and Deployment

### Build Docker Image

```bash
make build
# or
docker build -t krasaee/alethic-ism-ai-model-pricing:latest .
```

### Deploy to Kubernetes

1. **Create the secret** (update with your database credentials):
```bash
kubectl apply -f k8s/secret.yaml
```

2. **Run as a one-time job**:
```bash
kubectl apply -f k8s/job.yaml
```

3. **Schedule as a CronJob** (runs daily at midnight):
```bash
kubectl apply -f k8s/cronjob.yaml
```

### Check Job Status

```bash
# Check job status
kubectl get jobs -n alethic | grep pricing

# Check pod logs
kubectl logs -n alethic -l app=alethic-ism-ai-model-pricing

# Check if CronJob is scheduled
kubectl get cronjobs -n alethic
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_HOST` | PostgreSQL host | localhost |
| `DB_PORT` | PostgreSQL port | 5432 |
| `DB_NAME` | Database name | pricing |
| `DB_USER` | Database user | postgres |
| `DB_PASSWORD` | Database password | postgres |

## CI/CD

The GitHub Actions workflow automatically:
1. Builds the Docker image on push to main
2. Tags with version and latest
3. Pushes to Docker Hub
4. Can optionally deploy to Kubernetes cluster

## Pricing Data Sources

The pricing data is currently hardcoded based on publicly available pricing information:
- [Anthropic Pricing](https://www.anthropic.com/pricing)
- [OpenAI Pricing](https://openai.com/api/pricing/)
- [Google Gemini Pricing](https://ai.google.dev/pricing)

Future enhancements could include:
- Fetching pricing from official APIs when available
- Adding more providers (Cohere, Mistral, etc.)
- Historical pricing tracking
- Price change notifications

## Project Structure

```
.
├── main.py                 # Main Python script
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Local development setup
├── Makefile              # Build automation
├── k8s/                  # Kubernetes manifests
│   ├── job.yaml         # One-time job
│   ├── cronjob.yaml     # Scheduled job
│   └── secret.yaml      # Database credentials
└── .github/
    └── workflows/
        └── build-main.yml  # CI/CD pipeline
```

## License

Part of the Alethic ISM ecosystem.