# Secure App - DevSecOps Demonstration

A realistic, production-ready Python microservice demonstrating DevSecOps best practices with GitHub Actions CI/CD pipeline.

## Overview

This repository showcases:
- ✅ Secure Flask application with input validation
- ✅ Comprehensive unit tests with 100% passing rate
- ✅ Secure Python dependencies (no vulnerabilities)
- ✅ Hardened Docker container image
- ✅ Complete DevSecOps GitHub Actions pipeline
- ✅ Automated vulnerability scanning

## Repository Structure

```
secure-app/
├── app/
│   └── main.py              # Flask web application
├── tests/
│   └── test_main.py         # Unit tests (36 tests)
├── Dockerfile               # Multi-stage production build
├── requirements.txt         # Python dependencies
├── .github/
│   └── workflows/
│       └── devsecops-pipeline.yml  # CI/CD pipeline
└── README.md
```

## Quick Start

### Local Development

```bash
# Clone repository
git clone https://github.com/your-org/secure-app.git
cd secure-app

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python -m flask run

# Run tests
pytest tests/ -v
```

### Docker Build

```bash
# Build image
docker build -t secure-app:latest .

# Run container
docker run -p 5000:5000 secure-app:latest

# Access health endpoint
curl http://localhost:5000/api/health
```

## API Endpoints

### Health Check
```bash
GET /api/health
```

Response:
```json
{
  "status": "healthy",
  "service": "secure-app"
}
```

### Greet Endpoint
```bash
POST /api/greet
Content-Type: application/json

{
  "name": "Alice"
}
```

Response:
```json
{
  "message": "Hello, Alice!"
}
```

### Echo Endpoint
```bash
POST /api/echo
Content-Type: application/json

{
  "text": "Hello, World!"
}
```

Response:
```json
{
  "echo": "Hello, World!"
}
```

## Security Features

### Application Security
- ✅ Input validation on all endpoints
- ✅ Content-Type validation (JSON only for POST)
- ✅ Maximum input length enforcement (255 chars default)
- ✅ Safe character whitelisting for names
- ✅ Comprehensive error handling
- ✅ Structured logging for audit trail
- ✅ CORS configuration with origin validation
- ✅ Non-root container execution

### DevSecOps Pipeline

The GitHub Actions pipeline (`devsecops-pipeline.yml`) includes:

1. **Dependency Vulnerability Scanning**
   - Uses `pip-audit` to detect vulnerabilities in Python packages
   - Fails on critical vulnerabilities
   - Generates SBOM for supply chain security

2. **Unit Testing**
   - 36 comprehensive test cases
   - Code coverage reporting
   - Integration with Codecov

3. **Container Image Build**
   - Multi-stage build for minimal image size
   - Push to GitHub Container Registry
   - Build caching for faster builds

4. **Container Vulnerability Scanning**
   - Uses Trivy to scan for container vulnerabilities
   - Generates SARIF report for GitHub Security
   - Uploads findings to GitHub Security tab

5. **Deployment Readiness**
   - Automated deployment summary
   - Status checks before production deployment

## Testing

Run tests locally:

```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=app --cov-report=html

# Specific test class
pytest tests/test_main.py::TestHealthCheck -v

# Specific test
pytest tests/test_main.py::TestGreetEndpoint::test_greet_with_valid_name -v
```

## Dependencies

All dependencies are regularly scanned for vulnerabilities:

- **Flask 3.0.0** - Web framework
- **Flask-CORS 4.0.0** - Cross-Origin Resource Sharing
- **Werkzeug 3.0.1** - WSGI utility library
- **gunicorn 21.2.0** - Production WSGI server
- **requests 2.31.0** - HTTP library
- **pytest 7.4.3** - Testing framework
- **pytest-cov 4.1.0** - Coverage reporting

## Docker Image

Base image: **python:3.12-slim**
- Minimal attack surface
- Regular security updates
- Non-root user execution
- Multi-stage build optimization
- Health check included

## CI/CD Pipeline

The pipeline runs on:
- ✅ Every push to main/develop branches
- ✅ Every pull request to main/develop branches
- ✅ Automatic deployment on main branch push

## Security Scanning Tools

- **pip-audit** - Python dependency vulnerability scanning
- **Trivy** - Container image vulnerability scanning
- **GitHub Security** - Code scanning and alerts
- **codecov** - Code coverage tracking

## Deployment

This application is containerized and ready for:
- ✅ Docker Swarm
- ✅ Kubernetes
- ✅ Cloud platforms (AWS, GCP, Azure, etc.)
- ✅ Container orchestration services

## Best Practices Implemented

1. **Secure Coding**
   - Input validation and sanitization
   - Error handling without information disclosure
   - Logging for security audit trails

2. **DevSecOps Integration**
   - Automated vulnerability scanning
   - Shift-left security testing
   - Container image security

3. **Operational Security**
   - Non-root container execution
   - Minimal base image
   - Health checks
   - Proper logging

4. **Testing**
   - Comprehensive unit test coverage
   - Edge case handling
   - Security-focused test cases

## License

MIT

## Support

For questions or issues, please open a GitHub issue or contact the security team.
