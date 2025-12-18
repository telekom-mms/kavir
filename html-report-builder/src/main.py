# https://github.com/telekom-mms/kavir
# kavir - html-report-builder
# version: 2.1.0

import argparse, csv, json, os
from jinja2 import Template

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
    print(f"[ERR] An error occured while trying to load the config file: {args.config}. The config file does not exist or has syntax errors.")
    exit(1)
clusterName = args.clusterName

# load mandatory config parameters from config file
configLoadErrors = []
try:
    reportName = configParameters["report"]["name"]
except:
    configLoadErrors.append("report.name")
try:
    reportScope = configParameters["report"]["scope"]
except:
    configLoadErrors.append("report.scope")
try:
    srcDirPath = configParameters["paths"]["srcDir"]
except:
    configLoadErrors.append("paths.srcDir")
try:
    templateFilePath = configParameters["paths"]["templateFile"]
except:
    configLoadErrors.append("paths.templateFile")
try:
    outDirPath = configParameters["paths"]["outDir"]
except:
    configLoadErrors.append("paths.outDir")
try:
    menuEnabled = configParameters["menu"]["enabled"]
except:
    configLoadErrors.append("menu.enabled")

# load config parameters from config file (mandatory requirement depends on other variables)
if menuEnabled:
    try:
        menuLinkBasePath = configParameters["menu"]["linkBasePath"]
    except:
        configLoadErrors.append("menu.linkBasePath")

# evaluate config load errors
if configLoadErrors:
    for parameter in configLoadErrors:
        print(f"[ERR] The config file {args.config} is incomplete: {parameter} is missing. Please use the provided config file template as a reference.")
    exit(1)

# load optional config parameters from config file
styleFilePath = configParameters.get("paths").get("styleFile")

# config parameters validation
configValueErrors = []
for workloadResource in reportScope:
    if workloadResource not in ["deployments", "replicasets", "statefulsets", "daemonsets", "jobs", "cronjobs", "replicationcontrollers"]:
        configValueErrors.append(f"[ERR] Items in report.scope array must be one of the following: deployments, replicasets, statefulsets, daemonsets, jobs, cronjobs, replicationcontrollers. '{workloadResource}' did not match.")
if (not os.path.exists(srcDirPath)):
    configValueErrors.append(f"[ERR] Could not find the srcDir directory: {srcDirPath}")
if (not os.path.exists(templateFilePath)):
    configValueErrors.append(f"[ERR] Could not find the template file: {templateFilePath}")
templateFilePathParts = templateFilePath.split(".")
if (len(templateFilePathParts) < 3 or os.sep in templateFilePathParts[-2] or templateFilePathParts[-1] != "j2"):
    configValueErrors.append(f"[ERR] The template file must adhere to the following structure: <name>.<fileextension>.j2. {templateFilePath} did not match.")
if (styleFilePath is not None and not os.path.exists(styleFilePath)):
    configValueErrors.append(f"[ERR] Could not find the style file: {styleFilePath}")
if (not os.path.exists(outDirPath)):
    configValueErrors.append(f"[ERR] Could not find the outDir directory: {outDirPath}")

# compound config parameters
clusterDirPath = os.path.join(srcDirPath, clusterName)
outFileExtension = templateFilePathParts[-2]
outFilePath = os.path.join(outDirPath, f"{clusterName}.{outFileExtension}")

# compound config parameters validation
if (not os.path.exists(clusterDirPath)):
    configValueErrors.append(f"[ERR] Could not find the cluster directory: {clusterDirPath}")

# evaluate config value errors
if configValueErrors:
    for error in configValueErrors:
        print(error)
    exit(1)

# get the names of all clusters
clusters = [f for f in os.listdir(srcDirPath) if os.path.isdir(os.path.join(srcDirPath, f))]
if ".git" in clusters:
    clusters.remove(".git")

# print config parameters
if args.verbose:
    print(f"[DEBUG] config file        : {args.config}")
    print(f"[DEBUG] clusterName        : {clusterName}")
    print(f"[DEBUG] report.name        : {reportName}")
    print(f"[DEBUG] report.scope       : " + ", ".join(workloadResource for workloadResource in reportScope))
    print(f"[DEBUG] paths.srcDir       : {srcDirPath}")
    print(f"[DEBUG] paths.templateFile : {templateFilePath}")
    print(f"[DEBUG] paths.styleFile    : {styleFilePath}")
    print(f"[DEBUG] paths.outDir       : {outDirPath}")
    print(f"[DEBUG] menu.enabled       : {menuEnabled}")
    print(f"[DEBUG] menu.linkBasePath  : {menuLinkBasePath}")

# load report template
templateFile = open(templateFilePath, "r")
template = Template(templateFile.read())
templateFile.close()

# load style file
if styleFilePath is not None:
    styleFile = open(styleFilePath, "r")
    style = styleFile.read()
    styleFile.close()
else:
    style = ""

# load data from csv reports
workloadResourceReports = []
for workloadResource in reportScope:
    workloadResourceReport = {}
    workloadResourceReport["name"] = workloadResource
    try:
        csvReportFile = open(os.path.join(clusterDirPath, workloadResource + ".csv"), "r", newline="")
        csvReport = list(csv.reader(csvReportFile, delimiter=","))
        csvReportFile.close()
    except:
        workloadResourceReport["nodata"] = "no report found"
        workloadResourceReports.append(workloadResourceReport)
        print(f"[WARN] Could not find a report for {workloadResource}")
        continue
    if csvReport == [["out of scope"]]:
        workloadResourceReport["nodata"] = "not in scope of the report"
        workloadResourceReports.append(workloadResourceReport)
        continue
    if csvReport == [["Name", "Image:Tag"]] or csvReport == [["Name", "Namespace", "Image:Tag"]]:
        workloadResourceReport["nodata"] = f"in scope of the report; but there are no {workloadResource} to report about"
        workloadResourceReports.append(workloadResourceReport)
        continue
    workloadResourceReport["data"] = []
    if csvReport[0] == ["Name", "Namespace", "Image:Tag"]:
        workloadResourceReport["namespaces"] = True
    else:
        workloadResourceReport["namespaces"] = False
    for line in csvReport[1:]:
        data = {}
        # corner case: skip empty lines (e.g. at the end of the file)
        if (len(line) == 0):
            continue
        coloumnIndex = 0
        # "Name"
        data["name"] = line[coloumnIndex]
        coloumnIndex += 1
        # "Namespace"
        if workloadResourceReport["namespaces"] == True:
            data["namespace"] = line[coloumnIndex]
            coloumnIndex += 1
        # "Image" and "Tag"
        # get all image:tag strings in the current line
        imageAndTagStrings = line[coloumnIndex].split(" ")
        # convert every image:tag string to a pair which then contains the image and the tag as separate strings
        # store the pairs back to a list which then contains all image-tag-pairs for the current line
        data["imageAndTagPairs"] = []
        for imageAndTagString in imageAndTagStrings:
            data["imageAndTagPairs"].append(imageAndTagString.split(":"))
        workloadResourceReport["data"].append(data)
    workloadResourceReports.append(workloadResourceReport)

# build report
htmlReport = template.render(
    clusterName = clusterName,
    reportName = reportName,
    style = style,
    menuEnabled = menuEnabled,
    clusters = clusters,
    menuLinkBasePath = menuLinkBasePath,
    workloadResourceReports = workloadResourceReports
)

# save report
outFile = open(outFilePath, "w")
outFile.write(htmlReport)
outFile.close()

print(f"[INFO] Built {outFileExtension} report for cluster {clusterName}")
