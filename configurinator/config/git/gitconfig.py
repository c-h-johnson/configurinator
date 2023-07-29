from configurinator.common import group_exe
from configurinator.config import git
from configurinator.utils.config import ConfigEditor
from configurinator.utils.ui import select_exe, yesno


def run():
    with ConfigEditor(git.gitconfig_path) as cfg_edit:
        sign = yesno('Enable git signing?').result

        under = '[core]'
        cfg_edit.add(f'    editor = {select_exe(group_exe.editors.values())}', under=under)
        cfg_edit.add('    whitespace = trailing-space,space-before-tab', under=under)

        # https://git-scm.com/book/en/v2/Git-Basics-Git-Aliases
        under = '[alias]'
        cfg_edit.add('    unstage = reset HEAD --', under=under)
        # add all
        cfg_edit.add('    al = !git add . && git diff --cached', under=under)
        # push tags
        cfg_edit.add('    pt = push --tags', under=under)
        # commit with message
        cfg_edit.add('    cm = commit -m', under=under)
        # fixup last commit
        cfg_edit.add('    fixup = commit --fixup HEAD', under=under)
        # git fixup
        # git squash HEAD~[no. commits]
        cfg_edit.add('    squash = rebase --autosquash -i', under=under)

        under = '[push]'
        # automatically create branch on the remote if it does not exist (just `git push`, no arguments)
        cfg_edit.add('    autoSetupRemote = true', under=under)

        if sign:
            under = '[user]'
            cfg_edit.add('    signingkey = /home/<USER>/.ssh/id_ed25519.pub', under=under)
            under = '[gpg]'
            cfg_edit.add('    format = ssh', under=under)
            under = '[commit]'
            cfg_edit.add('    gpgsign = true', under=under)
            under = '[tag]'
            cfg_edit.add('    gpgsign = true', under=under)


if __name__ == '__main__':
    run()
