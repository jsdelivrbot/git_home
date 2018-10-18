" All system-wide defaults are set in $VIMRUNTIME/debian.vim and sourced by
" the call to :runtime you can find below.  If you wish to change any of those
" settings, you should do it in this file (/etc/vim/vimrc), since debian.vim
" will be overwritten everytime an upgrade of the vim packages is performed.
" It is recommended to make changes after sourcing debian.vim since it alters
" the value of the 'compatible' option.

" This line should not be removed as it ensures that various options are
" properly set to work with the Vim-related packages available in Debian.
runtime! debian.vim

" Uncomment the next line to make Vim more Vi-compatible
" NOTE: debian.vim sets 'nocompatible'.  Setting 'compatible' changes numerous
" options, so any other options should be set AFTER setting 'compatible'.
"set compatible

" Vim5 and later versions support syntax highlighting. Uncommenting the next
" line enables syntax highlighting by default.
if has("syntax")
  syntax on
endif

" If using a dark background within the editing area and syntax highlighting
" turn on this option as well
"set background=dark

" Uncomment the following to have Vim jump to the last position when
" reopening a file
"if has("autocmd")
"  au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
"endif

" Uncomment the following to have Vim load indentation rules and plugins
" according to the detected filetype.
"if has("autocmd")
"  filetype plugin indent on
"endif

" The following are commented out as they cause vim to behave a lot
" differently from regular Vi. They are highly recommended though.
set showcmd   " Show (partial) command in status line.
set showmatch   " Show matching brackets.
set ignorecase    " Do case insensitive matching
"set smartcase    " Do smart case matching
set incsearch   " Incremental search
set hlsearch
"set autowrite    " Automatically save before commands like :next and :make
"set hidden   " Hide buffers when they are abandoned
"set mouse=a   " Enable mouse usage (all modes)
set mouse=  " Disable mouse
set number
set t_Co=256
" set shiftwidth=4
" set tabstop=4          "tab length=4
" set expandtab
" set softtabstop=4     "delete 4 spaces upon backspace
set autoindent
set t_ZH=[3m  " italic
set t_ZR=[23m " italic
set list
set listchars=eol:¬,trail:·
set tabstop=2 shiftwidth=2 expandtab "Set tab to 2 spaces and replace all tabs with space
inoremap <C-c> <Esc><Esc>
" Remove search highlighting
nnoremap <silent><C-l> :nohl<CR><C-l>

highlight LineNr cterm=None ctermfg=046 ctermbg=233
" Highlight current line number
highlight CursorLineNr cterm=bold ctermfg=Red ctermbg=233 gui=bold guifg=Red
set cursorline
" Turn off highlight current line
highlight CursorLine cterm=none gui=none

" Enable PostgreSQL syntax highlighting
autocmd BufRead,BufNewFile *.psql set filetype=psql
autocmd BufRead,BufNewFile *.java set filetype=java
autocmd BufRead,BufNewFile *.scala set filetype=scala
autocmd BufRead,BufNewFile *.go set filetype=go

highlight Statement ctermfg=002 cterm=italic,bold
highlight Include ctermfg=002 cterm=italic,bold
highlight Comment ctermfg=062 cterm=italic
highlight Function ctermfg=012 cterm=bold
highlight String ctermfg=135 cterm=italic
highlight Number ctermfg=208
highlight StorageClass ctermfg=161 cterm=bold
highlight TypeDef ctermfg=166 cterm=italic,bold
highlight Type ctermfg=034 cterm=bold
set colorcolumn=80
highlight ColorColumn ctermbg=10
" For Python
highlight pythonStatement ctermfg=002 cterm=italic,bold
highlight pythonLambda ctermfg=003
highlight pythonEndOfFunction ctermfg=178 cterm=bold
highlight pythonContext ctermfg=010
" For Java
highlight JavaC ctermfg=027 cterm=italic
highlight JavaBuiltinMethod ctermfg=126 cterm=italic
highlight JavaBuiltinContainer ctermfg=93 cterm=bold
" For Go
highlight goBuiltins ctermfg=39 cterm=italic
highlight goRepeat ctermfg=3 cterm=italic,bold
highlight goType  ctermfg=012 cterm=bold
highlight goDeclaration  ctermfg=012 cterm=bold
highlight goConstants  ctermfg=039  cterm=bold
" Source a global configuration file if available
if filereadable("/etc/vim/vimrc.local")
  source /etc/vim/vimrc.local
endif
