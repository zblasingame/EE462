#!/bin/bash

dir=$1
temp=$2

in_dir="$dir/sub"
out_dir="$dir/fdbck"

# Loop through directories
for f in $in_dir/*
do
	filename=$(echo "$f" | sed -E 's/.*\/([[:alpha:]].*$)/\1/g')

	new_filename=$filename
	new_filename+='feedback'

	cat "$temp" > "$out_dir/$new_filename"
done
