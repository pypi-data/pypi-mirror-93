#! /usr/bin/zsh

# Functions for bash to help with path manipulation


prefix="$(wrk_config prefix)"

fpath_prepend "$(wrk_file functions)"

autoload -Uz wrk nowrk

compdef "_files -W $prefix -/" wrk

eval "$(register-python-argcomplete mkwrk)"
eval "$(register-python-argcomplete rmwrk)"
