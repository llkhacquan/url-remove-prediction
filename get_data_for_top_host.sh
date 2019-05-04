#!/usr/bin/env bash

TOP="${1:-1000}"
echo "Get data for $TOP"

hosts=(`ssh linkserver2v.dev.itim.vn "zcat /itim/linkserver/storage/data/common/database/browser/hostpopularity_last7days.gz | head -n $TOP | cut -d' ' -f2"`)
count=1
for host in "${hosts[@]}"; do
	echo "Proccessing $count $host"
	bash get_data_for_host.sh "$host"
	(( count++ ))
done
