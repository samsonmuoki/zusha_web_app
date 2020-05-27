from fabric.api import local


def deploy():
    local('ansible-playbook initialization_playbook.yml -i hosts.yml')
    local('ansible-playbook nginx_playbook.yml -i hosts.yml')
    local('ansible-playbook gunicorn_playbook.yml -i hosts.yml')
    local('ansible-playbook letsencrypt_playbook.yml -i hosts.yml')


def ci_cd():
    local('ansible-playbook cd_playbook.yml -i hosts.yml')


def periodic_tasks():
    local('ansible-playbook periodic_tasks_playbook.yml -i hosts.yml')
