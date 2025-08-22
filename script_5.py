# Create deployment scripts and documentation

# Deployment scripts
project_files["scripts/deploy.sh"] = '''#!/bin/bash

# 3-Tier Application Deployment Script
set -e

# Colors for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m' # No Color

# Default values
ENVIRONMENT="dev"
AWS_REGION="us-east-1"
DOCKER_REGISTRY=""
VERSION="latest"
SKIP_BUILD=false
SKIP_TERRAFORM=false

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -e, --environment   Environment to deploy (dev|staging|prod)"
    echo "  -r, --region        AWS region (default: us-east-1)"
    echo "  -d, --registry      Docker registry URL"
    echo "  -v, --version       Docker image version (default: latest)"
    echo "  --skip-build        Skip Docker image build"
    echo "  --skip-terraform    Skip Terraform deployment"
    echo "  -h, --help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 -e dev"
    echo "  $0 -e prod -r us-west-2 -d 123456789.dkr.ecr.us-west-2.amazonaws.com"
    exit 1
}

check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if required commands exist
    local commands=("aws" "terraform" "docker" "jq")
    for cmd in "${commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            log_error "$cmd is not installed or not in PATH"
            exit 1
        fi
    done
    
    # Check AWS credentials
    if ! aws sts get-caller-identity &> /dev/null; then
        log_error "AWS credentials not configured properly"
        exit 1
    fi
    
    # Check Docker daemon
    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running"
        exit 1
    fi
    
    log_success "All prerequisites met!"
}

build_and_push_images() {
    if [ "$SKIP_BUILD" = true ]; then
        log_warning "Skipping Docker build as requested"
        return
    fi
    
    log_info "Building and pushing Docker images..."
    
    # Get ECR login token
    aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "$DOCKER_REGISTRY"
    
    # Build and push backend
    log_info "Building backend image..."
    docker build -t "${DOCKER_REGISTRY}/backend:${VERSION}" ./application/backend
    docker push "${DOCKER_REGISTRY}/backend:${VERSION}"
    
    # Build and push frontend
    log_info "Building frontend image..."
    docker build -t "${DOCKER_REGISTRY}/frontend:${VERSION}" ./application/frontend
    docker push "${DOCKER_REGISTRY}/frontend:${VERSION}"
    
    log_success "Docker images built and pushed successfully!"
}

deploy_infrastructure() {
    if [ "$SKIP_TERRAFORM" = true ]; then
        log_warning "Skipping Terraform deployment as requested"
        return
    fi
    
    log_info "Deploying infrastructure with Terraform..."
    
    cd "terraform/environments/$ENVIRONMENT"
    
    # Initialize Terraform
    terraform init
    
    # Validate configuration
    terraform validate
    
    # Plan deployment
    log_info "Creating Terraform plan..."
    terraform plan -out=tfplan
    
    # Apply if plan is successful
    log_info "Applying Terraform configuration..."
    terraform apply tfplan
    
    # Get outputs
    log_info "Getting infrastructure outputs..."
    terraform output -json > ../../../outputs.json
    
    cd - > /dev/null
    
    log_success "Infrastructure deployed successfully!"
}

update_ecs_service() {
    log_info "Updating ECS service..."
    
    # Get cluster and service names from Terraform outputs
    CLUSTER_NAME=$(jq -r '.ecs_cluster_name.value' outputs.json)
    SERVICE_NAME=$(jq -r '.ecs_service_name.value' outputs.json)
    
    if [ "$CLUSTER_NAME" != "null" ] && [ "$SERVICE_NAME" != "null" ]; then
        aws ecs update-service \\
            --cluster "$CLUSTER_NAME" \\
            --service "$SERVICE_NAME" \\
            --force-new-deployment \\
            --region "$AWS_REGION"
        
        log_info "Waiting for service to stabilize..."
        aws ecs wait services-stable \\
            --cluster "$CLUSTER_NAME" \\
            --services "$SERVICE_NAME" \\
            --region "$AWS_REGION"
        
        log_success "ECS service updated successfully!"
    else
        log_warning "Could not find ECS cluster or service information"
    fi
}

run_health_checks() {
    log_info "Running health checks..."
    
    # Get ALB DNS name from outputs
    ALB_DNS=$(jq -r '.alb_dns_name.value' outputs.json)
    
    if [ "$ALB_DNS" != "null" ]; then
        # Wait for ALB to be ready
        log_info "Waiting for application to be healthy..."
        sleep 30
        
        # Check health endpoint
        local max_attempts=10
        local attempt=1
        
        while [ $attempt -le $max_attempts ]; do
            log_info "Health check attempt $attempt/$max_attempts..."
            
            if curl -f -s "http://$ALB_DNS/health" > /dev/null; then
                log_success "Application is healthy!"
                break
            fi
            
            if [ $attempt -eq $max_attempts ]; then
                log_error "Application failed health checks"
                return 1
            fi
            
            sleep 10
            ((attempt++))
        done
    else
        log_warning "Could not find ALB DNS name for health check"
    fi
}

cleanup() {
    log_info "Cleaning up temporary files..."
    rm -f outputs.json
    rm -f terraform/environments/*/tfplan
}

show_deployment_info() {
    log_info "Deployment Information:"
    echo "=========================="
    echo "Environment: $ENVIRONMENT"
    echo "Region: $AWS_REGION"
    echo "Version: $VERSION"
    
    if [ -f "outputs.json" ]; then
        ALB_DNS=$(jq -r '.alb_dns_name.value' outputs.json 2>/dev/null)
        if [ "$ALB_DNS" != "null" ] && [ "$ALB_DNS" != "" ]; then
            echo "Application URL: http://$ALB_DNS"
        fi
    fi
    echo "=========================="
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -e|--environment)
            ENVIRONMENT="$2"
            shift 2
            ;;
        -r|--region)
            AWS_REGION="$2"
            shift 2
            ;;
        -d|--registry)
            DOCKER_REGISTRY="$2"
            shift 2
            ;;
        -v|--version)
            VERSION="$2"
            shift 2
            ;;
        --skip-build)
            SKIP_BUILD=true
            shift
            ;;
        --skip-terraform)
            SKIP_TERRAFORM=true
            shift
            ;;
        -h|--help)
            show_usage
            ;;
        *)
            log_error "Unknown option: $1"
            show_usage
            ;;
    esac
done

# Validate environment
if [[ ! "$ENVIRONMENT" =~ ^(dev|staging|prod)$ ]]; then
    log_error "Invalid environment: $ENVIRONMENT. Must be dev, staging, or prod."
    exit 1
fi

# Main execution
main() {
    log_info "Starting deployment for $ENVIRONMENT environment..."
    
    check_prerequisites
    
    if [ "$SKIP_BUILD" != true ] && [ -z "$DOCKER_REGISTRY" ]; then
        log_error "Docker registry URL is required when building images"
        log_info "Use -d/--registry option or --skip-build to skip building"
        exit 1
    fi
    
    # Set trap to cleanup on exit
    trap cleanup EXIT
    
    if [ "$SKIP_BUILD" != true ]; then
        build_and_push_images
    fi
    
    deploy_infrastructure
    
    if [ "$SKIP_TERRAFORM" != true ]; then
        update_ecs_service
        run_health_checks
    fi
    
    show_deployment_info
    
    log_success "Deployment completed successfully! 🎉"
}

# Run main function
main "$@"
'''

