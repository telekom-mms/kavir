# Kubernetes Application Version Report (dev)

| *[dev](https://github.com/telekom-mms/kavir/blob/main/html-report-builder/examples/dev.md)* | [prod](https://github.com/telekom-mms/kavir/blob/main/html-report-builder/examples/prod.md) |

## deployments

| Name  | Namespace | Image | Tag/Version |
| ---  | --- | --- | --- |
| cmcc-operator | app | ghcr.io/telekom-mms/cmcc-operator/cmcc-operator<br /> | v1.14.15<br /> |
| gitea | gitea | docker.io/bitnami/gitea<br /> | 1.22.3-debian-12-r0<br /> |
| my-deployment | app | container-registry.acme.de/deployments/my-deployment<br /> | 0.4.2<br /> |
| trivy-dojo-operator | monitoring | ghcr.io/telekom-mms/docker-trivy-dojo-operator<br /> | 0.7.2<br /> |

## replicasets

not in scope of the report

## statefulsets

in scope of the report; but there are no statefulsets to report about

## daemonsets

not in scope of the report

## jobs

not in scope of the report

## cronjobs

| Name  | Namespace | Image | Tag/Version |
| ---  | --- | --- | --- |
| kavir | monitoring | ghcr.io/telekom-mms/kavir<br /> | 1.0.1<br /> |
| my-cronjob | app | container-registry.acme.de/cronjobs/my-cronjob<br /> | 1.0.0<br /> |

## replicationcontrollers

not in scope of the report
