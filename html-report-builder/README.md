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
* run `pip3 install -r requirements.txt`
* run `python3 main.py -c config.json -n <clusterName> [-v]`
  * run `python3 main.py -h` for further information

The html-report-builder will use the folders inside the `srcDir` to build the report. Make sure `srcDir` contains only folders you want to have listed in the menu.

You can run the html-report-builder with the example files in this repository:

```bash
cd kavir
python3 ./html-report-builder/main.py -c ./html-report-builder/config.json -n dev
```

## html report preview

Check out the `examples` folder for an example.