# Infrastructure setup script
project_files["scripts/setup-backend.sh"] = '''#!/bin/bash

# Terraform Backend Setup Script
set -e

# Colors for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m' # No Color

# Default values
AWS_REGION="us-east-1"
PROJECT_NAME="3tier-webapp"

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -r, --region        AWS region (default: us-east-1)"
    echo "  -p, --project       Project name (default: 3tier-webapp)"
    echo "  -h, --help          Show this help message"
    exit 1
}

check_aws_credentials() {
    log_info "Checking AWS credentials..."
    if ! aws sts get-caller-identity &> /dev/null; then
        log_error "AWS credentials not configured properly"
        exit 1
    fi
    log_success "AWS credentials verified"
}

create_s3_buckets() {
    log_info "Creating S3 buckets for Terraform state..."
    
    local environments=("dev" "staging" "prod")
    
    for env in "${environments[@]}"; do
        local bucket_name="terraform-state-${PROJECT_NAME}-${env}"
        
        log_info "Creating bucket: $bucket_name"
        
        # Create bucket
        if aws s3 mb "s3://$bucket_name" --region "$AWS_REGION" 2>/dev/null; then
            log_success "Created bucket: $bucket_name"
        else
            log_warning "Bucket $bucket_name already exists or creation failed"
        fi
        
        # Enable versioning
        aws s3api put-bucket-versioning \\
            --bucket "$bucket_name" \\
            --versioning-configuration Status=Enabled
        
        # Enable server-side encryption
        aws s3api put-bucket-encryption \\
            --bucket "$bucket_name" \\
            --server-side-encryption-configuration '{
                "Rules": [
                    {
                        "ApplyServerSideEncryptionByDefault": {
                            "SSEAlgorithm": "AES256"
                        }
                    }
                ]
            }'
        
        # Block public access
        aws s3api put-public-access-block \\
            --bucket "$bucket_name" \\
            --public-access-block-configuration \\
                BlockPublicAcls=true,\\
                IgnorePublicAcls=true,\\
                BlockPublicPolicy=true,\\
                RestrictPublicBuckets=true
        
        log_success "Configured bucket: $bucket_name"
    done
}

create_dynamodb_table() {
    log_info "Creating DynamoDB table for Terraform locks..."
    
    local table_name="terraform-locks"
    
    # Check if table already exists
    if aws dynamodb describe-table --table-name "$table_name" --region "$AWS_REGION" &>/dev/null; then
        log_warning "DynamoDB table $table_name already exists"
        return
    fi
    
    # Create table
    aws dynamodb create-table \\
        --table-name "$table_name" \\
        --attribute-definitions \\
            AttributeName=LockID,AttributeType=S \\
        --key-schema \\
            AttributeName=LockID,KeyType=HASH \\
        --billing-mode PAY_PER_REQUEST \\
        --region "$AWS_REGION" \\
        --tags \\
            Key=Project,Value="$PROJECT_NAME" \\
            Key=Purpose,Value="terraform-locks"
    
    log_info "Waiting for table to be active..."
    aws dynamodb wait table-exists --table-name "$table_name" --region "$AWS_REGION"
    
    log_success "Created DynamoDB table: $table_name"
}

create_ecr_repositories() {
    log_info "Creating ECR repositories for Docker images..."
    
    local repositories=("backend" "frontend")
    
    for repo in "${repositories[@]}"; do
        local repo_name="${PROJECT_NAME}-${repo}"
        
        log_info "Creating ECR repository: $repo_name"
        
        # Create repository
        if aws ecr create-repository \\
            --repository-name "$repo_name" \\
            --region "$AWS_REGION" \\
            --tags \\
                Key=Project,Value="$PROJECT_NAME" \\
                Key=Component,Value="$repo" \\
            &>/dev/null; then
            log_success "Created ECR repository: $repo_name"
        else
            log_warning "ECR repository $repo_name already exists or creation failed"
        fi
        
        # Set lifecycle policy
        aws ecr put-lifecycle-policy \\
            --repository-name "$repo_name" \\
            --region "$AWS_REGION" \\
            --lifecycle-policy-text '{
                "rules": [
                    {
                        "rulePriority": 1,
                        "description": "Keep last 10 images",
                        "selection": {
                            "tagStatus": "tagged",
                            "countType": "imageCountMoreThan",
                            "countNumber": 10
                        },
                        "action": {
                            "type": "expire"
                        }
                    }
                ]
            }' &>/dev/null
        
        log_success "Configured lifecycle policy for: $repo_name"
    done
}

update_terraform_backends() {
    log_info "Updating Terraform backend configurations..."
    
    local environments=("dev" "staging" "prod")
    
    for env in "${environments[@]}"; do
        local backend_file="terraform/environments/$env/backend.tf"
        local bucket_name="terraform-state-${PROJECT_NAME}-${env}"
        
        # Create backend.tf file
        cat > "$backend_file" << EOF
terraform {
  backend "s3" {
    bucket         = "$bucket_name"
    key            = "infrastructure/terraform.tfstate"
    region         = "$AWS_REGION"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
EOF
        
        log_success "Updated backend configuration for $env environment"
    done
}

show_completion_info() {
    log_success "Backend setup completed successfully!"
    echo ""
    echo "Created Resources:"
    echo "=================="
    echo "S3 Buckets:"
    echo "- terraform-state-${PROJECT_NAME}-dev"
    echo "- terraform-state-${PROJECT_NAME}-staging"
    echo "- terraform-state-${PROJECT_NAME}-prod"
    echo ""
    echo "DynamoDB Table:"
    echo "- terraform-locks"
    echo ""
    echo "ECR Repositories:"
    echo "- ${PROJECT_NAME}-backend"
    echo "- ${PROJECT_NAME}-frontend"
    echo ""
    echo "Next Steps:"
    echo "==========="
    echo "1. Configure your environment-specific variables in terraform/environments/*/terraform.tfvars"
    echo "2. Update Docker registry URLs in your deployment scripts"
    echo "3. Run: ./scripts/deploy.sh -e dev to deploy to development"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -r|--region)
            AWS_REGION="$2"
            shift 2
            ;;
        -p|--project)
            PROJECT_NAME="$2"
            shift 2
            ;;
        -h|--help)
            show_usage
            ;;
        *)
            log_error "Unknown option: $1"
            show_usage
            ;;
    esac
done

# Main execution
main() {
    log_info "Setting up Terraform backend for project: $PROJECT_NAME"
    log_info "Region: $AWS_REGION"
    
    check_aws_credentials
    create_s3_buckets
    create_dynamodb_table
    create_ecr_repositories
    update_terraform_backends
    show_completion_info
}

# Run main function
main "$@"
'''

