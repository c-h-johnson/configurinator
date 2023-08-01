from configurinator.config.helix import cache, config_toml, share


def run(store):
    if share.supported:
        config_toml.run(store)
        if '--log' not in share.CMD_ARGS:
            cache.run()
