"""
kavir - html-report-builder
version: 1.0.0
"""

import argparse, csv, json, dominate, os
from dominate.tags import *

scriptPath = os.path.dirname(os.path.realpath(__file__))

# load command line arguments
parser = argparse.ArgumentParser(description="Build a single page html report from your kavir csv files")
parser.add_argument("-c", "--config", help="the path to config file", required=True)
parser.add_argument("-n", "--clusterName", help="the name of the folder in the git repository which contains all the csv files for the cluster", required=True)
parser.add_argument("-v", "--verbose", help="print the used config parametes",  action='store_true')
args = parser.parse_args()

try:
    configParameters = json.load(open(args.config))
except:
    print(f"[ERR] Could not find the config file: {args.config}")
    exit(1)
clusterName = args.clusterName.lower()

# config parameters from config file
try:
    reportName = configParameters["reportName"]
    srcDir = configParameters["paths"]["srcDir"]
    styleFile = configParameters["paths"]["styleFile"]
    outDir = configParameters["paths"]["outDir"]
    menuEnabled = configParameters["menu"]["enabled"]
    menuLinkBasePath = configParameters["menu"]["linkBasePath"]
except:
    print(f"[ERR] The config file {args.config} is incomplete. Please use the provided template as a reference.")
    exit(1)

# compound config parameters
clusterDir = os.path.join(srcDir, clusterName)
outFile = os.path.join(outDir, clusterName + ".html")

# config parameters validation
if (not os.path.exists(clusterDir)):
    print(f"[ERR] Could not find the srcDir directory: {clusterDir}")
    exit(1)
if (not os.path.exists(styleFile)):
    print(f"[ERR] Could not find the style file: {styleFile}")
    exit(1)
if (not os.path.exists(outDir)):
    print(f"[ERR] Could not find the outDir directory: {outDir}")
    exit(1)

# get the names of all clusters
clusters = [f for f in os.listdir(srcDir) if os.path.isdir(os.path.join(srcDir, f))]
if ".git" in clusters:
    clusters.remove(".git")

# print config parameters
if args.verbose:
    print(f"[INFO] config file      : {args.config}")
    print(f"[INFO] clusterName      : {clusterName}")
    print(f"[INFO] reportName       : {reportName}")
    print(f"[INFO] srcDir           : {srcDir}")
    print(f"[INFO] styleFile        : {styleFile}")
    print(f"[INFO] outDir           : {outDir}")
    print(f"[INFO] menuEnabled      : {menuEnabled}")
    print(f"[INFO] menuLinkBasePath : {menuLinkBasePath}")

htmlReport = dominate.document(title=reportName)

def setStyle():
    file = open(styleFile, "r")
    styleFileContent = file.read()
    file.close()
    htmlReport.head.add(style(styleFileContent))

def createHeader():
    header = ul()
    header.add(li(h1(f"{reportName} ({clusterName.upper()})"), cls="headline"))
    if (menuEnabled == True):
        for cluster in clusters:
            header.add(li(a(cluster.upper(), href=str(os.path.join(menuLinkBasePath, cluster + ".html")))))
    htmlReport.add(header)

def createResourceSection(resource):
    htmlReport.add(h2(resource))
    try:
        file = open(os.path.join(clusterDir, resource + ".csv"), "r", newline="")
        csvRows = list(csv.reader(file, delimiter=","))
        file.close()
    except:
        htmlReport.add(div("no report found"))
        return
    if csvRows == [["out of scope"]]:
        htmlReport.add(div("not in scope of the report"))
        return
    if csvRows == [["Name", "Image:Tag"]]:
        htmlReport.add(div(f"in scope of the report; but there are no {resource} to report about"))
        return
    resourceData = table()
    with resourceData.add(tbody()):
        # table header
        tableHeader = tr(cls="table-header")
        tableHeader.add(td("Name", cls="table-header-name"))
        tableHeader.add(td("Image", cls="table-header-image"))
        tableHeader.add(td("Tag/Version", cls="table-header-tag-version"))
        # table body
        for csvRow in csvRows[1:]:
            # corner case: skip empty lines (e.g. at the end of the file)
            if (len(csvRow) == 0):
                continue
            # table row
            tableRow = tr()
            # "Name" cell
            tableRow.add(td(csvRow[0]))
            # get all image:tag strings for this row
            imageAndTagStrings = csvRow[1].split(" ")
            # convert every image:tag string to a pair which then contains the image and the tag as separate strings
            # store the pairs back to a list which then contains all image-tag-pairs for this row
            imageAndTagPairs = []
            for imageAndTagString in imageAndTagStrings:
                imageAndTagPairs.append(imageAndTagString.split(":"))
            # "Image" cell and "Tag/Version" cell
            imageCell = td()
            tagCell = td()
            for imageAndTagPair in imageAndTagPairs:
                imageCell.add(imageAndTagPair[0])
                imageCell.add(br())
                # corner case: image has no tag
                try:
                    tagCell.add(imageAndTagPair[1])
                    tagCell.add(br())
                except:
                    tagCell.add("-")
                    tagCell.add(br())
            imageCell["style"] = "white-space:pre-line;"
            tagCell["style"] = "white-space:pre-line;"
            tableRow.add(imageCell)
            tableRow.add(tagCell)
    htmlReport.add(resourceData)

def main():
    # report style
    setStyle()
    # report header
    createHeader()
    # report resource section
    resources = [
        "deployments",
        "replicasets",
        "statefulsets",
        "daemonsets",
        "jobs",
        "cronjobs",
        "replicationcontrollers"
    ]
    for resource in resources:
        createResourceSection(resource)
    # save the report
    with open(outFile, "w") as file:
        file.write(str(htmlReport.render()))

if __name__ == "__main__":
    main()
