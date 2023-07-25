import os

from config import firefox
from utils.config import ConfigEditor


def pref(id, val):
    if isinstance(val, bool):
        if val:
            val_str = 'true'
        else:
            val_str = 'false'
    elif isinstance(val, int):
        val_str = str(val)
    else:
        raise RuntimeError(f'{val} of type {type(val)} is not a valid preference value')

    return f'user_pref("{id}", {val_str});'


def run():
    with ConfigEditor(os.path.join(firefox.default, 'prefs.js'), '//') as cfg_edit:
        cfg_edit.add(pref('browser.aboutConfig.showWarning', False))

        # disable disk cache
        cfg_edit.add(pref('browser.cache.check_doc_frequency', 0))
        cfg_edit.add(pref('browser.cache.disk.capacity', 0))
        cfg_edit.add(pref('browser.cache.disk.content_type_media_limit', 0))
        cfg_edit.add(pref('browser.cache.disk.enable', False))
        cfg_edit.add(pref('browser.cache.disk.free_space_hard_limit', 0))
        cfg_edit.add(pref('browser.cache.disk.free_space_soft_limit', 0))
        cfg_edit.add(pref('browser.cache.disk.max_chunks_memory_usage', 0))
        cfg_edit.add(pref('browser.cache.disk.max_entry_size', 0))
        cfg_edit.add(pref('browser.cache.disk.max_priority_chunks_memory_usage', 0))
        cfg_edit.add(pref('browser.cache.disk.metadata_memory_limit', 0))
        cfg_edit.add(pref('browser.cache.disk.preload_chunk_count', 0))
        cfg_edit.add(pref('browser.cache.disk.smart_size.enabled', False))
        cfg_edit.add(pref('browser.cache.disk_cache_ssl', False))

        # disable offline cache
        cfg_edit.add(pref('browser.cache.offline.capacity', 0))
        cfg_edit.add(pref('browser.cache.offline.enable', False))
        cfg_edit.add(pref('browser.cache.offline.storage.enable', False))

        # disable sessionstore
        cfg_edit.add(pref('browser.sessionstore.interval', 1800000))
        cfg_edit.add(pref('browser.sessionstore.max_resumed_crashes', 0))
        cfg_edit.add(pref('browser.sessionstore.resume_from_crash', False))
        cfg_edit.add(pref('browser.sessionstore.upgradeBackup.maxUpgradeBackups', 0))

        # disable unneeded services
        cfg_edit.add(pref('extensions.pocket.enabled', False))
        cfg_edit.add(pref('services.sync.prefs.sync.browser.urlbar.suggest.history', False))

        # disable history
        cfg_edit.add(pref('places.history.enabled', False))
        cfg_edit.add(pref('privacy.history.custom', True))

        # urlbar
        cfg_edit.add(pref('browser.urlbar.maxRichResults', 1))

        # https only
        cfg_edit.add(pref('dom.security.https_only_mode', True))
        cfg_edit.add(pref('dom.security.https_only_mode_ever_enabled', True))
        cfg_edit.add(pref('dom.security.https_only_mode_ever_enabled_pbm', True))
        cfg_edit.add(pref('services.sync.prefs.sync-seen.dom.security.https_only_mode', True))
        cfg_edit.add(pref('services.sync.prefs.sync-seen.dom.security.https_only_mode_ever_enabled', True))
        cfg_edit.add(pref('services.sync.prefs.sync-seen.dom.security.https_only_mode_ever_enabled_pbm', True))
        cfg_edit.add(pref('services.sync.prefs.sync-seen.dom.security.https_only_mode_pbm', True))


if __name__ == '__main__':
    run()
