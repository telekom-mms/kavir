# kavir - **K**ubernetes **A**pplication **V**ers**I**on **R**eporter - html-report-builder/docker

The container

* builds the `config.json` for kavirs html-report-builder based on environment variables
* executes kavirs html-report-builder

## optional environment variables

| variable           | equivalent in kavirs html-report-builder `config.json` | default value                                                                          |
| ------------------ | ------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| verbose            |                                                        | `true`                                                                                 |
| report_name        | report.name                                            | `Kubernetes Application Version Report`                                                |
| report_scope       | report.scope                                           | `deployments replicasets statefulsets daemonsets jobs cronjobs replicationcontrollers` |
| paths_templateFile | paths.templateFile                                     | `/etc/kavir/html-report-builder/templates/simple.html.j2`                              |
| paths_styleFile    | paths.styleFile                                        | `/etc/kavir/html-report-builder/styles/simple.css`                                     |
| menu_enabled       | menu.enabled                                           | `true`                                                                                 |

## mandatory environment variables

| variable           | equivalent in kavirs html-report-builder `config.json` |
| ------------------ | ------------------------------------------------------ |
| paths_srcDir       | paths.srcDir                                           |
| paths_outDir       | paths.outDir                                           |
| menu_linkBasePath* | menu.linkBasePath                                      |

\* menu_linkBasePath is mandatory if menu_enabled == "true"

## Usage

```bash
cd ./docker/examples
docker run \
-v /absolute/path/to/kavir/docker/examples:/tmp/kavir/in \
-v /var/www/kavir:/tmp/kavir/out \
-e paths_srcDir="/tmp/kavir/in" \
-e paths_outDir="/tmp/kavir/out" \
-e menu_linkBasePath="https://kavir.acme.de" \
ghcr.io/telekom-mms/kavir-html-report-builder:1.0.0
```

## releases

Check the packages of this repository to view the releases of the container.
