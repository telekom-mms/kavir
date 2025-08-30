# kavir - **K**ubernetes **A**pplication **V**ers**I**on **R**eporter - git-pages

The `pipelines` folder contains pipeline templates to utilise the pipeline and pages features of a git hosting service in a convenient way to run kavirs html-report-builder. The pipeline

* runs the `kavir-html-report-builder` container
* provides the environment variables for the `kavir-html-report-builder` container
* utilises the pages feature of the git hosting service to host kavirs html reports

## Usage

* copy the pipeline template into your git repository that contains the kavir csv reports
  * adjust the pipeline template to your needs
