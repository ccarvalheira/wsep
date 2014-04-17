#!/bin/bash
cd /home/ubuntu/wsep/wsep
. ../env/bin/activate
cat << EOF | python manage.py flush
yes
EOF

cat << EOF | python manage.py syncdb
no
EOF

#python manage.py syncdb --database=triple
python manage.py migrate
#python manage.py loaddata initial_data.json

cat << EOF | ~/cassandra/bin/cqlsh 192.168.186.192
use ws;drop table tsstore; create table tsstore (bucket text, dataset bigint, time text, primary key(bucket, dataset, time));
EOF

cd /home/ubuntu/ws_client
. env/bin/activate
cd ws_client
python cli.py
