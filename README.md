# kavir - **K**ubernetes **A**pplication **V**ers**I**on **R**eporter

kavir forwards information about applications in a kubernetes cluster to a git repository. This way software and stakeholders without access to the kubernetes cluster can still see the image names and versions that are used by the applications in the cluster.

kavir can observe all [kubernetes workload resources](https://kubernetes.io/docs/concepts/workloads/controllers/).

## kavir - container image

The container uses a bash script to gather information via `kubectl` and commits them as csv files to the predefined git repository. Look inside the `docker/` folder to read more about it and how to use it.

## helm chart

The helm chart uses the container image described above to create a [kubernetes cronjob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/) inside the kubernetes cluster which periodically updates the csv files in the predefined git repository. Look inside the `charts/kavir/` folder to read more about it and how to use it.

## html-report-builder

The html-report-builder is a python script that uses the csv files to build a html report (static html file). Look inside the `html-report-builder/` folder to read more about it and how to use it.

## git-pages

Pipeline templates to utilise the pipeline and pages features of a git hosting service in a convenient way to run kavirs html-report-builder. Look inside the `git-pages/` folder to read more about it and how to use it.
