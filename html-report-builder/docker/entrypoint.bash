#!/bin/bash
# https://github.com/telekom-mms/kavir/tree/main

# https://gist.github.com/mohanpedala/1e2ff5661761d3abd0385e8223e16425
set -e
set -o pipefail

# optional env vars
verbose=${verbose:=true}
report_name=${report_name:=Kubernetes Application Version Report}
report_scope=${report_scope:=deployments replicasets statefulsets daemonsets jobs cronjobs replicationcontrollers}
paths_templateFile=${paths_templateFile:=/etc/kavir-html-report-builder/templates/simple.html.j2}
paths_styleFile=${paths_styleFile:=/etc/kavir-html-report-builder/styles/simple.css}
menu_enabled=${menu_enabled:=true}

# mandatory env vars
mandatory_env_var_undefined=0
if [ -z "${paths_srcDir}" ]; then
  echo '[ERR] env var "paths_srcDir" is undefined.'
  mandatory_env_var_undefined=1
fi
if [ -z "${paths_outDir}" ]; then
  echo '[ERR] env var "paths_outDir" is undefined.'
  mandatory_env_var_undefined=1
fi
if [[ -z "${menu_linkBasePath}" && "${menu_enabled}" == "true" ]]; then
  echo '[ERR] env var "menu_linkBasePath" is undefined (which is not allowed if env var "menu_enabled" == "true").'
  mandatory_env_var_undefined=1
fi
if [ $mandatory_env_var_undefined -eq 1 ]; then
  exit 1
fi

# build kavir html-report-builder config.json
report_scope_bash_array=($report_scope)
report_scope_json_array=$(printf '%s\n' "${report_scope_bash_array[@]}" | jq -R . | jq -s .)
config_report=$(jq -n \
--arg name "${report_name}" \
--argjson scope "${report_scope_json_array}" \
'$ARGS.named')

config_paths=$(jq -n \
--arg srcDir "${paths_srcDir}" \
--arg templateFile "${paths_templateFile}" \
--arg styleFile "${paths_styleFile}" \
--arg outDir "${paths_outDir}" \
'$ARGS.named')

config_menu=$(jq -n \
--argjson enabled "${menu_enabled}" \
--arg linkBasePath "${menu_linkBasePath}" \
'$ARGS.named')

config=$(jq -n \
--argjson report "${config_report}"  \
--argjson paths "${config_paths}" \
--argjson menu "${config_menu}" \
'$ARGS.named')

echo $config | jq . > /etc/kavir-html-report-builder/config.json

if [ $verbose == "true" ]; then
  echo "[DEBUG] config.json:"
  cat /etc/kavir-html-report-builder/config.json
fi

# get clusters
clusters=$(cd $paths_srcDir;  ls -d */ | sed "s#/##")

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
