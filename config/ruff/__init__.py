from utils.config import ConfigEditor
from utils.env import dotfile_path

config_path = dotfile_path('.config/ruff/pyproject.toml')


def run():
    with ConfigEditor(config_path) as cfg_edit:
        section = '[tool.ruff]'

        cfg_edit.add('select = ["A", "AIR", "ANN", "ARG", "ASYNC", "B", "BLE", "C4", "C90", "COM", "D", "DJ", "DTZ", "E", "EM", "ERA", "F", "FLY", "G", "I", "ICN", "INP", "ISC", "N", "NPY", "PD", "PERF", "PGH", "PIE", "PL", "PT", "PYI", "Q", "RET", "RSE", "RUF", "SIM", "SLF", "SLOT", "T10", "TID", "TRY", "UP", "W", "YTT"]', under=section)

        cfg_edit.add('cache-dir = "/tmp/.ruff_cache"', under=section)

        comment = '# ignore line too long'
        cfg_edit.add(comment, under=section)
        cfg_edit.add('ignore = ["E501"]', under=comment)

        cfg_edit.add('ignore-init-module-imports = true', under=section)

        section = '[tool.ruff.flake8-quotes]'

        cfg_edit.add('inline-quotes = "single"', under=section)
