# Self-Healing E-Commerce Platform

A production-grade microservices application with 
self-healing infrastructure on AWS EKS.

## Architecture

Three independent microservices communicating over HTTP:
- **Inventory Service** (port 8001) — manages product stock
- **Cart Service** (port 8002) — handles user carts
- **Payment Service** (port 8003) — processes checkout

## Tech Stack

- Python + FastAPI
- Docker + Docker Compose
- Kubernetes (EKS) — coming in Phase 3
- Terraform — coming in Phase 3
- GitHub Actions CI/CD — coming in Phase 5
- Prometheus + Grafana — coming in Phase 6

## Run Locally With Docker

git clone https://github.com/Akioye/ecommerce-platform
cd ecommerce-platform
docker compose up --build
