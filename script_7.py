# Fix the function definition order and create the CSV

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

print(f"📊 Project Statistics:")
print(f"Total Files: {total_files}")
print(f"Total Characters: {total_size:,}")
print(f"Total Lines of Code: {total_lines:,}")
print(f"\nFiles by Category:")
category_counts = df['Category'].value_counts()
for category, count in category_counts.items():
    print(f"  {category}: {count} files")

print(f"\n✅ Complete project saved to: {csv_filename}")

# Display sample of the CSV content
print(f"\n📋 Sample of project files:")
print(df[['File Path', 'Category', 'Description']].head(10).to_string(index=False))

print(f"\n🚀 Project Features:")
features = [
    "✅ Complete 3-tier architecture (React, Node.js, MySQL)",
    "✅ Full Terraform infrastructure as code",
    "✅ Multi-environment support (dev, staging, prod)",
    "✅ CI/CD pipelines with GitHub Actions",
    "✅ Docker containerization",
    "✅ Auto-scaling and load balancing",
    "✅ Database with Multi-AZ and backups",
    "✅ Comprehensive monitoring and alerting",
    "✅ Security best practices",
    "✅ Local development environment",
    "✅ Automated deployment scripts",
    "✅ Complete documentation"
]

for feature in features:
    print(feature)

print(f"\n📁 Project Structure Overview:")
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

print(f"\n🎯 Ready for deployment! Use the interactive web app above to explore all files and configurations.")
print(f"\n📄 Access the CSV file for complete project reference: {csv_filename}")