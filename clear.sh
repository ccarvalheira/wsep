#!/bin/bash
cd /home/ubuntu/wsep/wsep
. ../env/bin/activate
rm ../wsep.db

cat << EOF | python manage.py syncdb
no
EOF

python manage.py syncdb --database=triple
python manage.py migrate
#python manage.py loaddata initial_data.json

cat << EOF | ~/cassandra/bin/cqlsh 192.168.186.192
use ws;drop table tsstore; create table tsstore (bucket text, dataset bigint, time text, primary key(bucket, dataset, time));
EOF

cat << EOF | python manage.py dbshell
insert into dataviewer_dimension (description, datatype, ts_column, name, units) values ('asd','array','time','time','sec');
EOF

cd /home/ubuntu/ws_client
. env/bin/activate
cd ws_client
python initter.py

