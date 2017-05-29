import yaml
import os
from django.conf import settings

env_entry = 'docker_compose'

def pre_start(env):
    os.makedirs(settings.DOCKER_COMPOSE_DIR, exist_ok=True)
    env[env_entry] = {
        'version': '3',
        'services': {},
    }

def post_start(env):
    with open(
        os.path.join(settings.DOCKER_COMPOSE_DIR, 'docker-compose.yml'),
        'w'
    ) as docker_compose_file:
        yaml.dump(env[env_entry], docker_compose_file, default_flow_style=False)
    del env[env_entry]
