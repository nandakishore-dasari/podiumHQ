# Terraform AWS VPC + EKS Provisioning & Teardown Runbook

This directory contains modular Terraform configuration to provision an AWS VPC and an EKS cluster for PodiumHQ.

## Cost Warning & Clean Teardown Guarantee
Running an EKS cluster with NAT Gateways on AWS costs ~$0.15/hour. To guarantee zero unwanted charges after evaluation, follow the **Teardown Runbook** below immediately after demoing.

---

## 🚀 Provisioning Steps

1. Configure AWS credentials:
   ```bash
   aws configure
   ```
2. Initialize Terraform:
   ```bash
   terraform init
   ```
3. Copy variables template:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```
4. Review execution plan:
   ```bash
   terraform plan -out=tfplan
   ```
5. Apply infrastructure:
   ```bash
   terraform apply tfplan
   ```
6. Connect `kubectl` to your new cluster:
   ```bash
   aws eks --region ap-south-1 update-kubeconfig --name podiumhq-eks
   kubectl get nodes
   ```

---

## 🛑 Teardown Runbook (`terraform destroy`)

To completely wipe all cloud resources and stop billing:

1. **Delete any in-cluster LoadBalancers and PVCs first** (so AWS ALB and EBS volumes don't block VPC deletion):
   ```bash
   helm uninstall podiumhq -n podiumhq || true
   kubectl delete pvc --all -n podiumhq || true
   ```

2. **Execute Terraform Destroy**:
   ```bash
   terraform destroy -auto-approve
   ```

3. **Verify AWS Console**:
   * EKS Clusters: Ensure `podiumhq-eks` is deleted.
   * EC2 Instances & NAT Gateways: Verify terminated.
   * VPC: Ensure `podiumhq-vpc` is deleted.
