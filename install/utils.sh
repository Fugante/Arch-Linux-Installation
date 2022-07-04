select_option()
{
    # $1: string containing the possible choices
    # $2: Text to show until a valid option is chosen

    OPTION=""
    while [[ ! *"$OPTION"* =~ [$1] ]]
    do
        echo $2
        read OPTION
    done
    echo $OPTION
}

select_option1()
{
    option
    while $
    do
        echo $
}