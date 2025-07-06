#!/bin/bash
# kavir - docker
# version: 1.1.0

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

if [ "$reportNamespaces" = true ]; then
  csvReportHeader="Name,Namespace,Image:Tag"
  kubectlJsonpath='{range .items[*]}{@.metadata.name}{","}{@.metadata.namespace}{","}{..image}{"\n"}{end}'
else
  csvReportHeader="Name,Image:Tag"
  kubectlJsonpath='{range .items[*]}{@.metadata.name}{","}{..image}{"\n"}{end}'
fi

cd /tmp

gitCloneUrl=$(sed -e "s^//^//MadebyI-Am-hehu:$gitProjectAccessToken@^" <<< "$gitRepoUrl")
git clone $gitCloneUrl
cd $(basename $gitRepoUrl .git)
if [ ! -d "$clusterName" ]; then
  mkdir "$clusterName"
fi
cd "$clusterName"

for workloadResource in "${!reportScope[@]}"; do
  if [ "${reportScope[$workloadResource]}" = true ]; then
    kubectl get $workloadResource --all-namespaces -o jsonpath="${kubectlJsonpath}" > "_$workloadResource.csv"
    if [ "$reportNamespaces" = true ]; then
      # sort report by first coloumn ("Name") and second coloumn ("Namespace")
      sort -k1,1 -k2,2 -n -t, "_$workloadResource.csv" -o "_$workloadResource.csv"
    else
      # sort report by first coloumn ("Name")
      sort -k1 -n -t, "_$workloadResource.csv" -o "_$workloadResource.csv"
    fi
    echo $csvReportHeader > "$workloadResource.csv"
    while read line; do
      coloumnIndex=1
      name=$(echo $line | awk -v i=$coloumnIndex -F',' '{print $i}')
      ((coloumnIndex++))
      if [ "$reportNamespaces" = true ]; then
        namespace=$(echo $line | awk -v i=$coloumnIndex -F',' '{print $i}')
        ((coloumnIndex++))
      fi
      # sort content of the coloumn "Image:Tag" since it might contain multiple entries (space separated)
      image=$(echo $line | awk -v i=$coloumnIndex -F',' '{print $i}' | tr ' ' '\n' | sort | tr '\n' ' ' | xargs)
      echo "$name,${namespace:+$namespace,}$image" >> "$workloadResource.csv"
    done <"_$workloadResource.csv"
  else
    echo "out of scope" > "$workloadResource.csv"
  fi
  git add "$workloadResource.csv"
done

git config user.name "$gitUserName"
git config user.email "$gitUserEmail"
git commit -m "Updated csv reports for cluster $clusterName"
git push
