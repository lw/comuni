./osmosis-*/bin/osmosis \
  --read-pbf emilia-romagna.pbf \
  --tag-filter accept-relations boundary=administrative \
  --tag-filter accept-ways boundary=administrative \
  --write-xml output2.osm.bz2

./osmosis-*/bin/osmosis \
  --read-pbf emilia-romagna.pbf \
  --tag-filter accept-relations type=boundary \
  --tag-filter accept-relations boundary=administrative \
  --used-way \
  --used-node outPipe.0=rels \
  \
  --read-pbf emilia-romagna.pbf \
  --tag-filter accept-ways boundary=administrative \
  --used-node outPipe.0=ways \
  \
  --merge inPipe.0=rels inPipe.1=ways \
  --write-xml output.osm.bz2
