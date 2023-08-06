#! /usr/bin/zsh

# Functions for bash to help with path manipulation



source "$( wrk_file bash_functions/path_funcs.bash )"
source "$( wrk_file bash_functions/nowrk.bash )"
source "$( wrk_file bash_functions/wrk.bash )"

eval "$(register-python-argcomplete mkwrk)"
eval "$(register-python-argcomplete rmwrk)"
