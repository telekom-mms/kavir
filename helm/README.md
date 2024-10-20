# kavir - **K**ubernetes **A**pplication **V**ers**I**on **R**eporter - helm

The helm chart uses the container image described in the `docker` folder to create a [kubernetes cronjob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/) inside the kubernetes cluster which periodically updates the csv files in the predefined git repository.

## values.yaml

| variable               | description                                                                                   |
| ---------------------- | --------------------------------------------------------------------------------------------- |
| namespace              | the kubernetes namespace for all the resources that the helm chart installs                   |
| schedule               | the kubernetes cronjob schedule                                                               |
| clusterName            | the name of the folder in the git repository which contains all the csv files for the cluster |
| **containerRegistry**  |                                                                                               |
| image                  | the name of the image in the container registry. The default value refers to the image provided by this repository via [ghcr](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) |
| dockerconfigjson       | the [.dockerconfigjson](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/) to access the container image. If you want to use the default image, provide a dockerconfigjson to pull from the ghcr |
| **git**                |                                                                                               |
| repoUrl                | the git repository url kavir forwards the information to                                      |
| projectAccessToken     | the git project access token kavir uses to access the git repository                          |
| userName               | the username that is shown for the commits made by kavir                                      |
| userEmail              | the email that is shown for the commits made by kavir                                         |
| **reportScope**        |                                                                                               |
| deployments            | determines whether kavir gathers information on deployments                                   |
| replicasets            | determines whether kavir gathers information on replicasets                                   |
| statefulsets           | determines whether kavir gathers information on statefulsets                                  |
| daemonsets             | determines whether kavir gathers information on daemonsets                                    |
| jobs                   | determines whether kavir gathers information on jobs                                          |
| cronjobs               | determines whether kavir gathers information on cronjobs                                      |
| replicationcontrollers | determines whether kavir gathers information on replicationcontrollers                        |

## Usage

* create a git repository to which the information is committed
* create a project access token for this git repository
  * role: Maintainer
  * scopes: write_repository
* create `values.yaml` from `values.yaml.template`
  * configure `values.yaml`
* run `helm install kavir kavir/helm`

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

* [Github csv rendering](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files#rendering-csv-and-tsv-data)
* [Gitlab csv rendering](https://docs.gitlab.com/ee/user/project/repository/files/csv.html)
