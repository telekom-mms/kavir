#!/bin/bash
# https://github.com/telekom-mms/kavir

# https://gist.github.com/mohanpedala/1e2ff5661761d3abd0385e8223e16425
set -e
set -o pipefail

# optional env vars
verbose=${verbose:=true}
reportName=${reportName:=Kubernetes Application Version Report}
reportScope=${reportScope:=deployments replicasets statefulsets daemonsets jobs cronjobs replicationcontrollers}
pathsTemplateFile=${pathsTemplateFile:=/etc/kavir-html-report-builder/templates/simple.html.j2}
pathsStyleFile=${pathsStyleFile:=/etc/kavir-html-report-builder/styles/tech.css}
menuEnabled=${menuEnabled:=true}

# mandatory env vars
mandatoryEnvVarUndefined=0
if [ -z "${pathsSrcDir}" ]; then
  echo '[ERR] env var "pathsSrcDir" is undefined.'
  mandatoryEnvVarUndefined=1
fi
if [ -z "${pathsOutDir}" ]; then
  echo '[ERR] env var "pathsOutDir" is undefined.'
  mandatoryEnvVarUndefined=1
fi
if [[ -z "${menuLinkBasePath}" && "${menuEnabled}" == "true" ]]; then
  echo '[ERR] env var "menuLinkBasePath" is undefined (which is not allowed if env var "menuEnabled" == "true").'
  mandatoryEnvVarUndefined=1
fi
if [ $mandatoryEnvVarUndefined -eq 1 ]; then
  exit 1
fi

# build kavir html-report-builder config.json
reportScopeBashArray=($reportScope)
reportScopeJsonArray=$(printf '%s\n' "${reportScopeBashArray[@]}" | jq -R . | jq -s .)
configReport=$(jq -n \
--arg name "${reportName}" \
--argjson scope "${reportScopeJsonArray}" \
'$ARGS.named')

configPaths=$(jq -n \
--arg srcDir "${pathsSrcDir}" \
--arg templateFile "${pathsTemplateFile}" \
--arg styleFile "${pathsStyleFile}" \
--arg outDir "${pathsOutDir}" \
'$ARGS.named')

configMenu=$(jq -n \
--argjson enabled "${menuEnabled}" \
--arg linkBasePath "${menuLinkBasePath}" \
'$ARGS.named')

config=$(jq -n \
--argjson report "${configReport}"  \
--argjson paths "${configPaths}" \
--argjson menu "${configMenu}" \
'$ARGS.named')

echo $config | jq . > /etc/kavir-html-report-builder/config.json

if [ $verbose == "true" ]; then
  echo "[DEBUG] config.json:"
  cat /etc/kavir-html-report-builder/config.json
fi

# get clusters
clusters=$(cd $pathsSrcDir;  ls -d */ | sed "s#/##")

# build the html reports
if [ $verbose == "true" ]; then
  for cluster in ${clusters[@]}; do
    python3 /opt/kavir-html-report-builder/main.py -c /etc/kavir-html-report-builder/config.json -n $cluster -v
  done
else
  for cluster in ${clusters[@]}; do
    python3 /opt/kavir-html-report-builder/main.py -c /etc/kavir-html-report-builder/config.json -n $cluster
  done
fi
