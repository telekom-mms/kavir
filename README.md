# kavir - **K**ubernetes **A**pplication **V**ers**I**on **R**eporter

kavir forwards information about applications in a kubernetes cluster to a git repository. This way software and stakeholders that do not have access to the kubernetes cluster can still see the image names and versions that are used by the applications in the cluster.

kavir can observe all [kubernetes workload resources](https://kubernetes.io/docs/concepts/workloads/controllers/).

To achieve this goal, kavir relies on three components:

## container image

The container is based on [bitnamis kubectl container](https://github.com/bitnami/containers/tree/main/bitnami/kubectl) published under the [Apache2 License](https://www.apache.org/licenses/LICENSE-2.0). It uses a bash file which gathers information via `kubectl` and commits them as csv files to the predefined git repository. Look inside the `docker` folder to read more about it and how to use it.
