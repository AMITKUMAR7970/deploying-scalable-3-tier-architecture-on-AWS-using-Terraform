import plotly.graph_objects as go

# Data from the provided JSON
files_by_category = [
    {"category": "Application - Frontend", "count": 7},
    {"category": "Root", "count": 5},
    {"category": "Terraform Environment - Dev", "count": 4},
    {"category": "Terraform Environment - Staging", "count": 4},
    {"category": "Terraform Environment - Prod", "count": 4},
    {"category": "Scripts", "count": 3},
    {"category": "Application - Backend", "count": 3},
    {"category": "Terraform Module - Monitoring", "count": 3},
    {"category": "Terraform Module - Rds", "count": 3},
    {"category": "Terraform Module - Alb", "count": 3},
    {"category": "Terraform Module - Ecs", "count": 3},
    {"category": "Terraform Module - Security", "count": 3},
    {"category": "Terraform Module - Vpc", "count": 3},
    {"category": "Documentation", "count": 2},
    {"category": "CI/CD", "count": 2}
]

# Extract and abbreviate category names to fit 15-character limit
categories = []
counts = []
category_mapping = {
    "Application - Frontend": "App Frontend",
    "Root": "Root",
    "Terraform Environment - Dev": "TF Env Dev",
    "Terraform Environment - Staging": "TF Env Stage", 
    "Terraform Environment - Prod": "TF Env Prod",
    "Scripts": "Scripts",
    "Application - Backend": "App Backend",
    "Terraform Module - Monitoring": "TF Mod Monitor",
    "Terraform Module - Rds": "TF Mod RDS",
    "Terraform Module - Alb": "TF Mod ALB",
    "Terraform Module - Ecs": "TF Mod ECS",
    "Terraform Module - Security": "TF Mod Security",
    "Terraform Module - Vpc": "TF Mod VPC",
    "Documentation": "Documentation",
    "CI/CD": "CI/CD"
}

for item in files_by_category:
    categories.append(category_mapping[item["category"]])
    counts.append(item["count"])

# Sort by count descending for better visualization
sorted_data = sorted(zip(categories, counts), key=lambda x: x[1], reverse=True)
categories, counts = zip(*sorted_data)

# Use brand colors alternating through the primary colors
colors = ["#1FB8CD", "#DB4545", "#2E8B57", "#5D878F", "#D2BA4C"] * 3

# Create horizontal bar chart
fig = go.Figure(data=go.Bar(
    y=categories,
    x=counts,
    orientation='h',
    marker=dict(color=colors[:len(categories)]),
    text=counts,
    textposition='outside',
    cliponaxis=False,
    hovertemplate='<b>%{y}</b><br>Files: %{x}<extra></extra>'
))

# Update layout
fig.update_layout(
    title="DevOps Project File Distribution",
    xaxis_title="File Count",
    yaxis_title="Category"
)

# Save the chart
fig.write_image("devops_files_chart.png")