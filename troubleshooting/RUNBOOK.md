# PodiumHQ Troubleshooting Lab & Remediation Runbook

This guide covers diagnosis and remediation for 4 real-world Kubernetes failure scenarios.

---

## Scenario 1: ImagePullBackOff / ErrImagePull
* **Symptom**: Pod fails to start; `kubectl get pods` shows `ImagePullBackOff`.
* **Root Cause**: Non-existent tag specified in deployment (`ghcr.io/...:nonexistent-tag-999`).
* **Diagnosis Command**:
  ```bash
  kubectl describe pod -l app=broken-image -n podiumhq
  ```
  Look for `Failed to pull image ...: manifest unknown`.
* **Remediation**:
  Update image tag in Helm `values.yaml` to valid Git commit SHA and run:
  ```bash
  helm upgrade podiumhq ./helm/podiumhq -n podiumhq
  ```

---

## Scenario 2: Service Selector Mismatch (502 / Connection Refused)
* **Symptom**: Requests to Service fail with `502 Bad Gateway`.
* **Root Cause**: Service selector does not match pod labels.
* **Diagnosis Command**:
  ```bash
  kubectl get endpoints broken-service-demo -n podiumhq
  ```
  Output shows `<none>` under ENDPOINTS.
* **Remediation**:
  Align Service `.spec.selector` with Pod template `.metadata.labels`.

---

## Scenario 3: Readiness Probe Failure (Pod Never Becomes Ready)
* **Symptom**: Pod stays at `0/1 READY` and never receives ingress traffic.
* **Root Cause**: Readiness probe pointing to non-existent endpoint `/nonexistent-probe-endpoint`.
* **Diagnosis Command**:
  ```bash
  kubectl describe pod -l app=broken-probe -n podiumhq
  ```
  Look for `Readiness probe failed: HTTP probe failed with statuscode: 404`.
* **Remediation**:
  Update readiness probe path in deployment manifest to valid `/ready` endpoint.

---

## Scenario 4: Missing Secret (CreateContainerConfigError)
* **Symptom**: Pod status is `CreateContainerConfigError`.
* **Root Cause**: Pod references `non-existent-db-secret` which does not exist in the namespace.
* **Diagnosis Command**:
  ```bash
  kubectl describe pod -l app=broken-secret -n podiumhq
  ```
  Look for `Error: secret "non-existent-db-secret" not found`.
* **Remediation**:
  Create the missing secret using `scripts/bootstrap-secrets.sh`.
