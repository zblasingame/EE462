#!/bin/bash

dir=$1
output_file="$dir/grades"

touch "$output_file"

OLDIFS=$IFS

# empty file
> "$output_file"

# Loop through directories
for f in $dir/fdbck/*
do
	scores=($(grep '^[[:space:]]score:' "$f" | sed 's/^[^-0-9]*\([-0-9.]\+\).*$/\1/'))

	IFS='+' # change Internal Field Seperator
	total_score=$(echo "scale=1;${scores[*]}" | bc)
	IFS=$OLDIFS # change it back

	filename=$(echo "$f" | sed -E 's/.*\/([[:alpha:]].*$)/\1/g')

	if [ "$filename" != "$output_file" ]
	then
		echo "$filename, $total_score" >> "$output_file" 

		if ! grep -q "Total_score" "$f"
		then
			printf "\nTotal_score: %f out of %f" "$total_score" "$2" >> "$f"
		fi
	fi
done
