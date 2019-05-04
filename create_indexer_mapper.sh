#!/usr/bin/env bash

MAPPING_FILE="data/indexer_mapper"
mkdir -p data
if [ ! -f "$MAPPING_FILE" ] || test `find "$MAPPING_FILE" -mmin +1440`
then
	echo "Getting new file"
	if [ -f "$MAPPING_FILE" ]; then rm "$MAPPING_FILE"; fi
	for x in {1..30}; do
		buckets=`ssh -o StrictHostKeyChecking=no indexer${x}v.dev.itim.vn "ls /var/itim/indexer/ | grep '_next'"`
		for bucket in $buckets; do
			bucket=`echo $bucket | sed 's/_next//g'`
			echo "$x $bucket" >> "$MAPPING_FILE"
		done
	done
	total_bucket=`cat data/indexer_mapper | wc -l`
	if [[ $total_bucket -ne 1024 ]]; then
		echo "TOTAL BUCKETS IS NOT 1024"
		rm "$MAPPING_FILE"
	fi
fi
