from configurinator.common import Exe
from configurinator.config import helix

# ordered descending
EDITOR = {
    'hx': Exe('hx', *helix.share.CMD_ARGS),  # helix
    'helix': Exe('helix', *helix.share.CMD_ARGS),  # some distrobutions such as arch linux rename hx to helix
    'kak': Exe('kak'),  # kakoune
    'nvim': Exe('nvim', '-i', 'NONE'),  # neovim
    'vim': Exe('vim'),
    'emacs': Exe('emacs'),
    'vi': Exe('vi'),
    'nano': Exe('nano'),
}

TERMINAL = {
    'alacritty': Exe('alacritty'),
    'kitty': Exe('kitty'),
    'foot': Exe('foot'),
}
