# ArgoCD Installation and GitOps Demo Guide

## 1. Install ArgoCD on the EKS Cluster
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

## 2. Access ArgoCD Web UI
```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```
* URL: `https://localhost:8080`
* Username: `admin`
* Initial Password:
  ```bash
  kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
  ```

## 3. Deploy the PodiumHQ GitOps Application
```bash
kubectl apply -f argocd/application.yaml
```

## 4. Demonstrate Drift Healing (Viva Demo)
To demonstrate self-healing in real time:
1. Manually scale backend deployment:
   ```bash
   kubectl scale deployment podiumhq-backend -n podiumhq --replicas=5
   ```
2. Watch ArgoCD detect the drift (`OutOfSync`) and automatically reconcile it back to the Helm specification (`selfHeal: true`).
