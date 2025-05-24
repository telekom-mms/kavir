"""
kavir - html-report-builder
version: 1.1.0
"""

import argparse, csv, json, dominate, os
from dominate.tags import *

scriptPath = os.path.dirname(os.path.realpath(__file__))

# load command line arguments
parser = argparse.ArgumentParser(description="Build a html report (static html file) from your kavir csv files")
parser.add_argument("-c", "--config", help="the path to config file", required=True)
parser.add_argument("-n", "--clusterName", help="the name of the folder which contains all the csv files for the cluster", required=True)
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
    print(f"[DEBUG] config file      : {args.config}")
    print(f"[DEBUG] clusterName      : {clusterName}")
    print(f"[DEBUG] reportName       : {reportName}")
    print(f"[DEBUG] srcDir           : {srcDir}")
    print(f"[DEBUG] styleFile        : {styleFile}")
    print(f"[DEBUG] outDir           : {outDir}")
    print(f"[DEBUG] menuEnabled      : {menuEnabled}")
    print(f"[DEBUG] menuLinkBasePath : {menuLinkBasePath}")

htmlReport = dominate.document(title=reportName)

def addStyle():
    file = open(styleFile, "r")
    styleFileContent = file.read()
    file.close()
    htmlReport.head.add(style(styleFileContent))

def addHeader():
    header = div(cls="header")
    header.add(h1(f"{reportName} ({clusterName})", cls="headline"))
    if (menuEnabled == False):
        htmlReport.add(header)
        return
    for cluster in clusters:
        if cluster == clusterName:
            header.add(a(cluster, href=str(os.path.join(menuLinkBasePath, cluster + ".html")), cls="active"))
        else:
            header.add(a(cluster, href=str(os.path.join(menuLinkBasePath, cluster + ".html"))))
    htmlReport.add(header)

def addWrSection(wr):
    htmlReport.add(h2(wr))
    try:
        file = open(os.path.join(clusterDir, wr + ".csv"), "r", newline="")
        csvRows = list(csv.reader(file, delimiter=","))
        file.close()
    except:
        htmlReport.add(p("no report found"))
        return
    if csvRows == [["out of scope"]]:
        htmlReport.add(p("not in scope of the report"))
        return
    if csvRows == [["Name", "Image:Tag"]]:
        htmlReport.add(p(f"in scope of the report; but there are no {wr} to report about"))
        return
    wrData = table()
    # table header
    with wrData.add(thead()):
        td("Name", cls="table-header-name")
        td("Image", cls="table-header-image")
        td("Tag/Version", cls="table-header-tag-version")
    # table body
    with wrData.add(tbody()):
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
    htmlReport.add(wrData)

def main():
    # report style
    addStyle()
    # report header
    addHeader()
    # report workload resources section
    wrs = [
        "deployments",
        "replicasets",
        "statefulsets",
        "daemonsets",
        "jobs",
        "cronjobs",
        "replicationcontrollers"
    ]
    for wr in wrs:
        addWrSection(wr)
    # save the report
    with open(outFile, "w") as file:
        file.write(str(htmlReport.render()))
    print(f"[INFO] Built html report for cluster {clusterName}")

if __name__ == "__main__":
    main()
