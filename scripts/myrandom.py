import numpy as np
import argparse

def take_random_lines(input_file, output_file, percentage=10):
    # Read all lines from the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Calculate the number of lines to sample
    num_lines_to_sample = int(len(lines) * (percentage / 100))

    # Randomly sample the lines using numpy
    sampled_lines = np.random.choice(lines, num_lines_to_sample, replace=False)

    # Write the sampled lines to the output file
    with open(output_file, 'w') as file:
        file.writelines(sampled_lines)

def main():
    parser = argparse.ArgumentParser(description="Take a random sample of lines from a file.")
    parser.add_argument('input_file', type=str, help='The input file path')
    parser.add_argument('output_file', type=str, help='The output file path')
    parser.add_argument('--percentage', type=float, default=10, help='Percentage of lines to sample (default is 10%)')

    args = parser.parse_args()

    take_random_lines(args.input_file, args.output_file, args.percentage)

if __name__ == "__main__":
    main()
