# Self-Healing E-Commerce Platform

A production-grade microservices application with self-healing 
infrastructure on AWS EKS.

## Demo Video

<p align="center">
  <a href="https://vimeo.com/1195453321?share=copy">
    <img 
      src="click.png"
      width="580"
      alt="Project Demo"
      style="border-radius:16px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);"
    />
  </a>
</p>

## Architecture Diagram
<p align="center">
    <img src="self-healing-project-architecture.png" width="700" alt="self-healing-project-architecture.png"/>
  </a>
</p>



## Tech Stack

- **Python + FastAPI** — microservices framework
- **Docker + Docker Compose** — containerization
- **Terraform** — provisions AWS infrastructure as code
- **AWS EKS** — managed Kubernetes cluster
- **AWS ECR** — private Docker image registry
- **AWS VPC** — private network with public/private subnets across 2 availability zones
- **Helm** — Kubernetes package manager for deployments
- **GitHub Actions** — CI/CD pipeline, auto-deploys on every push to main
- **Prometheus + Grafana** — live monitoring and metrics dashboard
- **Ansible** — bastion host configuration management

## Self-Healing Demo

This platform demonstrates Kubernetes self-healing in real time.

1. All 3 services run with 2 replicas each across 2 availability zones
2. A pod is deliberately deleted using `kubectl delete pod <pod-name>`
3. Kubernetes detects the missing pod within seconds
4. A replacement pod is automatically created and reaches Running status in under 30 seconds
5. The service never goes down — the second replica handles traffic while the replacement starts
6. The entire recovery is visible live on the Grafana dashboard

## 💡 The Problem It Solves

Traditional deployments fail and stay down until an engineer 
manually notices, diagnoses, and fixes the issue. That could 
take minutes or hours depending on the time of day.

This platform solves that by running every service with multiple 
replicas across two AWS availability zones. When a pod crashes, 
Kubernetes detects it within seconds and automatically schedules 
a replacement — no human intervention, no downtime, no 3am 
phone calls. Recovery happens in under 30 seconds, verified 
live on a Grafana dashboard.

---

## 🚀 How to Run It

**Prerequisites:** AWS account, Terraform, kubectl, Helm, 
Docker, AWS CLI installed and configured.

**Step 1 — Clone the repo**
```bash
git clone https://github.com/Akioye/ecommerce-platform
cd ecommerce-platform
```

**Step 2 — Configure AWS credentials**
```bash
aws configure
# Enter your Access Key ID, Secret Access Key, region: us-east-1
```

**Step 3 — Provision infrastructure**
```bash
cd terraform
terraform init
terraform apply
```
This creates your VPC, EKS cluster, ECR repositories, 
NAT Gateway, and bastion host. Takes 15-20 minutes.

**Step 4 — Connect to the cluster**
```bash
aws eks update-kubeconfig --region us-east-1 --name ecommerce-cluster
kubectl get nodes  # verify 2 nodes are Ready
```

**Step 5 — Push Docker images to ECR**
```bash
aws ecr get-login-password --region us-east-1 | docker login \
  --username AWS --password-stdin \
  524178179037.dkr.ecr.us-east-1.amazonaws.com

docker build -t 524178179037.dkr.ecr.us-east-1.amazonaws.com/inventory-service:latest ./inventory-service
docker push 524178179037.dkr.ecr.us-east-1.amazonaws.com/inventory-service:latest

docker build -t 524178179037.dkr.ecr.us-east-1.amazonaws.com/cart-service:latest ./cart-service
docker push 524178179037.dkr.ecr.us-east-1.amazonaws.com/cart-service:latest

docker build -t 524178179037.dkr.ecr.us-east-1.amazonaws.com/payment-service:latest ./payment-service
docker push 524178179037.dkr.ecr.us-east-1.amazonaws.com/payment-service:latest
```

**Step 6 — Deploy services with Helm**
```bash
cd ..
helm upgrade --install ecommerce ./helm/ecommerce
kubectl get pods  # all 6 pods should show Running
```

**Step 7 — Install monitoring**
```bash
helm repo add prometheus-community \
  https://prometheus-community.github.io/helm-charts
helm repo update
helm install monitoring \
  prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace
```

**Step 8 — Access Grafana dashboard**
```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
# Open http://localhost:3000
# Username: admin
# Get password: kubectl get secret --namespace monitoring \
#   monitoring-grafana -o jsonpath="{.data.admin-password}" | base64 --decode
```

**Destroy when done — stops all AWS billing**
```bash
cd terraform
terraform destroy
```

---

## 📊 Results

| Metric | Result |
|---|---|
| Pod recovery time | Under 30 seconds |
| Zero downtime deployments | ✅ Verified |
| Services across availability zones | 2 (us-east-1a, us-east-1b) |
| Replicas per service | 2 |
| CI/CD pipeline execution time | Under 60 seconds |
| Infrastructure provisioned as code | 20 AWS resources via Terraform |

---

## 💰 AWS Cost Estimate

| Resource | Cost |
|---|---|
| EKS Control Plane | $0.10/hour |
| 2x t3.small EC2 nodes | ~$0.04/hour |
| NAT Gateway | ~$0.05/hour |
| Bastion host (t3.micro) | ~$0.01/hour |
| **Total** | **~$0.20/hour (~$4.80/day)** |

Always destroy infrastructure when not in use:
```bash
terraform destroy
```

---

## 🧠 What I Learned

**Kubernetes self-healing isn't magic.** It's a control loop. 
The deployment controller constantly compares the desired 
state (2 replicas) against the actual state. When they 
don't match, it acts immediately. Understanding this loop 
changed how I think about distributed systems.

**Infrastructure as code changes how you think about cloud.** 
Writing Terraform taught me that every AWS resource has 
dependencies, a NAT Gateway needs an Elastic IP, private 
subnets need route tables, EKS nodes need specific IAM 
policies. Missing one breaks everything. I learned this 
the hard way when nodes failed to join the cluster because 
I had no NAT Gateway.

**Helm charts are Kubernetes templates, not magic.** 
Writing them from scratch showed me exactly what 
Kubernetes needs to run a service, a Deployment to 
manage pods and a Service to give them a stable network 
address. Once I understood that, the templating made 
complete sense.

**Prometheus and Grafana are separate concerns.** 
Prometheus collects and stores metrics. Grafana just 
reads from Prometheus and draws charts. Understanding 
the separation helped me debug why dashboards weren't 
showing data, it was a Prometheus scraping issue, 
not a Grafana issue.

**Debugging distributed systems requires different thinking.** 
When something broke, the error was rarely where I 
was looking. A pod failing to start was actually an 
ECR authentication issue. Nodes not joining the cluster 
was a missing NAT Gateway. I learned to trace problems 
upstream rather than fixing symptoms.

## Screenshots

### Grafana Live Monitoring
<p align="center">
    <img src="screenshots/grafana-inventory.png" width="700" alt="grafana-inventory.png"/>
  </a>
</p>

<p align="center">
    <img src="screenshots/grafana-cart.png" width="700" alt="grafana-cart.png"/>
  </a>
</p>

<p align="center">
    <img src="screenshots/grafana-payment.png" width="700" alt="grafana-payment.png"/>
  </a>
</p>


### Chaos Engineering — Pod Self-Healing
<p align="center">
    <img src="screenshots/grafana-chaos-engineering.png" width="700" alt="grafana-chaos-engineering.png"/>
  </a>
</p>


### GitHub Actions CI/CD Pipeline
<p align="center">
    <img src="screenshots/github-actions-pipeline.png" width="700" alt="github-actions-pipeline.png"/>
  </a>
</p>

