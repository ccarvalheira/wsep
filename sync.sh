#!/bin/bash
rm ../wsep.db
python manage.py syncdb
python manage.py syncdb --database=triple
python manage.py migrate
