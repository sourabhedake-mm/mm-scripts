#!/usr/bin/env bash

prefix=$1
start_index=$2

for tenant_index in $(seq $start_index 3000); do
    echo $tenant_index
	curl 'https://api-boris-us-west.eng.macrometa.io/_api/tenant' \
      -u 'root:Macrometa123!@#' \
	  --data-raw "{\"email\":\"${prefix}_${tenant_index}@test.com\",\"passwd\":\"Sour@123\",\"dcList\":\"boris-ap-west,boris-us-east,boris-us-west\",\"plan\":\"FREE\",\"attribution\":\"Macrometa\",\"contact\":{\"firstname\":\"\",\"lastname\":\"\",\"email\":\"${prefix}_${tenant_index}@test.com\",\"phone\":\"\",\"line1\":\"\",\"line2\":\"\",\"city\":\"\",\"state\":\"\",\"country\":\"\",\"zipcode\":\"\"}}" \
	  --compressed
#    sleep 5s
    echo
    echo
done
