#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
PS1='[\u@\h \W]\$ '

# # Haskell Initialization
# [ -f "/home/langtano/.ghcup/env" ] && source "/home/langtano/.ghcup/env" # ghcup-env

## Python pyenv
# export PYENV_ROOT="$HOME/.local/share/pyenv"
# command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
# eval "$(pyenv init -)"
# eval "$(pyenv virtualenv-init -)"

# Start Graphical Interface
if [ $TERM == linux ]
then
    startx
fi

# # Node Version Manager
# export NVM_DIR="$HOME/.local/share/nvm"
# [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
# [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion