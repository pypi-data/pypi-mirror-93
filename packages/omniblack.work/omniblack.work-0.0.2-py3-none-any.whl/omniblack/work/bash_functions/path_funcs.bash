# Functions for bash to help with path manipulation

# We only support bash
if [ -z "$BASH_VERSION" ]; then
    return 1
fi

# path_contains, path_append, and path_prepend are from:
#       Simon J. Gerraty <sjg@zen.void.oz.au>
#
#       @(#)Copyright (c) 1991 Simon J. Gerraty
#
#       This file is provided in the hope that it will
#       be of use.  There is absolutely NO WARRANTY.
#       Permission to copy, redistribute or otherwise
#       use this file is hereby granted provided that
#       the above copyright notice and this notice are
#       left intact.

# Modified by Datatrac

# true if $1 found in $2 (or PATH) ?
path_contains() {
    local pth=${2:-PATH}
    local tmp=${!pth}
    case ":$tmp:" in
        *:$1:*)
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}
export -f path_contains

# if $1 exists and is not in path, append it
path_append () {
    path_contains "$@" && return 0
    local pth=${2:-PATH}
    local tmp=${!pth}:${1}
    tmp=${tmp#:}            # drop any leading : (if path was empty)
    eval ${2:-PATH}="$tmp"
    echo "${2:-PATH} += ${1}"
}
export -f path_append

# if $1 exists and is not in path, prepend it
path_prepend () {
    path_contains "$@" && return 0
    local pth=${2:-PATH}
    local tmp=${1}:${!pth}
    tmp=${tmp%:}            # drop any trailing : (if path was empty)
    eval ${2:-PATH}="$tmp"
    echo "${2:-PATH} += ${1}"

    hash -r                 # some commands could be different now
}
export -f path_prepend

# if $1 is in path, remove it
path_del () {
    path_contains "$@" || return 0

    local rem=$1
    local pth=${2:-PATH}
    local tmp=:${!pth}:     # make sure there are delims at the begin/end
    tmp=${tmp/:$rem:/:}     # remove the specified element
    tmp=${tmp%:}            # drop the trailing :
    tmp=${tmp#:}            # drop the leading :
    eval ${2:-PATH}="$tmp"
    echo "${2:-PATH} -= ${1}"

    hash -r                 # some commands could be not found now
}
export -f path_del

