import os
from collections import namedtuple

from common import File, RemoteBundleList, UrlResource, group_url
from utils.env import dotfile_path


def browse(f_list: dict | list) -> File | None:
    directory = isinstance(f_list, dict)
    opts = f_list.keys() if directory else [f.name for f in f_list]

    while True:
        selection = select(*opts, back=True)
        if not selection:
            return None
        if directory:
            sub = browse(f_list[selection])
            if sub:
                return sub
            continue
        for f in f_list:
            if f.name == selection:
                return f


def get_bg(default_files: list[str] = []) -> File:
    base_opts = [
                'select from database of online backgrounds',
                'manually input url',
                'input path of local file',
                ]
    if default_files:
        base_opts.append('select from default backgrounds provided by the window manager')
    while True:
        print('Where to find background?')
        src = select(*base_opts)
        idx = base_opts.index(src)
        if idx in range(2):
            if idx == 0:
                f = browse(group_url.wallpapers)
            else:  # idx == 1
                f_url = input('url (enter to go back): ')
                if not f_url:
                    continue
                f_name = input_with_default('filename', default=os.path.basename(f_url))
                f = UrlResource(url=f_url, name=f_name)

            if not f:
                continue
            return f.download(dotfile_path('Pictures/Wallpapers'))
        if idx in range(2, 4):
            if idx == 2:
                path = input('local path (enter to go back): ')
            else:  # idx == 3
                path = select(*default_files, back=True)
            if not path:
                continue
            return File(path=path)


def select_exe(exes) -> str:
    for i in exes:
        if i.exists:
            print(f'selecting {i.name} as editor')
            return i.command
    print(f'could not find any of {[i.name for i in exes]} on $PATH')

    return input('enter command to use instead: ')


def input_with_default(prompt, default):
    response = input(f'{prompt} (press enter for default "{default}"): ')
    if not response:
        response = default
    return response


def select(
    *options: list[str],
    none: bool = False,
    back: bool = False,
    default: str = '',
) -> str:
    options = list(options)
    if none:
        options.insert(0, None)
    if back:
        options.append('[go back]')
    while True:
        print('select from the following list:')
        for i, opt in enumerate(options):
            print(f'{i} - {opt}')

        prompt = f'0-{len(options)-1}'
        if default:
            prompt += f' (default {default})'
        prompt += ': '
        selection = input(prompt)

        if selection == '' and default:
            print(f'selecting default option {default}')
            return default
        try:
            result = options[int(selection)]
            print(f'selecting option {selection}: {result}')
        except ValueError:
            if selection in options:
                result = selection
            else:
                print(f'Invalid option {selection}')
                continue
        except IndexError:
            print(f'{selection} out of range')
            continue

        if result == '[go back]':
            return ''
        return result


YesNoResult = namedtuple('YesNoResult', ['result', 'all'], defaults=[False])


def yesno(prompt: str, repeat: bool = False) -> YesNoResult:
    options = 'y/ya/n/na' if repeat else 'y/n'
    max_len = 2 if repeat else 1
    while True:
        response = input(f'{prompt} ({options}):')

        if response[0] == 'y':
            result = YesNoResult(True)
        elif response[0] == 'n':
            result = YesNoResult(False)
        else:
            print(f'Invalid input "{response}"')
            continue

        if len(response) > max_len:
            print(f'Input "{response}" invalid: too many characters')
            continue
        if len(response) == 2 and response[1] == 'a':
            result.all = True
        elif len(response) == 2:
            print(f'Input "{response}" invalid: {response[1]} is not a valid character')
            continue

        return result


def select_remote_file(remote_bundle_list: RemoteBundleList, path: str) -> File:
    bundle_map = {f'{i} ({len(j.files)} files) ({j.resource.url})': j for i, j in remote_bundle_list.bundles.items()}
    remote_bundle = bundle_map[select(*bundle_map.keys())]
    dir_path = os.path.join(path, remote_bundle.name)
    remote_bundle.resource.download(dir_path)

    files = remote_bundle.files
    selected_file = files[0] if len(files) == 1 else select(*files)
    return File(os.path.join(dir_path, selected_file))
