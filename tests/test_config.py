import os
import re

import pytest
from utils.config import ConfigEditor

_cfg_file = 'test.cfg'


class TestConfig:
    __test__ = False

    def __init__(self, initial_config: str):
        self._cfg = initial_config

    def __enter__(self):
        with open(_cfg_file, 'w') as f:
            f.write(self._cfg)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        os.remove(_cfg_file)

    @property
    def cfg(self) -> str:
        return self._cfg

    def _verify_cfg_file(self, cfg: str):
        with open(_cfg_file, 'r') as f:
            assert f.read() == cfg
            f.seek(0)


heading = TestConfig(
"""
# options
a = 1
# b = 2
"""
)

regex = re.compile('a = 1')


def test_is_comment():
    test_cfgs = {
        TestConfig('# a = 1'): '#',
        TestConfig('#a = 1'): '#',
        TestConfig('//a = 1'): '//',
    }

    for test, comment_str in test_cfgs.items():
        with test as cfg_test:
            with ConfigEditor(_cfg_file, comment_str) as cfg_edit:
                assert cfg_edit._is_comment(regex.search(cfg_test.cfg).start())

    with heading as cfg_test:
        with ConfigEditor(_cfg_file) as cfg_edit:
            assert not cfg_edit._is_comment(regex.search(cfg_test.cfg).start())
            assert cfg_edit._is_comment(re.compile('b = 2').search(cfg_test.cfg).start())
            assert not cfg_edit._is_comment(-1)


def test_comment():
    test_cfgs = {
        TestConfig('a = 1'): '#',
        TestConfig('a = 1'): '//',
    }

    for test, comment_str in test_cfgs.items():
        with test as cfg_test:
            with ConfigEditor(_cfg_file, comment_str) as cfg_edit:
                cfg_edit.comment('a = 1')
            cfg_test._verify_cfg_file(comment_str + ' ' + cfg_test.cfg)

    with heading as cfg_test:
        with ConfigEditor(_cfg_file) as cfg_edit:
            cfg_edit.comment('b = 2')
        cfg_test._verify_cfg_file(cfg_test.cfg)

    with heading as cfg_test:
        with ConfigEditor(_cfg_file) as cfg_edit:
            cfg_edit.comment('a = 1')
        cfg_test._verify_cfg_file("""
# options
# a = 1
# b = 2
"""
)


def test_uncomment():
    test_cfgs = {
        TestConfig('# a = 1'): '# ',
        TestConfig('#a = 1'): '#',
        TestConfig('//a = 1'): '//',
    }

    for test, comment_str in test_cfgs.items():
        with test as cfg_test:
            with ConfigEditor(_cfg_file, comment_str) as cfg_edit:
                cfg_edit.for_each(regex, cfg_edit.uncomment)
            cfg_test._verify_cfg_file(cfg_test.cfg[len(comment_str):])

    with heading as cfg_test:
        with ConfigEditor(_cfg_file) as cfg_edit:
            cfg_edit.for_each(re.compile(r'\w = \d'), cfg_edit.uncomment)
        cfg_test._verify_cfg_file("""
# options
a = 1
b = 2
"""
)


