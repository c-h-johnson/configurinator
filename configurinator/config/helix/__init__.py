from config.helix import cache, share, config_toml


def run():
    if share.supported:
        config_toml.run()
        if '--log' not in share.CMD_ARGS:
            cache.run()
