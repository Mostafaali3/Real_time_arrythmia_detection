import os
import shutil


def repeat_data(input_file, output_file, repeat_count=2):
    """
    Repeat the data from an input file multiple times.

    Parameters:
    -----------
    input_file : str
        Path to the input file containing numerical data
    output_file : str
        Path to save the repeated data file
    repeat_count : int, optional
        Number of times to repeat the original data (default is 2)

    Returns:
    --------
    None
        Writes repeated data to the output file
    """
    # Read the input file
    try:
        with open(input_file, 'r') as f:
            # Read all lines
            data = f.readlines()
    except Exception as e:
        print(f"Error reading input file {input_file}: {e}")
        return False

    # Write repeated data to output file
    try:
        with open(output_file, 'w') as f:
            for _ in range(repeat_count):
                f.writelines(data)

        print(f"Processed {input_file}:")
        print(f"  Original data points: {len(data)}")
        print(f"  Total data points after repetition: {len(data) * repeat_count}")
        return True
    except Exception as e:
        print(f"Error writing to output file {output_file}: {e}")
        return False


def process_directory(input_dir, output_dir, repeat_count=2, file_pattern='*.txt'):
    """
    Process all files in a directory that match a given pattern.

    Parameters:
    -----------
    input_dir : str
        Path to the input directory containing files to process
    output_dir : str
        Path to the output directory to save repeated data files
    repeat_count : int, optional
        Number of times to repeat the original data (default is 2)
    file_pattern : str, optional
        File pattern to match (default is '*.txt')

    Returns:
    --------
    None
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Import glob for file pattern matching
    import glob

    # Find all files matching the pattern
    input_files = glob.glob(os.path.join(input_dir, file_pattern))

    if not input_files:
        print(f"No files found in {input_dir} matching pattern {file_pattern}")
        return

    # Process each file
    successful_files = 0
    total_files = len(input_files)

    for input_file in input_files:
        # Get the filename from the full path
        filename = os.path.basename(input_file)

        # Create output file path
        output_file = os.path.join(output_dir, filename)

        # Repeat the data
        if repeat_data(input_file, output_file, repeat_count):
            successful_files += 1

    # Print summary
    print("\nProcessing Summary:")
    print(f"Total files processed: {total_files}")
    print(f"Successful files: {successful_files}")
    print(f"Output directory: {output_dir}")


def main():
    # Example usage
    input_directory = './data'  # Current directory, change as needed
    output_directory = './repeated_data'  # Output directory

    # Repeat data 2 times for all .txt files
    process_directory(input_directory, output_directory, repeat_count=10, file_pattern='*.txt')

    # Optional: Different repeat counts or file patterns
    # process_directory(input_directory, './repeated_data_x4', repeat_count=4, file_pattern='10*.txt')


if __name__ == "__main__":
    main()