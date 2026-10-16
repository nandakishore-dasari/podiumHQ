## Summary of Changes
- Briefly describe the purpose and scope of this pull request.

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Security / Hardening improvement
- [ ] CI/CD or Infrastructure as Code update
- [ ] Documentation update

## DevSecOps & Quality Assurance Checklist
- [ ] Local tests executed and passing with $\ge 80\%$ code coverage (`pytest tests/ -v --cov=app`)
- [ ] Security linter and static analysis clean (`ruff check .`)
- [ ] Container security verified (non-root UID, dropped Linux capabilities)
- [ ] Trivy vulnerability scan passes without CRITICAL CVEs
- [ ] Helm chart linted successfully (`helm lint helm/podiumhq`)
- [ ] No hardcoded secrets, API keys, or plaintext credentials committed
