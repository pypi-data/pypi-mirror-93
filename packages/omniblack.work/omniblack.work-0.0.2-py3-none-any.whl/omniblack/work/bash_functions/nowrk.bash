nowrk () {
    if [[ -n "$WRK_ENV" ]]
    then
        prefix="$( wrk_config prefix )"

        if [[ -f "$SRC/devtools/nowrk.ext" ]]
        then
            source "$SRC/devtools/nowrk.ext";
        fi
        if [[ -n "$OLD_LOC" ]]
        then
            cd "$OLD_LOC";
        fi

        path_del "$SRC/devtools/bin";

        unset OLD_LOC WRK_ENV SRC
    fi
}
export -f nowrk
