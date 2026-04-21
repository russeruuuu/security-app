# Deployment Guide

This guide provides instructions for deploying the secure-app microservice to various environments.

## Prerequisites

- Docker installed (version 20.10+)
- kubectl configured (for Kubernetes deployment)
- Docker registry credentials for ghcr.io (for container updates)

## Local Development Deployment

### Quick Start

```bash
# Clone repository
git clone https://github.com/russeruuuu/security-app.git
cd secure-app

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run locally
python -m flask run --host=0.0.0.0 --port=5000
```

### Verify Health

```bash
curl http://localhost:5000/api/health
```

## Docker Deployment

### Build Image

```bash
docker build -t secure-app:latest .
```

### Run Container

```bash
docker run -d \
  --name secure-app \
  -p 5000:5000 \
  -e ALLOWED_ORIGINS="http://localhost:3000" \
  secure-app:latest
```

### Health Check

```bash
curl http://localhost:5000/api/health
```

### Stop Container

```bash
docker stop secure-app
docker rm secure-app
```

## Docker Compose Deployment

Create `docker-compose.yml`:

```yaml
version: '3.9'

services:
  secure-app:
    build: .
    container_name: secure-app
    ports:
      - "5000:5000"
    environment:
      - ALLOWED_ORIGINS=http://localhost:3000
      - LOG_LEVEL=INFO
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 5s
    restart: unless-stopped
```

Deploy:

```bash
docker-compose up -d
```

## Kubernetes Deployment

### Create Namespace

```bash
kubectl create namespace secure-app
```

### Create Deployment

Create `k8s-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
  namespace: secure-app
  labels:
    app: secure-app
    version: v1
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: secure-app
  template:
    metadata:
      labels:
        app: secure-app
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
      - name: secure-app
        image: ghcr.io/russeruuuu/security-app:main
        imagePullPolicy: Always
        ports:
        - containerPort: 5000
          name: http
          protocol: TCP
        env:
        - name: ALLOWED_ORIGINS
          value: "https://yourdomain.com"
        - name: LOG_LEVEL
          value: "INFO"
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /api/health
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 10
          timeoutSeconds: 3
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /api/health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 2
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
---
apiVersion: v1
kind: Service
metadata:
  name: secure-app
  namespace: secure-app
  labels:
    app: secure-app
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 5000
    protocol: TCP
    name: http
  selector:
    app: secure-app
```

Deploy to Kubernetes:

```bash
kubectl apply -f k8s-deployment.yaml
```

### Verify Deployment

```bash
# Check pod status
kubectl get pods -n secure-app

# Check service
kubectl get svc -n secure-app

# View logs
kubectl logs -n secure-app -l app=secure-app -f

# Port forward for testing
kubectl port-forward -n secure-app svc/secure-app 5000:80
```

### Test Health Endpoint

```bash
curl http://localhost:5000/api/health
```

## AWS ECS Fargate Deployment

### Create ECR Repository

```bash
aws ecr create-repository --repository-name secure-app --region us-east-1
```

### Push Image

```bash
# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

# Tag image
docker tag secure-app:latest <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/secure-app:latest

# Push image
docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/secure-app:latest
```

### Create ECS Task Definition

Use AWS Console or CLI to create task definition with:
- Image: `<ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/secure-app:latest`
- Memory: 512 MB
- CPU: 256 units
- Port mapping: 5000 → 5000

### Launch Service

```bash
aws ecs create-service \
  --cluster my-cluster \
  --service-name secure-app \
  --task-definition secure-app \
  --desired-count 3 \
  --launch-type FARGATE
```

## GitHub Container Registry (GHCR) Deployment

### Authenticate

```bash
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
```

### Push Image

```bash
docker tag secure-app:latest ghcr.io/username/secure-app:latest
docker push ghcr.io/username/secure-app:latest
```

## Monitoring & Logs

### Container Logs

```bash
# Docker
docker logs -f secure-app

# Kubernetes
kubectl logs -f -n secure-app -l app=secure-app

# ECS
aws logs tail /ecs/secure-app --follow
```

### Health Monitoring

```bash
# Check health endpoint
while true; do
  curl -s http://localhost:5000/api/health | jq .
  sleep 10
done
```

### Metrics Collection

The application logs structured data suitable for:
- ELK Stack
- CloudWatch
- Datadog
- New Relic
- Prometheus

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| FLASK_ENV | production | Flask environment mode |
| ALLOWED_ORIGINS | localhost:3000 | CORS allowed origins |
| LOG_LEVEL | INFO | Logging level |
| PORT | 5000 | Application port |
| WORKERS | 4 | Gunicorn worker count |

## Security Considerations

1. **Use HTTPS/TLS in production** - Configure load balancer with SSL certificate
2. **Network policies** - Restrict ingress/egress traffic
3. **Secrets management** - Use environment secrets for sensitive configuration
4. **Resource limits** - Set CPU and memory limits to prevent DoS
5. **Non-root user** - Container runs as UID 1000
6. **Read-only filesystem** - Enable in Kubernetes for additional security

## Rollback Procedure

### Docker

```bash
docker pull ghcr.io/username/secure-app:previous-tag
docker run -d --name secure-app-previous ghcr.io/username/secure-app:previous-tag
```

### Kubernetes

```bash
kubectl rollout history deployment/secure-app -n secure-app
kubectl rollout undo deployment/secure-app -n secure-app --to-revision=2
```

## Performance Tuning

### Gunicorn Workers

For 2 CPU system:
```
workers = (2 * CPU_count) + 1 = 5
```

### Resource Limits

Recommended for production:
- Memory: 256-512 MB
- CPU: 200-500m

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs secure-app

# Check resource availability
docker stats
```

### Health Check Failing

```bash
# Test endpoint directly
docker exec secure-app curl http://localhost:5000/api/health

# Check port binding
docker port secure-app
```

### High Memory Usage

```bash
# Set memory limit in docker-compose
mem_limit: 512m

# Check for memory leaks
docker stats --no-stream
```

---

For additional support, see [README.md](README.md) and [PIPELINE_LOGS.md](PIPELINE_LOGS.md)
