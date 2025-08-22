# Create final documentation and save project to CSV

# Additional documentation files
project_files["docs/architecture.md"] = '''# Architecture Overview

## System Architecture

The 3-Tier Web Application follows a modern cloud-native architecture deployed on AWS:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              AWS CLOUD                                  │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                        PRESENTATION TIER                        │   │
│  │                                                                 │   │
│  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │   │
│  │  │    ALB       │    │   Frontend   │    │  CloudFront  │     │   │
│  │  │  (Routes     │───▶│  (React.js)  │◄───│   (CDN)      │     │   │
│  │  │   Traffic)   │    │   Container  │    │  [Optional]  │     │   │
│  │  └──────────────┘    └──────────────┘    └──────────────┘     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                 │                                       │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                       APPLICATION TIER                          │   │
│  │                                                                 │   │
│  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │   │
│  │  │     ALB      │    │     ECS      │    │  Auto Scale  │     │   │
│  │  │  (Backend    │───▶│  (Node.js)   │◄───│    Group     │     │   │
│  │  │   Routes)    │    │   Fargate    │    │             │     │   │
│  │  └──────────────┘    └──────────────┘    └──────────────┘     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                 │                                       │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                         DATA TIER                               │   │
│  │                                                                 │   │
│  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │   │
│  │  │     RDS      │    │  Read        │    │   Backup     │     │   │
│  │  │   MySQL      │───▶│ Replicas     │    │   & Point    │     │   │
│  │  │  Multi-AZ    │    │ [Production] │    │  in Time     │     │   │
│  │  └──────────────┘    └──────────────┘    └──────────────┘     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

## Network Architecture

### VPC Design
- **CIDR Block**: Environment-specific (10.0.0.0/16, 10.1.0.0/16, 10.2.0.0/16)
- **Multi-AZ Deployment**: 2-3 Availability Zones
- **Subnet Strategy**:
  - Public Subnets: ALB, NAT Gateways
  - Private Subnets: Application servers
  - Database Subnets: RDS instances (isolated)

### Security Groups
- **ALB Security Group**: HTTP/HTTPS from internet
- **Application Security Group**: Traffic from ALB only
- **Database Security Group**: MySQL from application tier only

## Component Details

### Frontend Tier
- **Technology**: React.js 18
- **Container**: Docker with NGINX
- **Deployment**: Served via ALB
- **Features**:
  - Responsive design
  - User CRUD operations
  - Real-time API integration
  - Health checks

### Application Tier
- **Technology**: Node.js + Express.js
- **Container**: Docker on ECS Fargate
- **Auto Scaling**: 2-20 tasks based on CPU/Memory
- **Features**:
  - RESTful API design
  - Database connection pooling
  - Request logging and monitoring
  - Health check endpoints
  - Graceful shutdown handling

### Data Tier
- **Technology**: MySQL 8.0 on RDS
- **High Availability**: Multi-AZ deployment (production)
- **Backup Strategy**: Automated backups with point-in-time recovery
- **Security**: Encryption at rest and in transit
- **Monitoring**: Performance Insights enabled

## Infrastructure as Code

### Terraform Structure
```
terraform/
├── environments/          # Environment-specific configs
│   ├── dev/
│   ├── staging/
│   └── prod/
└── modules/              # Reusable modules
    ├── vpc/             # Networking
    ├── alb/             # Load balancing
    ├── ecs/             # Container orchestration
    ├── rds/             # Database
    ├── security/        # Security groups
    └── monitoring/      # CloudWatch & alarms
```

### Module Dependencies
```
VPC → Security Groups → ALB
                     ↓
Security Groups → ECS Service
                     ↓
Security Groups → RDS Instance
```

## Deployment Architecture

### CI/CD Pipeline
1. **Code Commit** → Triggers GitHub Actions
2. **Build Phase** → Docker images built and pushed to ECR
3. **Infrastructure Phase** → Terraform plan and apply
4. **Application Phase** → ECS service update
5. **Verification Phase** → Health checks and monitoring

### Environment Promotion
- **Development**: Automatic deployment on merge
- **Staging**: Manual approval required
- **Production**: Manual approval + additional validations

## Monitoring & Observability

### Metrics Collection
- **Application Load Balancer**: Response time, error rates
- **ECS Services**: CPU, memory utilization
- **RDS Database**: Connection count, query performance
- **Custom Metrics**: Business logic metrics

### Logging Strategy
- **Application Logs**: Structured JSON logs to CloudWatch
- **Access Logs**: ALB access logs to S3
- **VPC Flow Logs**: Network traffic analysis
- **Audit Logs**: API access and data changes

### Alerting
- **Critical**: Service down, high error rates
- **Warning**: High resource utilization
- **Info**: Deployment notifications

## Security Architecture

### Network Security
- **VPC Isolation**: Private subnets for application and database
- **Security Groups**: Least privilege access rules
- **Network ACLs**: Additional subnet-level protection
- **VPC Flow Logs**: Network monitoring and forensics

### Application Security
- **IAM Roles**: Service-specific permissions
- **Secrets Management**: Database credentials in AWS Secrets Manager
- **Container Security**: Non-root users, minimal base images
- **API Security**: Rate limiting, input validation

### Data Security
- **Encryption at Rest**: RDS and S3 encryption
- **Encryption in Transit**: TLS for all communications
- **Backup Encryption**: Encrypted database backups
- **Key Management**: AWS KMS for encryption keys

## Scalability Design

### Horizontal Scaling
- **Frontend**: Multiple ALB targets
- **Backend**: ECS auto-scaling based on metrics
- **Database**: Read replicas for read-heavy workloads

### Vertical Scaling
- **ECS Tasks**: CPU/Memory can be adjusted
- **RDS Instance**: Instance class can be modified
- **Storage**: Auto-scaling storage for RDS

## Disaster Recovery

### Backup Strategy
- **Database**: Automated backups with 7-day retention
- **Code**: Git repository with multiple remotes
- **Infrastructure**: Terraform state in S3 with versioning

### Recovery Procedures
- **Data Recovery**: Point-in-time recovery from RDS backups
- **Infrastructure Recovery**: Terraform recreate from state
- **Application Recovery**: Deploy from container registry

### Business Continuity
- **Multi-AZ**: Database failover in minutes
- **Auto Scaling**: Automatic replacement of failed instances
- **Load Balancing**: Traffic redistribution on failures
'''

