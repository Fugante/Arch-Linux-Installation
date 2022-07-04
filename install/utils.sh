is_valid_option()
{
    # Use a regex expresion to validate if string 1 is within string 2

    [[ $1 =~ [$2] ]]
}

file_exists()
{
    # Check if filename $1 exists

    [[ -f $1 ]]
}

disk_exists()
{
    # Check if disk $1 exists

    lsblk $1 >&2
}

select_option()
{
    # $1: Text to prompt to the user
    # $2: Function to validate input
    # $3-$n: Paramenters passed to the validation function

    while :
    do
        echo "$1" >&2
        read option

        "$2" $option "${@:3}" && break
    done
    echo $option
}