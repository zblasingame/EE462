#!/bin/bash

num_questions=$1
output_file=$2
default_score=$3

> "$output_file"

for (( i = 1; i <= num_questions; i++ ))
do
	{
		echo "Q$i"
		echo -e "\tscore: $default_score"
		echo -e "\tcomments:"	
	} >> "$output_file"

done

echo -e "\nother\n\tscore: 0\n\tcomments:" >> "$output_file"
