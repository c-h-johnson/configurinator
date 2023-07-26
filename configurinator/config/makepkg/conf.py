from configurinator.utils.config import ConfigEditor


def run():
    with ConfigEditor('/etc/makepkg.conf', '# ') as cfg_edit:
        under = """#########################################################################
# EXTENSION DEFAULTS
#########################################################################
#"""
        # faster install from AUR by disabling compression
        cfg_edit.add("PKGEXT='.pkg.tar'", under=under)

if __name__ == '__main__':
    run()
