# url-remove-prediction
a simple decision tree to predict which urls are likely removed

# idea
removed urls are ussually have the same url's components:
- same host
- same path
- same query
- same parameter

by using a decision tree, we suppose we can predict if a url will be removed by main-content-filter or not

# dependencies

python3, sklearn, numpy, pandas

`sudo apt install python3 python3-pip`

`python3-pip install numpy pandas sklearn --user`

# prepare data

```
# example of getting data for bucket 19 (planner1v, indexer2v), which contains www.lazada.vn
# getting removed-url-by-mcf from planner
scp planner1v:/itim/planner/data/storage/current/19/urlremovedbymaincontentfilter.gz /tmp
# or getting removed-url-by-other-magic from indexer
scp indexer2v:/var/itim/indexer/19_next/common/remurl2docid.gz /tmp
# getting indexed-url from indexer
scp indexer2v:/var/itim/indexer/19_next/common/url2docid.gz /tmp

# combine downloaded resources to one file
zcat /tmp/urlremovedbymaincontentfilter.gz | awk '{print "true",$1}'|gzip > /tmp/removed.gz
zcat /tmp/url2docid.gz | awk '{print "false",$1}'|gzip > /tmp/not_removed.gz
zcat /tmp/removed.gz /tmp/not_removed.gz |gzip > data/19.gz

# transform urls to features
python3 prepare_data.py data/19.gz data/19-feature.gz
```

# simple usage 

`python3 tree.py <feature_files> [prediction_output_file]`