# Docker Compose for local development
project_files["docker-compose.yml"] = '''version: '3.8'

services:
  # MySQL Database
  database:
    image: mysql:8.0
    container_name: threetier-database
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: webapp_dev
      MYSQL_USER: appuser
      MYSQL_PASSWORD: apppassword
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    networks:
      - threetier-network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      timeout: 10s
      retries: 5
      interval: 30s

  # Backend API
  backend:
    build:
      context: ./application/backend
      dockerfile: Dockerfile
    container_name: threetier-backend
    restart: unless-stopped
    environment:
      - NODE_ENV=development
      - PORT=3000
      - DB_HOST=database
      - DB_USER=appuser
      - DB_PASSWORD=apppassword
      - DB_NAME=webapp_dev
    ports:
      - "3000:3000"
    depends_on:
      database:
        condition: service_healthy
    volumes:
      - ./application/backend:/app
      - /app/node_modules
    networks:
      - threetier-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      timeout: 10s
      retries: 5
      interval: 30s

  # Frontend React App
  frontend:
    build:
      context: ./application/frontend
      dockerfile: Dockerfile.dev
    container_name: threetier-frontend
    restart: unless-stopped
    environment:
      - REACT_APP_API_URL=http://localhost:3000
      - CHOKIDAR_USEPOLLING=true
    ports:
      - "80:3000"
    depends_on:
      backend:
        condition: service_healthy
    volumes:
      - ./application/frontend:/app
      - /app/node_modules
    networks:
      - threetier-network

  # NGINX Load Balancer (optional)
  nginx:
    image: nginx:alpine
    container_name: threetier-nginx
    restart: unless-stopped
    ports:
      - "8080:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - frontend
      - backend
    networks:
      - threetier-network

volumes:
  mysql_data:
    driver: local

networks:
  threetier-network:
    driver: bridge
'''