project_files["docs/deployment.md"] = '''# Deployment Guide

This guide covers deploying the 3-tier web application to AWS using Terraform and CI/CD pipelines.

## Prerequisites

### Required Tools
- AWS CLI v2
- Terraform >= 1.0
- Docker
- Node.js 16+
- Git

### AWS Account Setup
1. **AWS Account**: Active AWS account with appropriate permissions
2. **IAM User**: Programmatic access with required policies:
   - EC2FullAccess
   - RDSFullAccess
   - ECSFullAccess
   - VPCFullAccess
   - IAMFullAccess
   - S3FullAccess
   - CloudWatchFullAccess

## Initial Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd terraform-3tier-devops
```

### 2. Configure AWS Credentials
```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Default region name: us-east-1
# Default output format: json
```

### 3. Set Up Terraform Backend
```bash
chmod +x scripts/setup-backend.sh
./scripts/setup-backend.sh
```

This script creates:
- S3 buckets for Terraform state
- DynamoDB table for state locking
- ECR repositories for Docker images

## Environment Configuration

### Development Environment

1. **Navigate to dev environment**:
```bash
cd terraform/environments/dev
```

2. **Update terraform.tfvars**:
```hcl
# Basic Configuration
aws_region = "us-east-1"

# Networking
vpc_cidr = "10.0.0.0/16"
availability_zones = ["us-east-1a", "us-east-1b"]
public_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]
private_subnet_cidrs = ["10.0.3.0/24", "10.0.4.0/24"]
database_subnet_cidrs = ["10.0.5.0/24", "10.0.6.0/24"]

# Application Configuration
backend_image = "your-account.dkr.ecr.us-east-1.amazonaws.com/backend:latest"
backend_cpu = 256
backend_memory = 512
backend_desired_count = 1

# Database Configuration
db_name = "webapp_dev"
db_username = "admin"
db_password = "your-secure-password"
db_instance_class = "db.t3.micro"
```

3. **Initialize and Plan**:
```bash
terraform init
terraform plan
```

### Staging Environment

Similar to dev but with increased resources:
```hcl
# Application Configuration
backend_cpu = 512
backend_memory = 1024
backend_desired_count = 2

# Database Configuration
db_instance_class = "db.t3.small"
multi_az = true
```

### Production Environment

Production-ready configuration:
```hcl
# Application Configuration
backend_cpu = 1024
backend_memory = 2048
backend_desired_count = 3
backend_max_capacity = 20

# Database Configuration
db_instance_class = "db.t3.medium"
multi_az = true
backup_retention_period = 7
create_read_replica = true
```

## Manual Deployment

### Step-by-Step Deployment

1. **Build and Push Images**:
```bash
# Get ECR login
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com

# Build and push backend
docker build -t <account>.dkr.ecr.us-east-1.amazonaws.com/backend:latest ./application/backend
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/backend:latest

# Build and push frontend
docker build -t <account>.dkr.ecr.us-east-1.amazonaws.com/frontend:latest ./application/frontend
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/frontend:latest
```

2. **Deploy Infrastructure**:
```bash
cd terraform/environments/dev
terraform init
terraform plan
terraform apply
```

3. **Verify Deployment**:
```bash
# Get ALB DNS name
terraform output alb_dns_name

# Test application
curl http://<alb-dns-name>/health
curl http://<alb-dns-name>/api/users
```

## Automated Deployment

### Using Deployment Script

The project includes an automated deployment script:

```bash
# Deploy to development
./scripts/deploy.sh -e dev -d <your-ecr-registry>

# Deploy to staging
./scripts/deploy.sh -e staging -d <your-ecr-registry>

# Deploy to production
./scripts/deploy.sh -e prod -d <your-ecr-registry>
```

### Script Options
- `-e, --environment`: Environment (dev|staging|prod)
- `-r, --region`: AWS region
- `-d, --registry`: Docker registry URL
- `-v, --version`: Docker image version
- `--skip-build`: Skip Docker build
- `--skip-terraform`: Skip Terraform deployment

## CI/CD Pipeline Setup

### GitHub Actions Configuration

1. **Set Repository Secrets**:
```
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
DOCKER_REGISTRY=your-account.dkr.ecr.us-east-1.amazonaws.com
```

2. **Pipeline Behavior**:
- **Pull Request**: Terraform plan for dev/staging
- **Main Branch**: Auto-deploy to dev
- **Release Tag**: Deploy to staging/production

### Manual Pipeline Trigger

```bash
# Trigger deployment via GitHub CLI
gh workflow run "Terraform Apply" --ref main -f environment=dev
```

## Local Development

### Docker Compose Setup

1. **Start Services**:
```bash
docker-compose up -d
```

2. **Access Application**:
- Frontend: http://localhost:80
- Backend: http://localhost:3000
- Database: localhost:3306

3. **Development Commands**:
```bash
# View logs
make logs

# Run tests
make test

# Stop services
make down
```

## Monitoring Deployment

### Health Checks

1. **Application Health**:
```bash
curl http://<alb-dns>/health
```

2. **ECS Service Status**:
```bash
aws ecs describe-services --cluster <cluster-name> --services <service-name>
```

3. **RDS Status**:
```bash
aws rds describe-db-instances --db-instance-identifier <db-identifier>
```

### CloudWatch Monitoring

- **Dashboard**: AWS Console → CloudWatch → Dashboards
- **Alarms**: Monitor CPU, memory, response times
- **Logs**: Application and infrastructure logs

## Troubleshooting

### Common Issues

1. **ECS Task Fails to Start**:
```bash
# Check task definition
aws ecs describe-task-definition --task-definition <task-def-arn>

# Check service events
aws ecs describe-services --cluster <cluster> --services <service>
```

2. **Database Connection Issues**:
```bash
# Check security groups
aws ec2 describe-security-groups --group-ids <sg-id>

# Test connectivity from ECS
aws ecs execute-command --cluster <cluster> --task <task-arn> --command "nc -zv <db-endpoint> 3306"
```

3. **ALB Health Check Failures**:
```bash
# Check target group health
aws elbv2 describe-target-health --target-group-arn <tg-arn>

# Check application logs
aws logs tail /ecs/<environment>/app
```

### Debugging Commands

```bash
# Terraform debug
export TF_LOG=DEBUG
terraform apply

# AWS CLI debug
aws ecs describe-services --debug --cluster <cluster> --services <service>

# Docker debug
docker logs <container-id>
```

## Rollback Procedures

### Application Rollback

1. **ECS Service Rollback**:
```bash
# Get previous task definition
aws ecs describe-services --cluster <cluster> --services <service>

# Update service with previous task definition
aws ecs update-service --cluster <cluster> --service <service> --task-definition <previous-task-def>
```

2. **Infrastructure Rollback**:
```bash
# Terraform rollback (use previous state)
terraform plan -target=<resource>
terraform apply -target=<resource>
```

### Database Rollback

```bash
# Point-in-time recovery
aws rds restore-db-instance-to-point-in-time \
  --source-db-instance-identifier <source-db> \
  --target-db-instance-identifier <target-db> \
  --restore-time <timestamp>
```

## Security Considerations

### Pre-deployment Checklist
- [ ] Secrets stored in AWS Secrets Manager
- [ ] Security groups follow least privilege
- [ ] Database in private subnets
- [ ] Encryption enabled for RDS and S3
- [ ] VPC Flow Logs enabled
- [ ] CloudTrail enabled for auditing

### Post-deployment Validation
- [ ] Application accessible via HTTPS
- [ ] Database not publicly accessible
- [ ] Health checks passing
- [ ] Monitoring and alerting configured
- [ ] Backup strategy validated

## Production Deployment Checklist

### Before Production Deploy
- [ ] All tests pass in staging
- [ ] Performance testing completed
- [ ] Security scan completed
- [ ] Backup and recovery tested
- [ ] Rollback plan prepared
- [ ] Team notification sent

### During Production Deploy
- [ ] Monitor application metrics
- [ ] Watch for errors in logs
- [ ] Verify health checks
- [ ] Test critical functionality
- [ ] Confirm database connectivity

### After Production Deploy
- [ ] Validate all features working
- [ ] Check monitoring dashboards
- [ ] Verify backup job runs
- [ ] Update documentation
- [ ] Send completion notification
'''

