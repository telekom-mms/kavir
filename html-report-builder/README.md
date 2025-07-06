# kavir - **K**ubernetes **A**pplication **V**ers**I**on **R**eporter - html-report-builder

The html-report-builder is a python script that uses the csv files to build a html report (static html file).

## config.json

| variable     | description                                                                |
| ------------ | -------------------------------------------------------------------------- |
| reportName   | the name of the report that is displayed in the report header              |
| **paths**    |                                                                            |
| srcDir       | the path to the directory which contains the folders for the html report (If the directory is a git repository keep in mind that the html-report-builder does not git pull the latest commits. You have to take care of this on your own.) |
| styleFile    | the path to the style file (The content of the style file is rendered into the html report. Therefore it is not needed after the html report was created.) |
| outDir       | the path to the directory that will contain the html report created by this script (The script does not create missing parent directories.) |
| **menu**     |                                                                            |
| enabled      | indicates whether the menu is displayed in the report header               |
| linkBasePath | the link base path that is used to build the href of the links in the menu |

## Usage

* create `config.json` from `config.json.template`
  * configure `config.json`
* run `pip3 install -r ./requirements.txt`
* run `python3 ./main.py -c ./config.json -n <clusterName> [-v]`
  * run `python3 ./main.py -h` for further information

The html-report-builder will use the folders inside the `srcDir` to build the report. Make sure `srcDir` contains only folders you want to have listed in the menu.

You can run the html-report-builder with the example files in this repository:

```bash
python3 ./html-report-builder/main.py -c ./html-report-builder/config.json.template -n dev
python3 ./html-report-builder/main.py -c ./html-report-builder/config.json.template -n prod
```

## html report preview

Check out the `examples` folder for an example.

## template variables

The following variables are passed to the template and can therefore be used by Jinja2 inside the template. The variables are specified in jq filter syntax.

| variable                                               | type                   | description                                                                                             |
| ------------------------------------------------------ | ---------------------- | ------------------------------------------------------------------------------------------------------- |
| clusterName                                            | String                 | the name of the cluster                                                                                 |
| reportName                                             | String                 | the name of the report                                                                                  |
| style                                                  | String                 | the content of the style file                                                                           |
| menuEnabled                                            | Boolean                | indicates whether the user wants to display a menu in the report                                        |
| clusters                                               | List of strings        | the names of all available clusters. (Can be used for a menu.)                                          |
| menuLinkBasePath                                       | String                 | a link base path that can be used to build the href of links in the menu                                |
| workloadResourceReports                                | List of dictionairies  | the workload resource reports                                                                           |
| workloadResourceReports[].name                         | String                 | the name of the kubernetes workload resource                                                            |
| workloadResourceReports[].nodata                       | String                 | when present, there is no data for the kubernetes workload resource. The value contains the reason why. |
| workloadResourceReports[].data                         | List of dictionairies  | when present, it contains all workloads for the kubernetes workload resource                            |
| workloadResourceReports[].data[].name                  | String                 | the name of the workload                                                                                |
| workloadResourceReports[].data[].namespace             | String                 | when present, it contains the namespace of the workload                                                 |
| workloadResourceReports[].data[].imageAndTagPairs      | List of lists          | the list of image and tag pairs of the workload                                                         |
| workloadResourceReports[].data[].imageAndTagPairs[][0] | String                 | the image                                                                                               |
| workloadResourceReports[].data[].imageAndTagPairs[][1] | String                 | the image tag                                                                                           |
| workloadResourceReports[].namespaces                   | Boolean                | when present, indicates whether namespaces are included in the report                                   |
