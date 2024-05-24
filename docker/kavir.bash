#!/bin/bash
# kavir - docker
# version: 1.0.1

declare -A reportScope
reportScope=(
  ["deployments"]="$reportDeployments"
  ["replicasets"]="$reportReplicasets"
  ["statefulsets"]="$reportStatefulsets"
  ["daemonsets"]="$reportDaemonsets"
  ["jobs"]="$reportJobs"
  ["cronjobs"]="$reportCronjobs"
  ["replicationcontrollers"]="$reportReplicationcontrollers"
)

cd /tmp

gitRepoUrl=$(sed -e "s^//^//MadebyI-Am-hehu:$gitProjectAccessToken@^" <<< "$gitRepoUrl")
git clone $gitRepoUrl
cd $(basename $gitRepoUrl .git)
git config user.name "$gitUserName"
git config user.email "$gitUserEmail"

if [ ! -d "$clusterName" ]; then
  mkdir "$clusterName"
fi
cd "$clusterName"

for resource in "${!reportScope[@]}";do
  if [ "${reportScope[$resource]}" = true ]; then
    kubectl get $resource --all-namespaces -o jsonpath='{range .items[*]}{@.metadata.name}{","}{..image}{"\n"}{end}' >> "_$resource.csv"
    # sort by first coloumn (name)
    sort -k1 -n -t, "_$resource.csv" -o "_$resource.csv"
    echo "Name,Image:Tag" > "$resource.csv"
    # sort content of the second coloumn (images) since it might contain multiple entries (space separated)
    while read line; do
      coloumn1=$(echo $line | awk -F',' '{print $1}')
      coloumn2=$(echo $line | awk -F',' '{print $2}' | tr ' ' '\n' | sort | tr '\n' ' ' | xargs)
      echo "$coloumn1,$coloumn2" >> "$resource.csv"
    done <"_$resource.csv"
  else
    echo "out of scope" > "$resource.csv"
  fi
  git add "$resource.csv"
done

git commit -m "Updated report for cluster $clusterName"
git push $gitCredentialUrl
