from common import group_exe
from config import git
from utils.config import ConfigEditor
from utils.ui import select_exe


def run():
    with ConfigEditor(git.gitconfig_path) as cfg_edit:
        under = '[core]'
        cfg_edit.add(f'    editor = {select_exe(group_exe.editors.values())}', under=under)
        cfg_edit.add('    whitespace = trailing-space,space-before-tab', under=under)

        # https://git-scm.com/book/en/v2/Git-Basics-Git-Aliases
        under = '[alias]'
        cfg_edit.add('    unstage = reset HEAD --', under=under)
        # add all
        cfg_edit.add('    al = !git add . && git diff --cached', under=under)
        # commit with message
        cfg_edit.add('    cm = commit -m', under=under)
        # git commit --fixup HEAD
        # git squash HEAD~[no. commits]
        cfg_edit.add('    squash = rebase --autosquash -i', under=under)

        under = '[push]'
        # automatically create branch on the remote if it does not exist (just `git push`, no arguments)
        cfg_edit.add('    autoSetupRemote = true', under=under)


if __name__ == '__main__':
    run()
