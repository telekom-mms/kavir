# kavir - **K**ubernetes **A**pplication **V**ers**I**on **R**eporter - docker

The container is based on [bitnamis kubectl container](https://github.com/bitnami/containers/tree/main/bitnami/kubectl) published under the [Apache2 License](https://www.apache.org/licenses/LICENSE-2.0). It uses a bash file which gathers information via `kubectl` and commits them as csv files to the predefined git repository.

The container requires several environment variables. The `values.yaml` of the helm chart containes all environment variables, therefore it is recommended to use the helm chart to deploy kavir. Look inside the `helm` folder for further explanations.

## environment variables

| variable                     | description                                                                                   |
| ---------------------------- | --------------------------------------------------------------------------------------------- |
| clusterName                  | the name of the folder in the git repository which contains all the csv files for the cluster |
| gitRepoUrl                   | the git repository url kavir forwards the information to                                      |
| gitProjectAccessToken        | the git project access token kavir uses to access the git repository                          |
| gitUserName                  | the username that is shown for the commits made by kavir                                      |
| gitUserEmail                 | the email that is shown for the commits made by kavir                                         |
| reportDeployments            | determines whether kavir gathers information on deployments                                   |
| reportReplicasets            | determines whether kavir gathers information on replicasets                                   |
| reportStatefulsets           | determines whether kavir gathers information on statefulsets                                  |
| reportDaemonsets             | determines whether kavir gathers information on daemonsets                                    |
| reportJobs                   | determines whether kavir gathers information on jobs                                          |
| reportCronjobs               | determines whether kavir gathers information on cronjobs                                      |
| reportReplicationcontrollers | determines whether kavir gathers information on replicationcontrollers                        |

## releases

Check the packages of this repository to view the releases of the container.

## git repository preview

kavir creates the following structure in the git repository specified by `repoUrl`:

```text
├── clusterName1
│   ├── cronjobs.csv
│   ├── daemonsets.csv
│   ├── deployments.csv
│   ├── jobs.csv
│   ├── replicasets.csv
│   ├── replicationcontrollers.csv
│   ├── statefulsets.csv
├── clusterName2
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
kavir,ghcr.io/telekom-mms/kavir:1.0.1
my-cronjob,container-registry.acme.de/cronjobs/my-cronjob:1.0.0
```

In addition you may check if your git hosting service supports the rendering of csv files. This way you can have a look at the csv files ready rendered without further ado.

* [GitHub csv rendering](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files#rendering-csv-and-tsv-data)
* [GitLab csv rendering](https://docs.gitlab.com/ee/user/project/repository/files/csv.html)
