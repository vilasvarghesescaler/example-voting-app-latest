# GitHub Actions Secrets Reference

All values below must be configured in **Settings → Secrets and variables → Actions** in your repository (or at org level).

---

## Registry

| Secret | Description | Example |
|--------|-------------|---------|
| `DOCKER_REGISTRY` | Container registry hostname | `registry.example.com` or `docker.io` |
| `DOCKER_REPO` | Repository/org prefix | `myorg` or `myteam` |
| `DOCKER_USERNAME` | Registry login username | `ci-bot` |
| `DOCKER_PASSWORD` | Registry login password / token | (token value) |

> **ECR users**: Replace `DOCKER_USERNAME`/`DOCKER_PASSWORD` with `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY`, then swap the login action for `aws-actions/amazon-ecr-login`.

---

## AWS / EKS

| Secret | Description | Example |
|--------|-------------|---------|
| `AWS_REGION` | AWS region | `us-east-1` |
| `AWS_ACCESS_KEY_ID` | IAM access key ID | `AKIA...` |
| `AWS_SECRET_ACCESS_KEY` | IAM secret access key | (key value) |
| `AWS_DEPLOY_ROLE_ARN` | IAM role ARN to assume for deploy | `arn:aws:iam::123456789012:role/GitHubDeployRole` |
| `EKS_CLUSTER_NAME` | EKS cluster name | `voting-app-prod` |
| `KUBE_NAMESPACE_STAGING` | K8s namespace for staging | `voting-staging` |
| `KUBE_NAMESPACE_PRODUCTION` | K8s namespace for production | `voting-production` |

---

## Helm

| Secret | Description | Example |
|--------|-------------|---------|
| `HELM_RELEASE_NAME` | Helm release name prefix | `voting-app` |
| `HELM_CHART_PATH` | Path to Helm charts in repo | `k8s/helm` |

---

## Application — Vote Service

| Secret | Description | Example |
|--------|-------------|---------|
| `VOTE_REPLICA_COUNT` | Number of pods | `2` |
| `VOTE_CPU_REQUEST` | CPU request | `100m` |
| `VOTE_CPU_LIMIT` | CPU limit | `500m` |
| `VOTE_MEM_REQUEST` | Memory request | `128Mi` |
| `VOTE_MEM_LIMIT` | Memory limit | `256Mi` |
| `VOTE_INGRESS_HOST` | Ingress hostname | `vote.example.com` |
| `VOTE_TLS_SECRET` | TLS secret name in K8s | `vote-tls` |

---

## Application — Result Service

| Secret | Description | Example |
|--------|-------------|---------|
| `RESULT_REPLICA_COUNT` | Number of pods | `2` |
| `RESULT_CPU_REQUEST` | CPU request | `100m` |
| `RESULT_CPU_LIMIT` | CPU limit | `500m` |
| `RESULT_MEM_REQUEST` | Memory request | `128Mi` |
| `RESULT_MEM_LIMIT` | Memory limit | `256Mi` |
| `RESULT_INGRESS_HOST` | Ingress hostname | `result.example.com` |
| `RESULT_TLS_SECRET` | TLS secret name in K8s | `result-tls` |

---

## Application — Worker Service

| Secret | Description | Example |
|--------|-------------|---------|
| `WORKER_REPLICA_COUNT` | Number of pods | `1` |
| `WORKER_CPU_REQUEST` | CPU request | `100m` |
| `WORKER_CPU_LIMIT` | CPU limit | `500m` |
| `WORKER_MEM_REQUEST` | Memory request | `128Mi` |
| `WORKER_MEM_LIMIT` | Memory limit | `256Mi` |

---

## Shared Infrastructure

| Secret | Description | Example |
|--------|-------------|---------|
| `REDIS_HOST` | Redis hostname | `redis.voting-staging.svc.cluster.local` |
| `REDIS_PORT` | Redis port | `6379` |
| `DB_HOST` | PostgreSQL hostname | `postgres.voting-staging.svc.cluster.local` |
| `DB_PORT` | PostgreSQL port | `5432` |
| `DB_NAME` | Database name | `votes` |
| `DB_USER` | Database user | `votes_user` |
| `DB_PASSWORD` | Database password | (password value) |

---

## Integrations

| Secret | Description | Required |
|--------|-------------|----------|
| `CODECOV_TOKEN` | Codecov upload token | Optional |
| `SNYK_TOKEN` | Snyk API token for SCA | Optional |
| `CD_DISPATCH_TOKEN` | GitHub PAT with `repo` scope for cross-workflow dispatch | Required for CD trigger |
| `SLACK_WEBHOOK_URL` | Slack Incoming Webhook URL | Optional |

---

## GitHub Environments

Configure two **Environments** in Settings → Environments:

| Environment | Protection Rules |
|-------------|-----------------|
| `staging` | None (auto-deploy) |
| `production` | Required reviewers (≥1), prevent self-review |

---

## IAM Policy for GitHub Actions Deploy Role

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "eks:DescribeCluster",
        "eks:ListClusters"
      ],
      "Resource": "arn:aws:eks:REGION:ACCOUNT_ID:cluster/CLUSTER_NAME"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:PutImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload"
      ],
      "Resource": "*"
    }
  ]
}
```

The trust policy should allow `token.actions.githubusercontent.com` as the federated identity provider (OIDC recommended over long-lived keys).
