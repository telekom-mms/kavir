# kavir - **K**ubernetes **A**pplication **V**ers**I**on **R**eporter - docker

The container uses the `kavir.bash` script to gather information via `kubectl` and commits them as csv files to the predefined git repository.

## environment variables

The container requires several environment variables. Since kavir is meant to be run inside a kubernetes cluster it is recommended to use the helm chart to deploy kavir. The `values.yaml` of the helm chart contains all environment variables. Look inside the `charts/kavir/` folder for further explanations.

| variable                     | description                                                                                   |
| ---------------------------- | --------------------------------------------------------------------------------------------- |
| clusterName                  | the name of the folder in the git repository which contains all the csv files for the cluster |
| gitRepoUrl                   | the git repository url kavir forwards the information to                                      |
| gitProjectAccessToken        | the git project access token kavir uses to access the git repository (role: Maintainer, scopes: write_repository) |
| gitUserName                  | the username that is shown for the commits made by kavir                                      |
| gitUserEmail                 | the email that is shown for the commits made by kavir                                         |
| reportNamespaces             | determines whether kavir includes namespaces in the csv reports                               |
| reportDeployments            | determines whether kavir gathers information on deployments                                   |
| reportReplicasets            | determines whether kavir gathers information on replicasets                                   |
| reportStatefulsets           | determines whether kavir gathers information on statefulsets                                  |
| reportDaemonsets             | determines whether kavir gathers information on daemonsets                                    |
| reportJobs                   | determines whether kavir gathers information on jobs                                          |
| reportCronjobs               | determines whether kavir gathers information on cronjobs                                      |
| reportReplicationcontrollers | determines whether kavir gathers information on replicationcontrollers                        |

## releases

Check the [Packages](https://github.com/orgs/telekom-mms/packages?repo_name=kavir) of this repository to view the releases of the container.

## git repository preview

kavir creates the following structure in the git repository specified by `repoUrl`. Check out the `examples` folder for an example.

```text
├── dev
│   ├── cronjobs.csv
│   ├── daemonsets.csv
│   ├── deployments.csv
│   ├── jobs.csv
│   ├── replicasets.csv
│   ├── replicationcontrollers.csv
│   ├── statefulsets.csv
├── prod
│   ├── cronjobs.csv
│   ├── daemonsets.csv
│   ├── deployments.csv
│   ├── jobs.csv
│   ├── replicasets.csv
│   ├── replicationcontrollers.csv
│   ├── statefulsets.csv
```

A `cronjobs.csv` could look like this:

```csv
Name,Image:Tag
kavir,ghcr.io/telekom-mms/kavir:1.2.0
my-cronjob,container-registry.acme.de/cronjobs/my-cronjob:1.0.0
```

If `reportNamespaces` is set to `true`, the `cronjobs.csv` will look like this:

```csv
Name,Namespace,Image:Tag
kavir,monitoring,ghcr.io/telekom-mms/kavir:1.2.0
my-cronjob,app,container-registry.acme.de/cronjobs/my-cronjob:1.0.0
```

If cronjobs are in the scope of the report (`reportCronjobs=true`) but there are no cronjobs to report about, the `cronjobs.csv` will look like this:

```csv
Name,Image:Tag
```

If cronjobs are not in the scope of the report (`reportCronjobs=false`), the `cronjobs.csv` will look like this:

```csv
out of scope
```

In addition you may check if your git hosting service supports the rendering of csv files. This way you can have a look at the csv files ready rendered without further ado.

* [GitHub csv rendering](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files#rendering-csv-and-tsv-data)
* [GitLab csv rendering](https://docs.gitlab.com/ee/user/project/repository/files/csv.html)
