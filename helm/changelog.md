# Changelog

All notable changes to this component will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 1.1.0

### Added

* `helm/templates/cronjob.yaml`
  * `successfulJobsHistoryLimit`
  * `failedJobsHistoryLimit`
* `helm/values.yaml.template`
  * `successfulJobsHistoryLimit`
  * `failedJobsHistoryLimit`

## 1.0.1

### Fixed

* The clusterrole now grants access to the resources `replicationcontrollers`, `jobs` and `cronjobs` like intended.
  * Previously the clusterrole incorrectly granted the verbs for `replicationcontrollers` in the apiGroup `"apps"` instead of `""`.
  * Previously the clusterrole incorrectly granted the verbs for `jobs` and `cronjobs` in the apiGroup `"apps"` instead of `"batch"`.
* Moved documentation from `helm/` to `docker/`

## 1.0.0

Initial version
