# 🏋️ DevSecOps Cloud-Native Platform

A complete DevSecOps pipeline for a containerized 
FastAPI application with PostgreSQL, CI/CD, 
Docker, and Kubernetes.

---

## 🚀 Pipeline Flow

git push
    ↓
GitHub Actions
  → Tests (pytest)
  → Lint (ruff)
  → Docker build
  → Push to Docker Hub
    ↓
Kubernetes
  → FastAPI (2 replicas)
  → PostgreSQL

---

## 🛠️ Technologies

| Category | Technology |
|---|---|
| Backend | FastAPI, Python |
| Database | PostgreSQL, SQLAlchemy |
| Testing | pytest |
| Linting | ruff |
| Containerization | Docker, Docker Compose |
| Registry | Docker Hub |
| Orchestration | Kubernetes (Kind) |
| CI/CD | GitHub Actions |

---

## 📁 Project Structure

src/
  main.py
  db.py
  models.py
  schemas.py
tests/
k8s/
  deployment.yaml
  service.yaml
  postgres.yaml
.github/
  workflows/
    ci.yml
    docker.yml

---

## 🏃 How to Run

### With Docker Compose
docker compose up

### With Kubernetes
kind create cluster --name devsecops
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl port-forward service/fitness-api-service 8000:80

### Access the app
http://localhost:8000/health
http://localhost:8000/docs

---

## 🔜 Next Steps
- Azure Container Registry (ACR)
- Terraform (AKS)
- Monitoring (Prometheus/Grafana)
