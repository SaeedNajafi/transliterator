thing=$1

if [ $thing == "ace" ]; then
    echo thing was ace
else
    if [ $thing == "cool" ]; then
	echo thing was cool
    else
	echo thing was other
    fi
fi