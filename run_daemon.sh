#!/bin/bash
apt-get update
apt-get install -y python-dev libldap2-dev libsasl2-dev libssl-dev
pip install python-ldap
python /app/nginx-ldap-auth-daemon.py

