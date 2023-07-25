import os

from config import neovim
from utils.config import ConfigEditor
from utils.env import dotfile_path, is_exe, rm
from utils.info import Version, get_version


def _enable_lsp(cfg_edit, server, exe=None):
    if not exe:
        exe = server
    if is_exe(exe):
        cfg_edit.add(
                "lua << EOF\nrequire'lspconfig'."+server+'.setup{}\nEOF',
                under='" enable lsp',
                )


def run():
    with ConfigEditor(os.path.join(neovim.root, 'init.vim'), '" ') as cfg_edit:
        cfg_edit.add('set tabstop=4', under='" length of an actual \\t character:')
        cfg_edit.add('set softtabstop=-1', under='" length to use when editing text (eg. TAB and BS keys)\n" (0 for `tabstop`, -1 for `shiftwidth`):')
        cfg_edit.add('set shiftwidth=0', under='" length to use when shifting text (eg. <<, >> and == commands)\n" (0 for `tabstop`):')
        cfg_edit.add('set shiftround', under='" round indentation to multiples of `shiftwidth` when shifting text\n" (so that it behaves like Ctrl-D / Ctrl-T):')

        cfg_edit.add('set expandtab', under='" if set, only insert spaces; otherwise insert \\t and complete with spaces:')

        cfg_edit.add('set autoindent', under='" reproduce the indentation of the previous line:')
        cfg_edit.add('set smartindent', under='" try to be smart (increase the indenting level after `{`, decrease it after `}`, and so on):')
        cfg_edit.add('filetype plugin indent on', under='" use language-specific plugins for indenting (better):')

        under = '" reduce disk writes'
        cfg_edit.add('set noswapfile', under=under)
        rm(dotfile_path('.local/share/nvim/swap'))

        cfg_edit.add('let g:netrw_dirhistmax=0', under=under)  # disable dir history
        rm(dotfile_path('.local/share/nvim/.netrwhist'))

        lsp_1 = """\
lua << EOF
local nvim_lsp = require('lspconfig')

-- Use an on_attach function to only map the following keys
-- after the language server attaches to the current buffer
local on_attach = function(client, bufnr)
  local function buf_set_keymap(...) vim.api.nvim_buf_set_keymap(bufnr, ...) end
  local function buf_set_option(...) vim.api.nvim_buf_set_option(bufnr, ...) end

  --Enable completion triggered by <c-x><c-o>
  buf_set_option('omnifunc', 'v:lua.vim.lsp.omnifunc')

  -- Mappings.
  local opts = { noremap=true, silent=true }

  -- See `:help vim.lsp.*` for documentation on any of the below functions
  buf_set_keymap('n', 'gD', '<Cmd>lua vim.lsp.buf.declaration()<CR>', opts)
  buf_set_keymap('n', 'gd', '<Cmd>lua vim.lsp.buf.definition()<CR>', opts)
  buf_set_keymap('n', 'K', '<Cmd>lua vim.lsp.buf.hover()<CR>', opts)
  buf_set_keymap('n', 'gi', '<cmd>lua vim.lsp.buf.implementation()<CR>', opts)
  buf_set_keymap('n', '<C-k>', '<cmd>lua vim.lsp.buf.signature_help()<CR>', opts)
  buf_set_keymap('n', '<space>wa', '<cmd>lua vim.lsp.buf.add_workspace_folder()<CR>', opts)
  buf_set_keymap('n', '<space>wr', '<cmd>lua vim.lsp.buf.remove_workspace_folder()<CR>', opts)
  buf_set_keymap('n', '<space>wl', '<cmd>lua print(vim.inspect(vim.lsp.buf.list_workspace_folders()))<CR>', opts)
  buf_set_keymap('n', '<space>D', '<cmd>lua vim.lsp.buf.type_definition()<CR>', opts)
  buf_set_keymap('n', '<space>rn', '<cmd>lua vim.lsp.buf.rename()<CR>', opts)
  buf_set_keymap('n', '<space>ca', '<cmd>lua vim.lsp.buf.code_action()<CR>', opts)
  buf_set_keymap('n', 'gr', '<cmd>lua vim.lsp.buf.references()<CR>', opts)
  buf_set_keymap('n', '<space>e', '<cmd>lua vim.lsp.diagnostic.show_line_diagnostics()<CR>', opts)
  buf_set_keymap('n', '[d', '<cmd>lua vim.lsp.diagnostic.goto_prev()<CR>', opts)
  buf_set_keymap('n', ']d', '<cmd>lua vim.lsp.diagnostic.goto_next()<CR>', opts)
  buf_set_keymap('n', '<space>q', '<cmd>lua vim.lsp.diagnostic.set_loclist()<CR>', opts)
  buf_set_keymap("n", "<space>f", "<cmd>lua vim.lsp.buf.formatting()<CR>", opts)

end

-- Use a loop to conveniently call 'setup' on multiple servers and
-- map buffer local keybindings when the language server attaches"""

        servers = []
        server_test = {
                'ccls': 'ccls',
                'pylsp': 'pylsp',
                'rust-analyzer': 'rust_analyzer',
                }
        for exe, server in server_test.items():
            if is_exe(exe):
                servers.append("'"+server+"'")

        lsp_2 = 'local servers = { ' + ', '.join(servers) + ' }'

        lsp_3 = """\
for _, lsp in ipairs(servers) do
  nvim_lsp[lsp].setup {
    on_attach = on_attach,
    flags = {
      debounce_text_changes = 150,
    }
  }
end
EOF"""

        if get_version('nvim') >= Version(0, 5, 0):
            # enable language servers
            cfg_edit.add(lsp_1, under='" enable lsp')
            cfg_edit.add(lsp_2, under=lsp_1)
            cfg_edit.add(lsp_3, under=lsp_2)


if __name__ == '__main__':
    run()
