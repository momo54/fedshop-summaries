#!/bin/bash

# Directory containing the files
input_directory="dataset"
output_directory="dataset.10"
percentage=10

# Create the output directory if it doesn't exist
mkdir -p "$output_directory"

# Loop through each file in the input directory
for input_file in "$input_directory"/*.nt; do
  # Get the base name of the file (without the directory)
  filename=$(basename -- "$input_file")
  
  # Construct the output file path
  output_file="$output_directory/$filename"
  
  # Calculate the number of lines in the input file
  num_lines=$(wc -l < "$input_file")
  
  # Calculate 10% of the number of lines
  num_lines_to_sample=$(awk "BEGIN {printf \"%d\", $num_lines * $percentage / 100}")
  
  # Shuffle the lines and take the top 10%
  shuf "$input_file" | head -n "$num_lines_to_sample" > "$output_file"
  
  echo "Processed $input_file, sampled $num_lines_to_sample lines."
done
