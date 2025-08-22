# Create comprehensive Terraform DevOps project structure
import os

# Create the complete project structure
project_files = {}

# Root level files
project_files["README.md"] = '''# DevOps 3-Tier Web Application with Terraform

## 🚀 Project Overview

This project demonstrates a complete DevOps implementation for deploying a 3-tier web application on AWS using Terraform, featuring Infrastructure as Code (IaC), CI/CD pipelines, and best practices for scalable cloud architecture.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         AWS CLOUD                               │
│                                                                 │
│ ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│ │   Frontend      │  │    Backend      │  │    Database     │  │
│ │   (React.js)    │  │  (Node.js API)  │  │   (RDS MySQL)   │  │
│ │                 │  │                 │  │                 │  │
│ │ • ALB           │  │ • ECS Fargate   │  │ • Multi-AZ      │  │
│ │ • Auto Scaling  │  │ • Auto Scaling  │  │ • Automated     │  │
│ │ • CloudFront    │  │ • Health Checks │  │   Backups       │  │
│ └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🛠️ Technology Stack

- **Infrastructure**: Terraform, AWS (VPC, ALB, ECS, RDS, CloudWatch)
- **Frontend**: React.js, NGINX
- **Backend**: Node.js, Express.js, RESTful API
- **Database**: MySQL 8.0 (RDS Multi-AZ)
- **CI/CD**: GitHub Actions, AWS CodeDeploy
- **Monitoring**: CloudWatch, AWS X-Ray
- **Security**: IAM, Security Groups, KMS encryption

## 📁 Project Structure

```
.
├── .github/
│   └── workflows/          # GitHub Actions CI/CD pipelines
├── application/
│   ├── frontend/           # React.js application
│   └── backend/            # Node.js API
├── terraform/
│   ├── environments/       # Environment-specific configs
│   │   ├── dev/
│   │   ├── staging/
│   │   └── prod/
│   └── modules/           # Reusable Terraform modules
│       ├── vpc/
│       ├── alb/
│       ├── ecs/
│       ├── rds/
│       └── security/
├── scripts/               # Deployment and utility scripts
├── docs/                 # Additional documentation
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- AWS CLI configured with appropriate permissions
- Terraform >= 1.0 installed
- Docker installed (for local development)
- Node.js 16+ (for application development)

### Deployment Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd terraform-3tier-devops
   ```

2. **Configure AWS credentials**
   ```bash
   aws configure
   ```

3. **Set up Terraform backend**
   ```bash
   cd terraform/environments/dev
   terraform init
   ```

4. **Plan and apply infrastructure**
   ```bash
   terraform plan
   terraform apply
   ```

5. **Deploy application**
   ```bash
   ./scripts/deploy.sh dev
   ```

## 🌍 Environments

- **Development**: Single AZ, minimal resources, auto-shutdown
- **Staging**: Multi-AZ, production-like, limited scaling
- **Production**: Multi-AZ, high availability, full scaling, monitoring

## 🔒 Security Features

- VPC with private subnets for application and database tiers
- Security groups with least privilege access
- Encrypted storage and transit
- IAM roles with minimal required permissions
- VPC Flow Logs for network monitoring
- AWS Systems Manager for secure server access

## 📊 Monitoring & Observability

- CloudWatch metrics and alarms
- Application and infrastructure logs
- Health checks for all services
- Automated alerting via SNS
- Performance monitoring with AWS X-Ray

## 🔄 CI/CD Pipeline

- **Pull Request**: Terraform plan, security scan, code review
- **Merge to Main**: Automatic deployment to dev environment
- **Release Tag**: Deployment to staging and production
- **Rollback**: Automated rollback on deployment failure

## 🧪 Testing

- Unit tests for application code
- Integration tests for API endpoints
- Infrastructure tests with Terratest
- Security scans with tfsec
- Load testing for performance validation

## 📚 Documentation

- [Architecture Overview](docs/architecture.md)
- [Deployment Guide](docs/deployment.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Security Best Practices](docs/security.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and add tests
4. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for demonstrating DevOps best practices**
'''

