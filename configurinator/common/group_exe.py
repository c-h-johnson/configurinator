from config import helix

from common import Exe

# ordered descending
editors = {
    'hx': Exe('hx', *helix.share.CMD_ARGS),  # helix
    'helix': Exe('helix', *helix.share.CMD_ARGS),  # some distrobutions such as arch linux rename hx to helix
    'kak': Exe('kak'),  # kakoune
    'nvim': Exe('nvim', '-i', 'NONE'),  # neovim
    'vim': Exe('vim'),
    'emacs': Exe('emacs'),
    'vi': Exe('vi'),
    'nano': Exe('nano'),
}
