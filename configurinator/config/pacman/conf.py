from configurinator.utils.config import ConfigEditor


def run():
    with ConfigEditor('/etc/pacman.conf', '# ') as cfg_edit:
        under = '[options]'
        # Comparing versions before updating
        cfg_edit.add('VerbosePkgLists', under=under)
        # Progress bar easter egg
        cfg_edit.add('ILoveCandy', under=under)
        # Faster download
        cfg_edit.add('ParallelDownloads = 5', under=under)


if __name__ == '__main__':
    run()
