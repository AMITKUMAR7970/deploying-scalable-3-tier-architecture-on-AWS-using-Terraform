


# DevOps 3-Tier Web Application with Terraform

[![Terraform](https://img.shields.io/badge/Terraform-v1.5+-623CE4?logo=terraform&logoColor=white)](https://terraform.io)
[![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900?logo=amazon-aws&logoColor=white)](https://aws.amazon.com)
[![React](https://img.shields.io/badge/React-18.2+-61DAFB?logo=react&logoColor=white)](https://reactjs.org)
[![Node.js](https://img.shields.io/badge/Node.js-18+-339933?logo=node.js&logoColor=white)](https://nodejs.org)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A comprehensive, production-ready DevOps project demonstrating **Infrastructure as Code** deployment of a 3-tier web application on AWS using **Terraform**, **CI/CD pipelines**, and modern cloud-native practices.

---

## 🏗️ Project Architecture

```

┌─────────────────────────────────────────────────────────────────────────┐
│                              AWS CLOUD                                  │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    PRESENTATION TIER                            │   │
│  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │   │
│  │  │     ALB      │    │   Frontend   │    │  CloudFront  │     │   │
│  │  │  (Routes     │───▶│  (React.js)  │◄───│   (CDN)      │     │   │
│  │  │   Traffic)   │    │   Container  │    │  [Optional]  │     │   │
│  │  └──────────────┘    └──────────────┘    └──────────────┘     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                 │                                       │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                     APPLICATION TIER                            │   │
│  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │   │
│  │  │     ALB      │    │     ECS      │    │  Auto Scale  │     │   │
│  │  │  (Backend    │───▶│  (Node.js)   │◄───│    Group     │     │   │
│  │  │   Routes)    │    │   Fargate    │    │   (2-20)     │     │   │
│  │  └──────────────┘    └──────────────┘    └──────────────┘     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                 │                                       │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                         DATA TIER                               │   │
│  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │   │
│  │  │     RDS      │    │  Read        │    │   Backup     │     │   │
│  │  │   MySQL      │───▶│ Replicas     │    │   \& Point    │     │   │
│  │  │  Multi-AZ    │    │ [Production] │    │  in Time     │     │   │
│  │  └──────────────┘    └──────────────┘    └──────────────┘     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘

```

## 🚀 Features

### **🏭 Production-Ready Infrastructure**
- ✅ **Auto-scaling** applications based on CPU/memory metrics
- ✅ **Multi-AZ database** deployment with automated failover
- ✅ **Application Load Balancer** with health checks
- ✅ **VPC isolation** with public/private subnets
- ✅ **Comprehensive monitoring** and alerting

### **🔒 Security First**
- ✅ **Network isolation** - All application traffic in private subnets
- ✅ **Encryption** at rest and in transit
- ✅ **IAM roles** with least privilege access
- ✅ **Security groups** with minimal required access
- ✅ **VPC Flow Logs** and audit trails

### **⚡ Developer Experience**
- ✅ **One-command deployment** to any environment
- ✅ **Local development** with Docker Compose
- ✅ **Automated testing** and linting
- ✅ **Interactive project explorer**
- ✅ **Hot reload** development environment

### **📈 DevOps Excellence**
- ✅ **Infrastructure as Code** with Terraform modules
- ✅ **Multi-environment** support (dev, staging, prod)
- ✅ **CI/CD pipelines** with GitHub Actions
- ✅ **Container orchestration** with ECS Fargate
- ✅ **Automated deployments** with rollback capability

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | React.js 18, NGINX | Modern SPA with responsive UI |
| **Backend** | Node.js, Express.js | RESTful API with database integration |
| **Database** | MySQL 8.0 (RDS) | Persistent data with Multi-AZ |
| **Infrastructure** | Terraform, AWS | Infrastructure as Code |
| **Containers** | Docker, ECS Fargate | Application containerization |
| **Load Balancer** | AWS ALB | Traffic distribution and SSL termination |
| **Monitoring** | CloudWatch, SNS | Metrics, logs, and alerting |
| **CI/CD** | GitHub Actions | Automated testing and deployment |

## 📊 Project Statistics

- **52 files** across infrastructure, application, and deployment
- **5,806 lines of code** with comprehensive documentation
- **21 Terraform files** for infrastructure automation
- **6 reusable modules** for scalable architecture
- **3 environments** with production-grade configurations

## 🏃‍♂️ Quick Start

### Prerequisites
```


# Required tools

- AWS CLI v2
- Terraform >= 1.0
- Docker \& Docker Compose
- Node.js 18+
- Git

```

### 1. Local Development
```


# Clone repository

git clone <repository-url>
cd terraform-3tier-devops

# Start local environment

docker-compose up -d

# Access application

open http://localhost:80

```

### 2. AWS Deployment
```


# Setup AWS credentials

aws configure

# Initialize Terraform backend

./scripts/setup-backend.sh

# Deploy to development

./scripts/deploy.sh -e dev -d <your-ecr-registry>

```

## 📁 Project Structure

```

terraform-3tier-devops/
├── 📁 .github/workflows/          \# CI/CD pipelines
│   ├── terraform-plan.yml         \# Pull request validation
│   └── terraform-apply.yml        \# Automated deployment
├── 📁 application/                \# Application source code
│   ├── 📁 frontend/               \# React.js application
│   │   ├── Dockerfile             \# Production container
│   │   ├── Dockerfile.dev         \# Development container
│   │   ├── package.json           \# Dependencies
│   │   └── src/                   \# React components
│   └── 📁 backend/                \# Node.js API
│       ├── Dockerfile             \# API container
│       ├── server.js              \# Express server
│       └── package.json           \# Dependencies
├── 📁 terraform/                  \# Infrastructure as Code
│   ├── 📁 environments/           \# Environment configs
│   │   ├── dev/                   \# Development
│   │   ├── staging/               \# Staging
│   │   └── prod/                  \# Production
│   └── 📁 modules/                \# Reusable modules
│       ├── vpc/                   \# Networking
│       ├── alb/                   \# Load balancing
│       ├── ecs/                   \# Container orchestration
│       ├── rds/                   \# Database
│       ├── security/              \# Security groups
│       └── monitoring/            \# CloudWatch
├── 📁 scripts/                    \# Automation scripts
│   ├── deploy.sh                  \# Deployment automation
│   ├── setup-backend.sh           \# Backend initialization
│   └── init.sql                   \# Database setup
├── 📁 docs/                       \# Documentation
│   ├── architecture.md            \# System architecture
│   └── deployment.md              \# Deployment guide
├── docker-compose.yml             \# Local development
├── Makefile                       \# Development commands
└── README.md                      \# This file

```

## 🌍 Environment Configuration

### Development Environment
```


# terraform/environments/dev/terraform.tfvars

vpc_cidr = "10.0.0.0/16"
backend_cpu = 256
backend_memory = 512
backend_desired_count = 1
db_instance_class = "db.t3.micro"
multi_az = false

```

### Production Environment
```


# terraform/environments/prod/terraform.tfvars

vpc_cidr = "10.2.0.0/16"
backend_cpu = 1024
backend_memory = 2048
backend_desired_count = 3
backend_max_capacity = 20
db_instance_class = "db.t3.large"
multi_az = true
create_read_replica = true

```

## 🚢 Deployment Options

### Automated Deployment
```


# Deploy specific environment

./scripts/deploy.sh -e dev -d your-registry.com

# Deploy with custom version

./scripts/deploy.sh -e prod -v v1.2.3 -d your-registry.com

# Skip Docker build (use existing images)

./scripts/deploy.sh -e staging --skip-build

```

### Manual Terraform
```

cd terraform/environments/dev
terraform init
terraform plan
terraform apply

```

### Using Makefile
```

make up              \# Start local environment
make deploy-dev      \# Deploy to development
make deploy-prod     \# Deploy to production
make clean           \# Clean up local environment

```

## 🔄 CI/CD Pipeline

### Workflow Triggers
- **Pull Request** → Terraform plan + security scan
- **Push to Main** → Auto-deploy to development
- **Release Tag** → Deploy to staging/production
- **Manual Trigger** → Deploy to any environment

### Pipeline Steps
1. **Code Quality** → Lint, test, security scan
2. **Build** → Docker images to ECR
3. **Infrastructure** → Terraform plan and apply
4. **Deploy** → Update ECS services
5. **Verify** → Health checks and smoke tests

### Required Secrets
```


# GitHub Repository Secrets

AWS_ACCESS_KEY_ID: your-access-key
AWS_SECRET_ACCESS_KEY: your-secret-key
DOCKER_REGISTRY: your-account.dkr.ecr.region.amazonaws.com

```

## 📊 Monitoring & Observability

### CloudWatch Dashboards
- **Application Performance** → Response times, throughput
- **Infrastructure Health** → CPU, memory, disk usage
- **Database Metrics** → Connections, slow queries, storage

### Automated Alerts
- **Critical** → Service failures, high error rates
- **Warning** → Resource utilization thresholds
- **Info** → Deployment and scaling events

### Log Aggregation
- **Application Logs** → Structured JSON to CloudWatch
- **Access Logs** → ALB requests to S3
- **Infrastructure Logs** → VPC Flow Logs, CloudTrail

## 🔧 Development Commands

```


# Local development

make install         \# Install dependencies
make up             \# Start all services
make logs           \# View service logs
make test           \# Run tests
make lint           \# Code linting

# Infrastructure

make tf-init-dev    \# Initialize Terraform
make tf-plan-dev    \# Plan infrastructure changes
make tf-apply-dev   \# Apply changes

# Database

make db-shell       \# Connect to database
make db-migrate     \# Run migrations

```

## 🚨 Troubleshooting

### Common Issues

**ECS Tasks Fail to Start**
```


# Check task definition and service events

aws ecs describe-services --cluster dev-cluster --services dev-service
aws logs tail /ecs/dev/app --follow

```

**Database Connection Issues**
```


# Verify security groups and network connectivity

aws ec2 describe-security-groups --group-ids sg-xxx
aws rds describe-db-instances --db-instance-identifier dev-database

```

**ALB Health Check Failures**
```


# Check target group health

aws elbv2 describe-target-health --target-group-arn arn:aws:...
curl -I http://alb-dns-name/health

```

### Debug Mode
```


# Enable Terraform debug logging

export TF_LOG=DEBUG
terraform apply

# Enable AWS CLI debug

aws ecs describe-services --debug --cluster dev-cluster --services dev-service

```

## 📚 Documentation

- 🏗️ [Architecture Overview](docs/architecture.md)
- 🚀 [Deployment Guide](docs/deployment.md)
- 🔒 [Security Best Practices](docs/security.md)
- 📊 [Monitoring Setup](docs/monitoring.md)

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines
- Follow Infrastructure as Code best practices
- Write tests for new features
- Update documentation for changes
- Use semantic versioning for releases

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [HashiCorp Terraform](https://terraform.io) for Infrastructure as Code
- [AWS](https://aws.amazon.com) for cloud infrastructure
- [React](https://reactjs.org) and [Node.js](https://nodejs.org) communities
- [Docker](https://docker.com) for containerization

---

## 🌟 Star History

If you found this project helpful, please consider giving it a ⭐!

```


# Clone and explore the project

git clone <repository-url>
cd terraform-3tier-devops

# Start your DevOps journey!

make up

```

**Ready to deploy your next 3-tier application? All the tools and knowledge are right here! 🚀**

---

*Built with ❤️ for the DevOps community*
```

This comprehensive README.md file provides:

1. **Clear project overview** with architecture diagrams
2. **Complete feature list** highlighting production-readiness
3. **Technology stack** with explanations
4. **Quick start guide** for immediate use
5. **Detailed project structure** for navigation
6. **Environment configurations** for different deployment scenarios
7. **CI/CD pipeline documentation**
8. **Monitoring and troubleshooting guides**
9. **Development commands** and workflows
10. **Contributing guidelines** for collaboration

The README is structured to be both informative for newcomers and useful as a reference for experienced users, making the project accessible and professional.