# Create environment file
project_files[".env.example"] = '''# Environment Configuration Template
# Copy this file to .env and update with your values

# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCOUNT_ID=123456789012

# Docker Registry
DOCKER_REGISTRY=123456789012.dkr.ecr.us-east-1.amazonaws.com

# Application Configuration
NODE_ENV=development
PORT=3000

# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=webapp_dev
DB_USER=appuser
DB_PASSWORD=apppassword

# Frontend Configuration
REACT_APP_API_URL=http://localhost:3000

# Terraform Configuration
TF_VAR_db_password=your-secure-password
TF_VAR_environment=dev

# CI/CD Configuration
GITHUB_TOKEN=ghp_your_github_token
'''

# Create gitignore
project_files[".gitignore"] = '''# Dependencies
node_modules/
*/node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Production builds
build/
dist/
*/build/
*/dist/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Terraform
*.tfstate
*.tfstate.*
*.tfvars
!*.tfvars.example
.terraform/
.terraform.lock.hcl
terraform.tfplan
tfplan

# AWS
.aws/
outputs.json

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Docker
*.tar
*.tar.gz

# Coverage
coverage/
*.lcov
.nyc_output/

# Temporary files
tmp/
temp/
.cache/

# Database
*.sql
*.db
*.sqlite3

# Backup files
*.backup
*.bak

# Certificates
*.pem
*.key
*.crt

# Local development
docker-compose.override.yml
'''

