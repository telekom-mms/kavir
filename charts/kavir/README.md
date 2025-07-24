# kavir - **K**ubernetes **A**pplication **V**ers**I**on **R**eporter - helm

The helm chart uses the container image described in the `docker` folder to create a [kubernetes cronjob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/) inside the kubernetes cluster which periodically updates the csv files in the predefined git repository.

## values.yaml

| variable                   | description                                                                                   |
| -------------------------- | --------------------------------------------------------------------------------------------- |
| clusterName                | the name of the folder in the git repository which contains all the csv files for the cluster |
| **cronjob**                | the kubernetes cronjob schedule                                                               |
| schedule                   | the kubernetes cronjob schedule                                                               |
| successfulJobsHistoryLimit | This field tells kubernetes how many successful (completed) jobs to keep. For example, if you set it to 3, only the three most recent successful jobs will be retained. |
| failedJobsHistoryLimit     | This field tells kubernetes how many failed jobs to keep. For example, if you set it to 1, only the most recent failed job will remain. |
| **containerRegistry**      |                                                                                               |
| image                      | the name of the image in the container registry. The default value refers to the image provided by this repository via [ghcr](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) |
| dockerconfigjson           | the [.dockerconfigjson](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/) to access the container image. If you want to use the default image, provide a dockerconfigjson to pull from the ghcr |
| **git**                    |                                                                                               |
| repoUrl                    | the git repository url kavir forwards the information to                                      |
| projectAccessToken         | the git project access token kavir uses to access the git repository (role: Maintainer, scopes: write_repository) |
| userName                   | the username that is shown for the commits made by kavir                                      |
| userEmail                  | the email that is shown for the commits made by kavir                                         |
| **report**                 |                                                                                               |
| namespaces                 | determines whether kavir includes namespaces in the csv reports                               |
| **report.scope**           |                                                                                               |
| deployments                | determines whether kavir gathers information on deployments                                   |
| replicasets                | determines whether kavir gathers information on replicasets                                   |
| statefulsets               | determines whether kavir gathers information on statefulsets                                  |
| daemonsets                 | determines whether kavir gathers information on daemonsets                                    |
| jobs                       | determines whether kavir gathers information on jobs                                          |
| cronjobs                   | determines whether kavir gathers information on cronjobs                                      |
| replicationcontrollers     | determines whether kavir gathers information on replicationcontrollers                        |

## Usage

* create a git repository to which the information is committed
  * create a project access token for this git repository
    * role: Maintainer
    * scopes: write_repository
* create `values.yaml` from `values.yaml.template`
  * configure `values.yaml`
* run `helm install kavir ./helm --namespace kavir --create-namespace`
