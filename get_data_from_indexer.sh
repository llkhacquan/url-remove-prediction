#!/bin/bash

# bash get_data_from_indexer.sh <server> <bucket> <host> [output_folder]
# output_folder is an optinal parameter, default is /tmp
# example: bash get_data_from_indexer.sh indexer2v 19 www.lazada.vn /tmp

if [[ $# -lt 3 ]] ; then
    echo $#
    echo "Usage: get_data_from_indexer.sh <server> <bucket> <host> [output_folder]"
    exit 1
fi

if [[ $# -eq 4 ]] ; then
    output_folder=$4
else
    output_folder="/tmp"
fi

if ! [ -f $output_folder/${2}.url2docid.gz ]; then
    echo Pulling url2docid.gz
    scp $1:/var/itim/indexer/${2}_next/common/url2docid.gz $output_folder/${2}.url2docid.gz
else
    echo Skip pulling url2docid.gz
fi
if ! [ -f $output_folder/${2}.remurl2docid.gz ]; then
    echo Pulling remurl2docid.gz
    scp $1:/var/itim/indexer/${2}_next/common/remurl2docid.gz $output_folder/${2}.remurl2docid.gz
else
    echo Skip pulling remurl2docid.gz
fi

if ! [ -f $output_folder/${2}.$3.gz ]; then
    echo "Extracting $2.$3.gz"
    zcat $output_folder/$2.url2docid.gz | awk '{print $1}'|awk -F'/' -v host=$3 '{ if($3==""host"") print "false", $0}' | gzip > $output_folder/$2.$3.gz
    zcat $output_folder/$2.remurl2docid.gz | awk '{print $1}'|awk -F'/' -v host=$3 '{ if($3==""host"") print "true", $0}' | gzip -c >> $output_folder/$2.$3.gz
    echo "Extracted data to $output_folder/$2.$3.gz"
else
    echo "Skip Extracking $2.$3.gz"
fi