print("Created documentation and configuration files")

# Create comprehensive CSV file with all project files
import pandas as pd

# Prepare data for CSV
files_data = []
for file_path, content in project_files.items():
    folder_structure = file_path.split('/')
    
    category = "Root"
    if len(folder_structure) > 1:
        if folder_structure[0] == ".github":
            category = "CI/CD"
        elif folder_structure[0] == "terraform":
            if "modules" in folder_structure:
                category = f"Terraform Module - {folder_structure[2].title()}"
            else:
                category = f"Terraform Environment - {folder_structure[2].title()}"
        elif folder_structure[0] == "application":
            category = f"Application - {folder_structure[1].title()}"
        elif folder_structure[0] == "scripts":
            category = "Scripts"
        elif folder_structure[0] == "docs":
            category = "Documentation"
    
    file_type = file_path.split('.')[-1] if '.' in file_path.split('/')[-1] else 'directory'
    
    files_data.append({
        'File Path': file_path,
        'Category': category,
        'File Type': file_type,
        'Description': get_file_description(file_path),
        'Size (chars)': len(content),
        'Lines': content.count('\n') + 1 if content else 0
    })

def get_file_description(file_path):
    """Generate description for each file based on path"""
    descriptions = {
        'README.md': 'Main project documentation and setup guide',
        'Makefile': 'Automation commands for development and deployment',
        'docker-compose.yml': 'Local development environment with Docker',
        '.env.example': 'Environment variables template',
        '.gitignore': 'Git ignore patterns for the project',
        'deploy.sh': 'Automated deployment script for all environments',
        'setup-backend.sh': 'Script to initialize Terraform backend infrastructure',
        'init.sql': 'Database initialization script with sample data',
    }
    
    filename = file_path.split('/')[-1]
    
    if filename in descriptions:
        return descriptions[filename]
    elif 'terraform-plan.yml' in file_path:
        return 'GitHub Actions workflow for Terraform planning'
    elif 'terraform-apply.yml' in file_path:
        return 'GitHub Actions workflow for Terraform deployment'
    elif 'main.tf' in file_path:
        return 'Main Terraform configuration file'
    elif 'variables.tf' in file_path:
        return 'Terraform input variables definition'
    elif 'outputs.tf' in file_path:
        return 'Terraform output values definition'
    elif 'terraform.tfvars' in file_path:
        return 'Environment-specific Terraform variable values'
    elif 'Dockerfile' in filename:
        return 'Container image definition'
    elif 'package.json' in filename:
        return 'Node.js project dependencies and scripts'
    elif 'server.js' in filename:
        return 'Express.js backend API server'
    elif 'App.js' in filename:
        return 'Main React.js application component'
    elif 'nginx.conf' in filename:
        return 'NGINX web server configuration'
    elif file_path.endswith('.md'):
        return 'Documentation file in Markdown format'
    else:
        return 'Project configuration file'

