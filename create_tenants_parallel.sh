#!/usr/bin/env bash

prefix=$1
start_index=$2
end_index=$3

for tenant_index in $(seq $start_index $end_index); do
    echo $tenant_index
	curl 'https://api-sourabh-eu-west.eng.macrometa.io/_api/tenant' \
      -u 'root:Macrometa123!@#' \
	  --data-raw "{\"email\":\"${prefix}_${tenant_index}@test.com\",\"passwd\":\"Sour@123\",\"dcList\":\"sourabh-eu-west\",\"plan\":\"FREE\",\"attribution\":\"Macrometa\",\"contact\":{\"firstname\":\"\",\"lastname\":\"\",\"email\":\"${prefix}_${tenant_index}@test.com\",\"phone\":\"\",\"line1\":\"\",\"line2\":\"\",\"city\":\"\",\"state\":\"\",\"country\":\"\",\"zipcode\":\"\"}}" \
	  --compressed & sleep 0.5 
done
