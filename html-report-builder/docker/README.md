# kavir - **K**ubernetes **A**pplication **V**ers**I**on **R**eporter - html-report-builder/docker

The container

* builds the `config.json` for kavirs html-report-builder based on environment variables
* executes kavirs html-report-builder

## optional environment variables

| variable          | equivalent in kavirs html-report-builder `config.json` | default value                                                                          |
| ----------------- | ------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| verbose           |                                                        | `true`                                                                                 |
| reportName        | report.name                                            | `Kubernetes Application Version Report`                                                |
| reportScope       | report.scope                                           | `deployments replicasets statefulsets daemonsets jobs cronjobs replicationcontrollers` |
| pathsTemplateFile | paths.templateFile                                     | `/etc/kavir-html-report-builder/templates/simple.html.j2`                              |
| pathsStyleFile    | paths.styleFile                                        | `/etc/kavir-html-report-builder/styles/tech.css`                                       |
| menuEnabled       | menu.enabled                                           | `true`                                                                                 |

## mandatory environment variables

| variable          | equivalent in kavirs html-report-builder `config.json` |
| ----------------- | ------------------------------------------------------ |
| pathsSrcDir       | paths.srcDir                                           |
| pathsOutDir       | paths.outDir                                           |
| menuLinkBasePath* | menu.linkBasePath                                      |

\* menuLinkBasePath is mandatory if menuEnabled == "true"

## Usage

```bash
cd ./docker/examples
docker run \
-v /absolute/path/to/kavir/docker/examples:/tmp/kavir/in \
-v /var/www/kavir:/tmp/kavir/out \
-e pathsSrcDir="/tmp/kavir/in" \
-e pathsOutDir="/tmp/kavir/out" \
-e menuLinkBasePath="https://kavir.acme.de" \
ghcr.io/telekom-mms/kavir-html-report-builder:1.1.0
```

## releases

Check the [packages](https://github.com/orgs/telekom-mms/packages?repo_name=kavir) of this repository to view the releases of the container.