def test_add():
    # entry already exists
    with heading as cfg_test:
        with ConfigEditor(_cfg_file) as cfg_edit:
            cfg_edit.add('a = 1')
        cfg_test._verify_cfg_file(heading.cfg)

    # entry already exists but is commented
    with heading as cfg_test:
        with ConfigEditor(_cfg_file) as cfg_edit:
            cfg_edit.add('b = 2')
        cfg_test._verify_cfg_file("""
# options
a = 1
b = 2
""")

    # entry set to different value
    with heading as cfg_test:
        with ConfigEditor(_cfg_file) as cfg_edit:
            cfg_edit.add('a = 2')
        cfg_test._verify_cfg_file("""
# options
# b = 2
a = 2
""")

    # non-existent entry
    with heading as cfg_test:
        with ConfigEditor(_cfg_file) as cfg_edit:
            cfg_edit.add('c = 3', under='# options')
        cfg_test._verify_cfg_file("""
# options
c = 3
a = 1
# b = 2
""")

    # non-existent header
    with heading as cfg_test:
        with ConfigEditor(_cfg_file) as cfg_edit:
            cfg_edit.add('c = 3', under='# nonexistent options')
        cfg_test._verify_cfg_file("""
# options
a = 1
# b = 2
# nonexistent options
c = 3
""")

    # place at top of file
    with heading as cfg_test:
        with ConfigEditor(_cfg_file) as cfg_edit:
            cfg_edit.add('c = 3', under='# nonexistent options', start=True)
        cfg_test._verify_cfg_file("""# nonexistent options
c = 3

# options
a = 1
# b = 2
""")

    # new enclosed section
    with TestConfig('a = 1\n') as cfg_test:
        with ConfigEditor(_cfg_file) as cfg_edit:
            cfg_edit.add('    b: "2"', under='enclosed section {', enclose='}')
        cfg_test._verify_cfg_file("""a = 1
enclosed section {
    b: "2"
}
""")

    # append to existing enclosed section
    with TestConfig('enclosed section {\n    a: "1"\n}\n') as cfg_test:
        with ConfigEditor(_cfg_file) as cfg_edit:
            cfg_edit.add('    b: "2"', under='enclosed section {', enclose='}')
        cfg_test._verify_cfg_file("""enclosed section {
    b: "2"
    a: "1"
}
""")


def test_add_lines():
    with heading as cfg_test:
        with ConfigEditor(_cfg_file) as cfg_edit:
            cfg_edit.add_lines(
                'a = 1',
                'b = 2',
                'c = 3',
                under='# options'
            )
        cfg_test._verify_cfg_file("""
# options
a = 1
b = 2
c = 3
""")


def test_exists():
    with heading as _:
        with ConfigEditor(_cfg_file) as cfg_edit:
            assert cfg_edit.exists('a = 1')
            assert not cfg_edit.exists('b = 2')
            assert not cfg_edit.exists('c = 3')

            assert cfg_edit.exists('a = 1', True)
            assert cfg_edit.exists('b = 2', True)
            assert cfg_edit.exists('# b = 2', True)
            assert not cfg_edit.exists('c = 3', True)

    with heading as _:
        with ConfigEditor(_cfg_file) as cfg_edit:
            with pytest.raises(KeyError):
                cfg_edit.exists('a = 1', index=0)


def test_replace():
    with heading as cfg_test:
        with ConfigEditor(_cfg_file) as cfg_edit:
            cfg_edit.replace('a = 1', 'a = 2')
        cfg_test._verify_cfg_file("""
# options
a = 2
# b = 2
"""
)

    with heading as cfg_test:
        with ConfigEditor(_cfg_file) as cfg_edit:
            cfg_edit.replace('a = 2', 'a = 3')
        cfg_test._verify_cfg_file(heading.cfg)

    with heading as cfg_test:
        with ConfigEditor(_cfg_file) as cfg_edit:
            cfg_edit.replace('', 'a = 2')
        cfg_test._verify_cfg_file(heading.cfg)

    with heading as cfg_test:
        with ConfigEditor(_cfg_file) as cfg_edit:
            with pytest.raises(KeyError):
                cfg_edit.replace('a = 1', 'a = 2', index=0)


def test_remove():
    with heading as cfg_test:
        with ConfigEditor(_cfg_file) as cfg_edit:
            cfg_edit.remove('a = 1')
        cfg_test._verify_cfg_file("""
# options
# b = 2
"""
)

    with heading as cfg_test:
        with ConfigEditor(_cfg_file) as cfg_edit:
            cfg_edit.remove('a = 2')
        cfg_test._verify_cfg_file(heading.cfg)

    with heading as cfg_test:
        with ConfigEditor(_cfg_file) as cfg_edit:
            cfg_edit.remove('')
        cfg_test._verify_cfg_file(heading.cfg)

    with heading as cfg_test:
        with ConfigEditor(_cfg_file) as cfg_edit:
            with pytest.raises(KeyError):
                cfg_edit.remove('a = 1', index=0)
