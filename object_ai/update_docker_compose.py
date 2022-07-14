import sys
import yaml
import re

from object_ai.paths import PACKAGE_ROOT

def update_docker_compose(path, git_hash):
    with open(path) as f:
        compose = yaml.safe_load(f)
    old_image = compose['services']['web']['image']
    new_image = re.sub(':.+$', f':{git_hash}', old_image)
    compose['services']['web']['image'] = new_image

    with open(path, 'w') as f:
        yaml.safe_dump(compose, f)

git_hash = sys.argv[1]
path = PACKAGE_ROOT.joinpath('docker-compose.yml')
print('Updating docker-compose.yml with new image tag...')
update_docker_compose(path, git_hash)

