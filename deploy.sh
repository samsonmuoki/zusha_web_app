#!/bin/sh

ssh zusha.duckdns.org <<EOF
  cd project
  git pull
  source venv/bin/activate
  pip install -r /home/project/requirement/requirements_main.txt
  cd /home/project/zusha/
  ./manage.py migrate
  # sudo supervisorctl restart djtrump
  exit
EOF
