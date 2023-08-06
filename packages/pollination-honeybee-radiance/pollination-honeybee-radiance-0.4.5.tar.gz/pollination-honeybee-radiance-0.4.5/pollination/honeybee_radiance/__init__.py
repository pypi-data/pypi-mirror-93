"""Honeybee Radiance plugin for Pollination."""
from pollination_dsl.package import get_requirement_version

# set the version for docker image dynamically based on honeybee-radiance version
# in dependencies
image_version = get_requirement_version(__package__, 'honeybee-radiance')
image_id = f'ladybugtools/honeybee-radiance:{image_version}'

__pollination__ = {
    'app_version': '5.4',  # optional - tag for version of Radiance
    'config': {
        'docker': {
            'image': image_id,
            'workdir': '/home/ladybugbot/run'
        }
    }
}
