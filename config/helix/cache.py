import os
import platform

from config.helix import share
from utils.env import ln

log = 'helix.log'


def run():
    if platform.system() in ['Linux', 'Darwin']:
        ln(
            os.path.join('/tmp', log),
            os.path.join(share.cache_dir, log),
        )
    else:
        print('moving helix.log not supported on this operating system')


if __name__ == '__main__':
    run()
