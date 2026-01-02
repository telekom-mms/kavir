# Kubernetes Application Version Report (prod)

| [dev](https://github.com/telekom-mms/kavir/blob/main/html-report-builder/examples/dev.md) | *[prod](https://github.com/telekom-mms/kavir/blob/main/html-report-builder/examples/prod.md)* |

## deployments

| Name  | Image | Tag/Version |
| ---  | --- | --- |
| cmcc-operator | ghcr.io/telekom-mms/cmcc-operator/cmcc-operator<br /> | v1.14.15<br /> |
| gitea | docker.io/gitea/gitea<br /> | latest-rootless<br /> |
| my-deployment | container-registry.acme.de/deployments/my-deployment<br /> | 1.0.0<br /> |
| trivy-dojo-operator | ghcr.io/telekom-mms/docker-trivy-dojo-operator<br /> | 0.7.2<br /> |

## replicasets

not in scope of the report

## statefulsets

in scope of the report; but there are no statefulsets to report about

## daemonsets

not in scope of the report

## jobs

not in scope of the report

## cronjobs

| Name  | Image | Tag/Version |
| ---  | --- | --- |
| kavir | ghcr.io/telekom-mms/kavir<br /> | 1.2.0<br /> |
| my-cronjob | container-registry.acme.de/cronjobs/my-cronjob<br /> | 1.0.0<br /> |

## replicationcontrollers

not in scope of the report
