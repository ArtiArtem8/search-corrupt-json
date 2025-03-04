# Corrupted File Checker Script

This script checks for corrupted files in a specified directory and its subdirectories. It supports checking for corrupted JSON files and files filled with null bytes.

## Features

- Checks for corrupted JSON files by attempting to parse them.
- Checks for files filled with null bytes.
- Supports checking all files or only JSON files.
- Provides a progress bar to track the checking process.
- Supports verbose mode to print detailed results.

## Usage

To use this script, simply run it from the command line and provide the path to the directory you want to check. You can also use the `--all` flag to check all files (not just JSON files) and the `--verbose` flag to print detailed results.

### Running the Script

- **Check for corrupted files in the current directory:**

  ```bash
  python corrupted_file_checker.py
  ```

- **Check for corrupted files in a specific directory:**

  ```bash
  python corrupted_file_checker.py /path/to/directory
  ```

- **Check all files (not just JSON files):**

  ```bash
  python corrupted_file_checker.py /path/to/directory --all
  ```

- **Print detailed results:**

  ```bash
  python corrupted_file_checker.py /path/to/directory --verbose
  ```

## Requirements

- Python 3.6 or later
- `tqdm` library (optional, but recommended for the progress bar)

## Installation

To install the required libraries, run the following command:

```bash
pip install tqdm
```

## License

This script is free to everything...
