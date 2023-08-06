wrk () {
    if [[ -n "$WRK_ENV" ]]
    then
        nowrk
    fi

    prefix="$(wrk_config prefix)"
    if [[ -d "$prefix/$1/" ]]
    then

        export SRC="$prefix/$1"

        export OLD_LOC="$(pwd)";
        cd "$SRC";

        if [[ -f "$prefix/$1/devtools/wrk.ext" ]]
        then
            source "$SRC/devtools/wrk.ext";
        fi
        path_prepend "$SRC/devtools/bin";

        export WRK_ENV="$1"

    else
        echo "$1 not found in $prefix";
        return 1
    fi
}

export -f wrk
