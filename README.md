# Content Sentiment Classifier

## Overview
A production style ML API that classifies financial news text by sentiment (positive, negative, neutral) and topic (earnings, regulation, mergers & acquisitions, market movement). Built to demonstrate end-to-end ML deployment using FastAPI, Docker, and AWS.

## Tech Stack
| Technology | Purpose | Why |
|---|---|---|
| FastAPI | API framework | High performance, async support, automatic interactive docs via `/docs` |
| Pydantic | Request/response validation | Type-safe contracts enforced at the API boundary |
| Hugging Face Transformers | Zero-shot classification | `facebook/bart-large-mnli` enables classification without fine-tuning in Phase 1 |
| Docker | Containerization | Consistent environments across local dev and cloud deployment |
| AWS ECS (Fargate) | Container hosting | Managed, serverless container orchestration; no EC2 instances to maintain |
| AWS ECR | Container registry | Private Docker image storage integrated with ECS |
| AWS S3 | Model artifact storage | Durable, cheap storage for model files |
| AWS CloudWatch | Logging | Centralised log management for running containers |

## Architecture
```
User Request
     │
     ▼
FastAPI (ECS Fargate): http://54.243.10.49:7860
     │
     ▼
HuggingFace Pipeline (zero-shot classification)
     │
     ▼
JSON Response (sentiment + topic + confidence scores)
```

**Live Endpoints:**
- API: http://54.243.10.49:7860
- Interactive Docs: http://54.243.10.49:7860/docs
- Health Check: http://54.243.10.49:7860/health

> Note: Public IP is not static, will change if the ECS task restarts. An Application Load Balancer will be added in Phase 3 for a stable URL.

## Project Structure
```
content-sentiment-classifier/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app and endpoints
│   ├── model.py         # Model loading and inference logic
│   └── schemas.py       # Pydantic request/response models
├── task-definition.json # ECS task definition (sanitized)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.12+
- Docker Desktop
- AWS CLI configured (`aws configure`)
- uv (`pip install uv`)

### Installation
```bash
git clone https://github.com/danpelis/content-sentiment-classifier.git
cd content-sentiment-classifier
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Environment Variables
Copy `.env.example` to `.env` and fill in your values:
```bash
cp .env.example .env
```

`.env.example`:
```
AWS_ACCOUNT_ID=your-account-id
AWS_REGION=us-east-1
```

### Running Locally
```bash
uvicorn app.main:app --reload
```

### Running with Docker
```bash
docker compose up
```

API will be available at `http://localhost:7860`
Interactive docs at `http://localhost:7860/docs`

## API Reference

### GET /health
Returns service health status.

**Response:**
```json
{
  "status": "healthy"
}
```

### POST /classify
Classifies a text input by sentiment and topic.

**Request:**
```json
{
  "text": "Apple reports record quarterly earnings beating analyst expectations"
}
```

**Response:**
```json
{
  "sentiment": "positive",
  "confidence": 0.94,
}
```

## Deployment

### Push image to ECR
Authenticate Docker to ECR:
```bash
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS \
  --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
```

Build and push (targeting linux/amd64 for Fargate compatibility):
```bash
docker buildx build \
  --platform linux/amd64 \
  -t $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/finance-classifier:latest \
  --push .
```

### Deploy to ECS
Substitute your account ID into the task definition:
```bash
sed -i 's/AWS_ACCOUNT_ID/'$AWS_ACCOUNT_ID'/g' task-definition.json
```

Register the task definition:
```bash
aws ecs register-task-definition \
  --cli-input-json file://task-definition.json
```

Force a new deployment:
```bash
aws ecs update-service \
  --cluster content-sentiment-cluster \
  --service content-sentiment-service \
  --force-new-deployment
```

> **Note:** Remember to revert `task-definition.json` after deploying so the placeholder is restored before committing:
> ```bash
> sed -i 's/'$AWS_ACCOUNT_ID'/AWS_ACCOUNT_ID/g' task-definition.json
> ```

## Design Decisions

**Zero-shot classification over fine-tuning (Phase 1)**
`facebook/bart-large-mnli` was chosen for Phase 1 to focus on API and deployment mechanics rather than model training. The trade-off is lower accuracy on domain-specific text. Phase 3 will replace this with a fine-tuned model trained on a Reddit sentiment dataset via AWS SageMaker Training Jobs.

**FastAPI over Flask**
FastAPI provides automatic OpenAPI docs generation at `/docs`, native async support, and Pydantic integration for request validation out of the box. For an ML API where the bottleneck is model inference, async support is a meaningful advantage.

**Model loaded at startup via lifespan**
The HuggingFace pipeline is loaded once at application startup using FastAPI's `lifespan` context manager rather than on each request, avoiding the overhead of loading a large model on every call.

**ECS Fargate over EC2**
Fargate removes the need to manage underlying instances AWS handles patching, scaling, and availability. For a containerized application this is the appropriate production pattern.

**linux/amd64 build target**
Docker images must be built targeting `linux/amd64` explicitly when developing on Apple Silicon Macs, as Fargate runs on amd64 infrastructure. Use `docker buildx build --platform linux/amd64` to ensure compatibility.

## Future Improvements
See [ROADMAP.md](ROADMAP.md) for the full planned roadmap. Upcoming phases include:

- **Phase 3:** Reddit movie sentiment tracking pipeline PRAW ingestion, fine-tuned sentiment model on SageMaker, PostgreSQL on RDS, Streamlit dashboard on EC2
- **Application Load Balancer** stable public URL in front of ECS, replacing the current static IP
- **Phase 4:** Explainability via Integrated Gradients (Captum) and LLM summarization via Claude API and LangChain, surfacing "what audiences like/dislike" summaries

## Author
Daniel Pelis
[LinkedIn](https://linkedin.com/in/yourprofile) · [GitHub](https://github.com/yourusername)