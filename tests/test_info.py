import sys

from configurinator.utils.info import Version, get_version


def test_version_str():
    original = '0.0.0'
    version = Version().init_str(original)
    assert version == Version(0, 0, 0)
    assert str(version) == original

    assert Version(delimiter='-').init_str('0-0-0') == Version(0, 0, 0)


def test_version_compare():
    assert Version(1, 0, 0) > Version(0, 0, 0)
    assert Version(0, 1, 0) > Version(0, 0, 0)
    assert Version(0, 0, 1) > Version(0, 0, 0)
    assert Version(1, 0, 0) >= Version(0, 0, 0)
    assert Version(0, 1, 0) >= Version(0, 0, 0)
    assert Version(0, 0, 1) >= Version(0, 0, 0)
    assert Version(0, 0, 0) >= Version(0, 0, 0)

    assert not Version(1, 0, 0) < Version(0, 0, 0)
    assert not Version(0, 1, 0) < Version(0, 0, 0)
    assert not Version(0, 0, 1) < Version(0, 0, 0)
    assert not Version(1, 0, 0) <= Version(0, 0, 0)
    assert not Version(0, 1, 0) <= Version(0, 0, 0)
    assert not Version(0, 0, 1) <= Version(0, 0, 0)

    assert Version(0, 0, 0) < Version(1, 0, 0)
    assert Version(0, 0, 0) < Version(0, 1, 0)
    assert Version(0, 0, 0) < Version(0, 0, 1)
    assert Version(0, 0, 0) <= Version(1, 0, 0)
    assert Version(0, 0, 0) <= Version(0, 1, 0)
    assert Version(0, 0, 0) <= Version(0, 0, 1)
    assert Version(0, 0, 0) <= Version(0, 0, 0)

    assert not Version(0, 0, 0) > Version(1, 0, 0)
    assert not Version(0, 0, 0) > Version(0, 1, 0)
    assert not Version(0, 0, 0) > Version(0, 0, 1)
    assert not Version(0, 0, 0) >= Version(1, 0, 0)
    assert not Version(0, 0, 0) >= Version(0, 1, 0)
    assert not Version(0, 0, 0) >= Version(0, 0, 1)

    assert Version(0, 0, 0) == Version(0, 0, 0)
    assert Version(1, 0, 0) != Version(0, 0, 0)

    assert Version(1, 0, 0) != Version(0, 0, 0)
    assert Version(0, 0, 0) == Version(0, 0, 0)

    assert Version(1, 1) < Version(2, 0)
    assert Version(1, 1) <= Version(2, 0)

    assert Version(2, 0) > Version(1, 1)
    assert Version(2, 0) >= Version(1, 1)

    assert None < Version(0, 1)
    assert None < Version(0, 0)

    assert Version(0, 1) > None
    assert Version(0, 0) > None


def test_get_version():
    py_v = sys.version_info
    assert get_version('python') == Version(py_v.major, py_v.minor, py_v.micro)