# Development Dockerfile for frontend
project_files["application/frontend/Dockerfile.dev"] = '''FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Start development server
CMD ["npm", "start"]
'''

# Database initialization script
project_files["scripts/init.sql"] = '''-- Database initialization script
CREATE DATABASE IF NOT EXISTS webapp_dev;
USE webapp_dev;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_created_at (created_at)
);

-- Insert sample data
INSERT INTO users (name, email) VALUES
('John Doe', 'john.doe@example.com'),
('Jane Smith', 'jane.smith@example.com'),
('Bob Johnson', 'bob.johnson@example.com'),
('Alice Brown', 'alice.brown@example.com'),
('Charlie Wilson', 'charlie.wilson@example.com')
ON DUPLICATE KEY UPDATE
name = VALUES(name);

-- Create database user for application
CREATE USER IF NOT EXISTS 'appuser'@'%' IDENTIFIED BY 'apppassword';
GRANT SELECT, INSERT, UPDATE, DELETE ON webapp_dev.* TO 'appuser'@'%';
FLUSH PRIVILEGES;
'''

# Makefile for common tasks
project_files["Makefile"] = '''.PHONY: help install build test lint clean deploy destroy logs

# Default target
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\\033[36m%-20s\\033[0m %s\\n", $$1, $$2}'

# Local Development
install: ## Install dependencies for all components
	@echo "Installing backend dependencies..."
	cd application/backend && npm install
	@echo "Installing frontend dependencies..."
	cd application/frontend && npm install

build: ## Build Docker images locally
	@echo "Building Docker images..."
	docker-compose build

up: ## Start all services with Docker Compose
	@echo "Starting services..."
	docker-compose up -d

down: ## Stop all services
	@echo "Stopping services..."
	docker-compose down

logs: ## View logs from all services
	docker-compose logs -f

logs-backend: ## View backend logs
	docker-compose logs -f backend

logs-frontend: ## View frontend logs
	docker-compose logs -f frontend

logs-db: ## View database logs
	docker-compose logs -f database

# Testing
test: ## Run tests for all components
	@echo "Running backend tests..."
	cd application/backend && npm test
	@echo "Running frontend tests..."
	cd application/frontend && npm test

lint: ## Run linting for all components
	@echo "Linting backend..."
	cd application/backend && npm run lint
	@echo "Linting frontend..."
	cd application/frontend && npm run lint

lint-fix: ## Fix linting issues
	@echo "Fixing backend linting issues..."
	cd application/backend && npm run lint:fix
	@echo "Fixing frontend linting issues..."
	cd application/frontend && npm run lint:fix

# Infrastructure
setup-backend: ## Setup Terraform backend infrastructure
	./scripts/setup-backend.sh

deploy-dev: ## Deploy to development environment
	./scripts/deploy.sh -e dev

deploy-staging: ## Deploy to staging environment
	./scripts/deploy.sh -e staging

deploy-prod: ## Deploy to production environment
	./scripts/deploy.sh -e prod

# Terraform commands
tf-init-dev: ## Initialize Terraform for dev environment
	cd terraform/environments/dev && terraform init

tf-plan-dev: ## Plan Terraform changes for dev environment
	cd terraform/environments/dev && terraform plan

tf-apply-dev: ## Apply Terraform changes for dev environment
	cd terraform/environments/dev && terraform apply

tf-destroy-dev: ## Destroy dev environment
	cd terraform/environments/dev && terraform destroy

# Cleanup
clean: ## Clean up local environment
	docker-compose down -v
	docker system prune -f
	rm -f outputs.json

clean-all: ## Clean up everything including images
	docker-compose down -v --rmi all
	docker system prune -af
	rm -f outputs.json

# Database
db-migrate: ## Run database migrations (placeholder)
	@echo "Database migrations would go here"

db-seed: ## Seed database with sample data
	docker-compose exec database mysql -u root -prootpassword webapp_dev < scripts/init.sql

db-shell: ## Connect to database shell
	docker-compose exec database mysql -u appuser -papppassword webapp_dev

# Monitoring
health-check: ## Check health of all services
	@echo "Checking service health..."
	@curl -f http://localhost:3000/health || echo "Backend unhealthy"
	@curl -f http://localhost:80/ || echo "Frontend unhealthy"

# Documentation
docs: ## Generate documentation (placeholder)
	@echo "Documentation generation would go here"
'''

print("Created deployment scripts and configuration files")
print(f"Total files so far: {len(project_files)}")