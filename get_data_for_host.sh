#!/usr/bin/env bash

MAX_FALSE=100000
MAX_TRUE=100000
MAPPING_FILE="data/indexer_mapper"
REPO_DIR="/home/hoangch/code/java/search-engine"
HOST="$1"
CURRENT_DIR=`pwd`

bash create_indexer_mapper.sh
if [ ! -f "$MAPPING_FILE" ]; then
	echo "$MAPPING_FILE is not existed"
	return
fi
cd $REPO_DIR
export JAVA_MEM="128m"
buckets=(`bin/commons/java.sh vn.itim.engine.indexer.BucketIdGetterTool $HOST | grep "host's buckets" | cut -d':' -f2`)
buckets_length=${#buckets[@]}
cd $CURRENT_DIR

for file in "data/${HOST} data/${HOST}.gz"; do
	if [ -f "$file" ]; then rm "$file"; fi
done
host_esc=`echo $HOST | sed 's/\./\\\./g'`
bucket_max_false=`expr $MAX_FALSE / $buckets_length`
bucket_max_true=`expr $MAX_TRUE / $buckets_length`
for bucket in "${buckets[@]}"; do
	indexer=`cat $MAPPING_FILE | awk -v b=$bucket '$2 == b {print $1}'`
	echo "Host: $HOST; Bucket: $bucket; Indexer: $indexer"
	ssh indexer${indexer}v.dev.itim.vn "zcat /var/itim/indexer/${bucket}_next/common/remurl2docid.gz | awk '\$4==17'| grep -E '^https?://${host_esc}/' | cut -d' ' -f1 | shuf -n $bucket_max_true " | awk '{print "true "$1}' >> data/${HOST}
	ssh indexer${indexer}v.dev.itim.vn "zcat /var/itim/indexer/${bucket}_next/common/url2docid.gz |grep -E '^https?://${host_esc}/' | cut -d' ' -f1 | shuf -n $bucket_max_false " | awk '{print "false "$1}' >> data/${HOST}
done
cat data/${HOST} | gzip > data/${HOST}.gz
rm data/${HOST}