# GitHub Actions workflows
project_files[".github/workflows/terraform-plan.yml"] = '''name: 'Terraform Plan'

on:
  pull_request:
    branches: [ main, develop ]
    paths: 
      - 'terraform/**'
      - '.github/workflows/terraform-*.yml'

env:
  TF_VERSION: '1.5.0'
  AWS_REGION: 'us-east-1'

jobs:
  terraform-plan:
    name: 'Terraform Plan'
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        environment: [dev, staging]
    
    defaults:
      run:
        working-directory: terraform/environments/${{ matrix.environment }}
    
    steps:
    - name: Checkout
      uses: actions/checkout@v4
    
    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v3
      with:
        terraform_version: ${{ env.TF_VERSION }}
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}
    
    - name: Terraform Format Check
      run: terraform fmt -check -recursive
    
    - name: Terraform Init
      run: terraform init
    
    - name: Terraform Validate
      run: terraform validate
    
    - name: Terraform Plan
      id: plan
      run: |
        terraform plan -no-color -out=tfplan
        terraform show -no-color tfplan > plan.txt
      continue-on-error: true
    
    - name: Comment Plan on PR
      if: github.event_name == 'pull_request'
      uses: actions/github-script@v7
      with:
        script: |
          const fs = require('fs');
          const plan = fs.readFileSync('terraform/environments/${{ matrix.environment }}/plan.txt', 'utf8');
          
          const output = `
          #### Terraform Plan for ${{ matrix.environment }} 📖
          
          <details><summary>Show Plan</summary>
          
          \\`\\`\\`terraform
          ${plan}
          \\`\\`\\`
          
          </details>
          `;
          
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: output
          })
    
    - name: Security Scan
      uses: aquasecurity/tfsec-action@v1.0.3
      with:
        working_directory: terraform/environments/${{ matrix.environment }}
        
    - name: Upload Plan Artifact
      uses: actions/upload-artifact@v4
      with:
        name: terraform-plan-${{ matrix.environment }}
        path: terraform/environments/${{ matrix.environment }}/tfplan
        retention-days: 5
'''

project_files[".github/workflows/terraform-apply.yml"] = '''name: 'Terraform Apply'

on:
  push:
    branches: [ main ]
    paths: 
      - 'terraform/**'
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy'
        required: true
        default: 'dev'
        type: choice
        options:
          - dev
          - staging
          - prod

env:
  TF_VERSION: '1.5.0'
  AWS_REGION: 'us-east-1'

jobs:
  terraform-apply:
    name: 'Terraform Apply'
    runs-on: ubuntu-latest
    environment: ${{ github.event.inputs.environment || 'dev' }}
    
    defaults:
      run:
        working-directory: terraform/environments/${{ github.event.inputs.environment || 'dev' }}
    
    steps:
    - name: Checkout
      uses: actions/checkout@v4
    
    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v3
      with:
        terraform_version: ${{ env.TF_VERSION }}
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}
    
    - name: Terraform Init
      run: terraform init
    
    - name: Terraform Plan
      run: terraform plan -out=tfplan
    
    - name: Terraform Apply
      if: github.ref == 'refs/heads/main' || github.event_name == 'workflow_dispatch'
      run: terraform apply tfplan
    
    - name: Output Infrastructure URLs
      run: |
        echo "## Deployment Complete! 🚀" >> $GITHUB_STEP_SUMMARY
        echo "### Infrastructure Outputs:" >> $GITHUB_STEP_SUMMARY
        terraform output -json | jq -r 'to_entries[] | "- **\\(.key)**: \\(.value.value)"' >> $GITHUB_STEP_SUMMARY
'''

# Environment-specific configurations
environments = ["dev", "staging", "prod"]

