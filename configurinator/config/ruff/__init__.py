from utils.config import ConfigEditor
from utils.env import dotfile_path

config_path = dotfile_path('.config/ruff/pyproject.toml')


def run():
    with ConfigEditor(config_path) as cfg_edit:
        section = '[tool.ruff]'

        cfg_edit.add('select = ["A", "AIR", "ANN", "ARG", "ASYNC", "B", "BLE", "C4", "COM", "D", "DJ", "DTZ", "E", "EM", "ERA", "F", "FLY", "G", "I", "ICN", "INP", "ISC", "N", "NPY", "PD", "PERF", "PGH", "PIE", "PL", "PT", "PYI", "Q", "RET", "RSE", "RUF", "SIM", "SLF", "SLOT", "T10", "TID", "TRY", "UP", "W", "YTT"]', under=section)

        cfg_edit.add('cache-dir = "/tmp/.ruff_cache"', under=section)

        cfg_edit.add('ignore = ["ANN00", "ANN10", "ANN201", "ANN204", "D10", "E501"]', under=section)

        cfg_edit.add('ignore-init-module-imports = true', under=section)

        section = '[tool.ruff.flake8-quotes]'

        cfg_edit.add('inline-quotes = "single"', under=section)
