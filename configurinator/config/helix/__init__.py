from config.helix import cache, config_toml, share


def run():
    if share.supported:
        config_toml.run()
        if '--log' not in share.CMD_ARGS:
            cache.run()