for env in environments:
    # Main configuration
    project_files[f"terraform/environments/{env}/main.tf"] = f'''# {env.title()} Environment Configuration
terraform {{
  required_version = ">= 1.0"
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }}
  }}
  backend "s3" {{
    bucket         = "terraform-state-3tier-{env}"
    key            = "infrastructure/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }}
}}

provider "aws" {{
  region = var.aws_region
  
  default_tags {{
    tags = {{
      Environment = "{env}"
      Project     = "3tier-webapp"
      ManagedBy   = "terraform"
      Owner       = "devops-team"
    }}
  }}
}}

locals {{
  environment = "{env}"
  is_production = local.environment == "prod"
  
  common_tags = {{
    Environment = local.environment
    Project     = "3tier-webapp"
    ManagedBy   = "terraform"
  }}
}}

# VPC Module
module "vpc" {{
  source = "../../modules/vpc"
  
  environment         = local.environment
  vpc_cidr           = var.vpc_cidr
  availability_zones = var.availability_zones
  public_subnet_cidrs = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  database_subnet_cidrs = var.database_subnet_cidrs
  
  common_tags = local.common_tags
}}

# Security Module
module "security" {{
  source = "../../modules/security"
  
  environment = local.environment
  vpc_id      = module.vpc.vpc_id
  
  common_tags = local.common_tags
}}

# Application Load Balancer Module
module "alb" {{
  source = "../../modules/alb"
  
  environment           = local.environment
  vpc_id               = module.vpc.vpc_id
  public_subnet_ids    = module.vpc.public_subnet_ids
  alb_security_group_id = module.security.alb_security_group_id
  
  common_tags = local.common_tags
}}

# ECS Module for Backend
module "ecs" {{
  source = "../../modules/ecs"
  
  environment              = local.environment
  vpc_id                  = module.vpc.vpc_id
  private_subnet_ids      = module.vpc.private_subnet_ids
  ecs_security_group_id   = module.security.ecs_security_group_id
  alb_target_group_arn    = module.alb.backend_target_group_arn
  
  # Application configuration
  app_image               = var.backend_image
  app_port                = var.backend_port
  cpu                     = var.backend_cpu
  memory                  = var.backend_memory
  desired_count          = var.backend_desired_count
  max_capacity           = var.backend_max_capacity
  min_capacity           = var.backend_min_capacity
  
  # Database configuration
  database_url           = module.rds.database_url
  
  common_tags = local.common_tags
}}

# RDS Module
module "rds" {{
  source = "../../modules/rds"
  
  environment               = local.environment
  vpc_id                   = module.vpc.vpc_id
  database_subnet_ids      = module.vpc.database_subnet_ids
  rds_security_group_id    = module.security.rds_security_group_id
  
  # Database configuration
  db_name                  = var.db_name
  db_username              = var.db_username
  db_password              = var.db_password
  db_instance_class        = var.db_instance_class
  allocated_storage        = var.db_allocated_storage
  max_allocated_storage    = var.db_max_allocated_storage
  multi_az                = local.is_production
  backup_retention_period = local.is_production ? 7 : 1
  
  common_tags = local.common_tags
}}

# CloudWatch Module for Monitoring
module "monitoring" {{
  source = "../../modules/monitoring"
  
  environment          = local.environment
  alb_arn_suffix      = module.alb.alb_arn_suffix
  ecs_cluster_name    = module.ecs.cluster_name
  ecs_service_name    = module.ecs.service_name
  rds_instance_id     = module.rds.instance_id
  
  common_tags = local.common_tags
}}
'''

    # Variables
    if env == "dev":
        project_files[f"terraform/environments/{env}/terraform.tfvars"] = '''# Development Environment Variables
aws_region = "us-east-1"

# Networking
vpc_cidr = "10.0.0.0/16"
availability_zones = ["us-east-1a", "us-east-1b"]
public_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]
private_subnet_cidrs = ["10.0.3.0/24", "10.0.4.0/24"]
database_subnet_cidrs = ["10.0.5.0/24", "10.0.6.0/24"]

# Backend ECS Configuration
backend_image = "your-account.dkr.ecr.us-east-1.amazonaws.com/backend:latest"
backend_port = 3000
backend_cpu = 256
backend_memory = 512
backend_desired_count = 1
backend_min_capacity = 1
backend_max_capacity = 3

# Database Configuration
db_name = "webapp_dev"
db_username = "admin"
db_password = "dev-password-123" # Use AWS Secrets Manager in production
db_instance_class = "db.t3.micro"
db_allocated_storage = 20
db_max_allocated_storage = 100
'''
    elif env == "staging":
        project_files[f"terraform/environments/{env}/terraform.tfvars"] = '''# Staging Environment Variables
aws_region = "us-east-1"

# Networking
vpc_cidr = "10.1.0.0/16"
availability_zones = ["us-east-1a", "us-east-1b"]
public_subnet_cidrs = ["10.1.1.0/24", "10.1.2.0/24"]
private_subnet_cidrs = ["10.1.3.0/24", "10.1.4.0/24"]
database_subnet_cidrs = ["10.1.5.0/24", "10.1.6.0/24"]

# Backend ECS Configuration
backend_image = "your-account.dkr.ecr.us-east-1.amazonaws.com/backend:staging"
backend_port = 3000
backend_cpu = 512
backend_memory = 1024
backend_desired_count = 2
backend_min_capacity = 2
backend_max_capacity = 8

# Database Configuration
db_name = "webapp_staging"
db_username = "admin"
db_password = "staging-password-123" # Use AWS Secrets Manager in production
db_instance_class = "db.t3.small"
db_allocated_storage = 50
db_max_allocated_storage = 200
'''
    else:  # prod
        project_files[f"terraform/environments/{env}/terraform.tfvars"] = '''# Production Environment Variables
aws_region = "us-east-1"

# Networking
vpc_cidr = "10.2.0.0/16"
availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
public_subnet_cidrs = ["10.2.1.0/24", "10.2.2.0/24", "10.2.3.0/24"]
private_subnet_cidrs = ["10.2.4.0/24", "10.2.5.0/24", "10.2.6.0/24"]
database_subnet_cidrs = ["10.2.7.0/24", "10.2.8.0/24", "10.2.9.0/24"]

# Backend ECS Configuration
backend_image = "your-account.dkr.ecr.us-east-1.amazonaws.com/backend:latest"
backend_port = 3000
backend_cpu = 1024
backend_memory = 2048
backend_desired_count = 3
backend_min_capacity = 3
backend_max_capacity = 20

# Database Configuration
db_name = "webapp_prod"
db_username = "admin"
db_password = "prod-password-123" # Use AWS Secrets Manager in production
db_instance_class = "db.t3.medium"
db_allocated_storage = 100
db_max_allocated_storage = 500
'''

    # Variables definition
    project_files[f"terraform/environments/{env}/variables.tf"] = '''variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

# Networking Variables
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
}

variable "database_subnet_cidrs" {
  description = "CIDR blocks for database subnets"
  type        = list(string)
}

# Backend Application Variables
variable "backend_image" {
  description = "Docker image for backend application"
  type        = string
}

variable "backend_port" {
  description = "Port for backend application"
  type        = number
  default     = 3000
}

variable "backend_cpu" {
  description = "CPU units for backend task"
  type        = number
}

variable "backend_memory" {
  description = "Memory for backend task"
  type        = number
}

variable "backend_desired_count" {
  description = "Desired number of backend tasks"
  type        = number
}

variable "backend_min_capacity" {
  description = "Minimum capacity for backend auto scaling"
  type        = number
}

variable "backend_max_capacity" {
  description = "Maximum capacity for backend auto scaling"
  type        = number
}

# Database Variables
variable "db_name" {
  description = "Name of the database"
  type        = string
}

variable "db_username" {
  description = "Username for the database"
  type        = string
}

variable "db_password" {
  description = "Password for the database"
  type        = string
  sensitive   = true
}

variable "db_instance_class" {
  description = "Instance class for RDS"
  type        = string
}

variable "db_allocated_storage" {
  description = "Initial allocated storage for RDS"
  type        = number
}

variable "db_max_allocated_storage" {
  description = "Maximum allocated storage for RDS"
  type        = number
}
'''

    # Outputs
    project_files[f"terraform/environments/{env}/outputs.tf"] = '''output "vpc_id" {
  description = "ID of the VPC"
  value       = module.vpc.vpc_id
}

output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = module.alb.alb_dns_name
}

output "alb_zone_id" {
  description = "Zone ID of the Application Load Balancer"
  value       = module.alb.alb_zone_id
}

output "database_endpoint" {
  description = "Database endpoint"
  value       = module.rds.endpoint
  sensitive   = true
}

output "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  value       = module.ecs.cluster_name
}

output "ecs_service_name" {
  description = "Name of the ECS service"
  value       = module.ecs.service_name
}

output "environment_url" {
  description = "URL to access the application"
  value       = "http://${module.alb.alb_dns_name}"
}
'''

print("Created environment-specific configurations for:", ", ".join(environments))
print(f"Total files created so far: {len(project_files)}")