# Create DataFrame and save to CSV
df = pd.DataFrame(files_data)
df = df.sort_values(['Category', 'File Path'])

# Add summary statistics
total_files = len(df)
total_size = df['Size (chars)'].sum()
total_lines = df['Lines'].sum()

# Save to CSV
csv_filename = 'terraform_3tier_devops_project_complete.csv'
df.to_csv(csv_filename, index=False)

print(f"\\n📊 Project Statistics:")
print(f"Total Files: {total_files}")
print(f"Total Characters: {total_size:,}")
print(f"Total Lines of Code: {total_lines:,}")
print(f"\\nFiles by Category:")
category_counts = df['Category'].value_counts()
for category, count in category_counts.items():
    print(f"  {category}: {count} files")

print(f"\\n✅ Complete project saved to: {csv_filename}")
print(f"\\n🚀 Project Features:")
print("- ✅ Complete 3-tier architecture (React, Node.js, MySQL)")
print("- ✅ Full Terraform infrastructure as code")
print("- ✅ Multi-environment support (dev, staging, prod)")
print("- ✅ CI/CD pipelines with GitHub Actions")
print("- ✅ Docker containerization")
print("- ✅ Auto-scaling and load balancing")
print("- ✅ Database with Multi-AZ and backups")
print("- ✅ Comprehensive monitoring and alerting")
print("- ✅ Security best practices")
print("- ✅ Local development environment")
print("- ✅ Automated deployment scripts")
print("- ✅ Complete documentation")

# Display file structure summary
print(f"\\n📁 Project Structure Overview:")
print("terraform-3tier-devops/")
structure_items = [
    "├── .github/workflows/          # CI/CD pipelines",
    "├── application/",
    "│   ├── frontend/               # React.js app",
    "│   └── backend/                # Node.js API",
    "├── terraform/",
    "│   ├── environments/           # Dev, staging, prod configs",
    "│   └── modules/                # Reusable infrastructure modules",
    "├── scripts/                    # Deployment and utility scripts",
    "├── docs/                       # Architecture and deployment docs",
    "├── docker-compose.yml          # Local development",
    "├── Makefile                    # Development commands",
    "└── README.md                   # Project documentation"
]

for item in structure_items:
    print(item)

print(f"\\n🎯 Ready for deployment! Use the interactive web app above to explore all files and configurations.")