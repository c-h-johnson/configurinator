import os

from configurinator.utils.env import dotfile_path, is_exe


def test_dotfile_path():
    user = os.getlogin()

    fname = '.test'
    assert dotfile_path(fname) == f'/home/{user}/{fname}'

    fname = '.testdir/test'
    assert dotfile_path(fname) == f'/home/{user}/{fname}'

def test_is_exe():
    assert is_exe('python')
    assert not is_exe('hkjsdhfakhdkfhakhdflhsadkflhhsdfksdjf')
