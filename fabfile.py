from fabric.api import *

def deploy():
    local('ansible-playbook ansible_playbooks/initialization_playbook.yml -i hosts.yml')
    local('ansible-playbook ansible_playbooks/nginx_playbook.yml -i hosts.yml')
    local('ansible-playbook ansible_playbooks/gunicorn_playbook.yml -i hosts.yml')
    local('ansible-playbook ansible_playbooks/letsencrypt_playbook.yml -i hosts.yml')
