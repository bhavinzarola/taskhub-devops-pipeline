# 🚀 TaskHub DevOps Pipeline

A production-ready, end-to-end DevOps pipeline for a Python/Flask task management application — containerised with Docker, orchestrated with Kubernetes, provisioned with Terraform, and served behind an Nginx reverse proxy with a PostgreSQL database.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Local Development with Docker Compose](#local-development-with-docker-compose)
  - [Deploy to Kubernetes](#deploy-to-kubernetes)
  - [Infrastructure Provisioning with Terraform](#infrastructure-provisioning-with-terraform)
- [Environment Variables](#environment-variables)
- [Docker Details](#docker-details)
- [Kubernetes Details](#kubernetes-details)
- [Terraform Details](#terraform-details)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**TaskHub** is a full-stack task management web application designed to demonstrate a complete DevOps pipeline from local development to production deployment. The project showcases:

- Containerisation of a Python Flask application using Docker best practices (non-root user, slim base image, Gunicorn WSGI server)
- Multi-service local orchestration via Docker Compose (app + database + reverse proxy)
- Kubernetes manifests for scalable, cloud-native deployment
- Terraform configuration for repeatable infrastructure provisioning
- Nginx as a reverse proxy for the Flask application

---

## Architecture

```
                        ┌─────────────┐
                        │   Client    │
                        └──────┬──────┘
                               │  HTTP :80
                        ┌──────▼──────┐
                        │    Nginx    │  Reverse Proxy
                        └──────┬──────┘
                               │  :5000
                        ┌──────▼──────┐
                        │ Flask / App │  Gunicorn WSGI
                        │  (Python)   │
                        └──────┬──────┘
                               │
                        ┌──────▼──────┐
                        │ PostgreSQL  │  Persistent Storage
                        └─────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Application** | Python 3.11, Flask, Gunicorn |
| **Database** | PostgreSQL 15 |
| **Reverse Proxy** | Nginx (Alpine) |
| **Containerisation** | Docker, Docker Compose |
| **Orchestration** | Kubernetes |
| **Infrastructure** | Terraform (HCL) |
| **Frontend** | HTML, CSS |

---

## Project Structure

```
taskhub-devops-pipeline/
├── app/                        # Flask application source code
│   ├── app.py                  # Application entry point
│   ├── requirements.txt        # Python dependencies
│   └── templates/              # HTML templates
├── kubernetes/                 # Kubernetes manifests
│   ├── deployment.yaml         # App Deployment
│   ├── service.yaml            # Service definitions
│   └── ...
├── nginx/
│   └── nginx.conf              # Nginx reverse proxy configuration
├── terraform/                  # Infrastructure as Code
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── Dockerfile                  # Multi-stage Docker build
├── docker-compose.yml          # Local development orchestration
└── .gitignore
```

---

## Prerequisites

Make sure the following tools are installed before getting started:

- [Docker](https://docs.docker.com/get-docker/) `>= 24.x`
- [Docker Compose](https://docs.docker.com/compose/install/) `>= 2.x`
- [kubectl](https://kubernetes.io/docs/tasks/tools/) (for Kubernetes deployment)
- [Terraform](https://developer.hashicorp.com/terraform/install) `>= 1.x` (for infrastructure provisioning)
- [Python 3.11+](https://www.python.org/downloads/) (for local development without Docker)

---

## Getting Started

### Local Development with Docker Compose

This is the fastest way to get the full stack running locally.

**1. Clone the repository**

```bash
git clone https://github.com/bhavinzarola/taskhub-devops-pipeline.git
cd taskhub-devops-pipeline
```

**2. Start all services**

```bash
docker compose up --build
```

This will start three services:
- `db` — PostgreSQL database on the internal network
- `web` — Flask app served by Gunicorn on port `5000`
- `nginx` — Nginx reverse proxy exposed on port `80`

**3. Open the app**

```
http://localhost
```

**4. Stop all services**

```bash
docker compose down
```

To also remove the persistent database volume:

```bash
docker compose down -v
```

---

### Deploy to Kubernetes

**1. Build and push the Docker image**

```bash
docker build -t your-dockerhub-username/taskhub:latest .
docker push your-dockerhub-username/taskhub:latest
```

**2. Update the image reference** in `kubernetes/deployment.yaml` to point to your image.

**3. Apply the manifests**

```bash
kubectl apply -f kubernetes/
```

**4. Verify the deployment**

```bash
kubectl get pods
kubectl get services
```

---

### Infrastructure Provisioning with Terraform

**1. Navigate to the Terraform directory**

```bash
cd terraform
```

**2. Initialise Terraform**

```bash
terraform init
```

**3. Review the execution plan**

```bash
terraform plan
```

**4. Apply the infrastructure**

```bash
terraform apply
```

**5. Destroy infrastructure when done**

```bash
terraform destroy
```

---

## Environment Variables

The application is configured via environment variables. These are set in `docker-compose.yml` for local development and should be passed as Kubernetes Secrets or ConfigMaps in production.

| Variable | Description | Default |
|---|---|---|
| `DB_HOST` | PostgreSQL host | `db` |
| `DB_NAME` | Database name | `MyFirstAppDb` |
| `DB_USER` | Database user | `postgres` |
| `DB_PASSWORD` | Database password | *(see compose file)* |
| `DB_PORT` | Database port | `5432` |

> ⚠️ **Security Note:** Never commit real credentials to version control. Use environment-specific secret management (e.g. Kubernetes Secrets, AWS Secrets Manager, or HashiCorp Vault) in production environments.

---

## Docker Details

The `Dockerfile` follows production best practices:

- **Base image:** `python:3.11-slim` — minimal footprint
- **Non-root user:** The application runs as `appuser` for improved security
- **Gunicorn:** Production-ready WSGI server instead of the Flask development server
- **Port:** `5000`

```dockerfile
# Key highlights
FROM python:3.11-slim
RUN adduser --disabled-password --gecos '' appuser
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

---

## Kubernetes Details

The `kubernetes/` directory contains manifests for deploying TaskHub to any Kubernetes cluster (local via `minikube` or cloud-based via EKS/GKE/AKS):

- **Deployment** — defines replica count, container image, and environment config
- **Service** — exposes the app internally (ClusterIP) or externally (LoadBalancer/NodePort)

---

## Terraform Details

The `terraform/` directory contains HCL configuration to provision the required cloud infrastructure (e.g. VPC, compute instances, managed database, container registry). Update `variables.tf` with your environment-specific values before running.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">Built with ❤️ by <a href="https://github.com/bhavinzarola">bhavinzarola</a></p>
