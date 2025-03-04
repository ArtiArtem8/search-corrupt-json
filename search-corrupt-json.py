import sys
import os
import json
import importlib.util
import time
import argparse

def check_json(filepath):
    """
    Check if a JSON file is corrupted.

    Returns:
        str or None: Error message if the file is corrupted, otherwise None.
    """
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

    if not data:
        return None  # file is empty

    if all(b == 0x00 for b in data):
        return "Corrupted (all 0x00 bytes)"

    # Check if valid JSON
    try:
        json.loads(data.decode('utf-8-sig'))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        return f"Corrupted (invalid JSON: {str(e)})"
    except Exception as e:
        return f"Corrupted (error: {str(e)})"

    return None

def check_null_bytes(filepath):
    try:
        with open(filepath, 'rb') as f:
            first_chunk = f.read(1024)
            
            if not first_chunk:
                return None  # file is empty
            
            # If the first 1024 bytes are not all null, stop checking
            if not all(b == 0x00 for b in first_chunk):
                return None
            
            # If the first 1024 bytes are all null, check the rest of the file
            while True:
                chunk = f.read(1024)
                if not chunk:
                    break  # End of file
                if any(b != 0x00 for b in chunk):
                    return None
            
            return "Entire file is null bytes (0x00)"
    except Exception as e:
        return f"Error reading file: {str(e)}"
        
def simple_progress_bar(current, total):
    progress = int((current / total) * 100)
    if (current-1)%10 == 0:
        print(f"\rChecking files: {progress}% ({current}/{total})", end='')

def main():
    parser = argparse.ArgumentParser(description='Check for corrupted files',
                                     epilog='Example usage: python script.py --all --verbose /path/to/root/directory',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('path', nargs='?', default=os.getcwd(), help='Path to the directory to check. Defaults to the current working directory.')
    parser.add_argument('--all', action='store_true', help='Check all files, not just JSON files.')
    parser.add_argument('--verbose', action='store_true', help='Print results as files get checked. If not specified, only a progress bar will be displayed.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0', help='Show the version number and exit.')
    args = parser.parse_args()
    args.path = args.path.strip('"').strip("'")
    print(f"Searching for files in '{args.path}'")

    check_func = check_null_bytes if args.all else check_json
    file_extension = '' if args.all else '.json'

    files = []
    for foldername, _, filenames in os.walk(args.path):
        for filename in filenames:
            if filename.lower().endswith(file_extension):
                files.append(os.path.join(foldername, filename))
    last_update_time = time.time()
    corrupted_files = []
    if importlib.util.find_spec('tqdm') is not None:
        from tqdm import tqdm
        pbar = tqdm(files, desc="Checking files", unit=" files", mininterval=0.25, ascii=True)
        for filepath in pbar:
            result = check_func(filepath)
            if result:
                corrupted_files.append(filepath)
                if args.verbose:
                    tqdm.write(f"{result}: {filepath}")
            current_time = time.time()
            if current_time - last_update_time >= 1:
                pbar.set_description(f"Checking files: {os.path.basename(filepath)}")
                last_update_time = current_time
    else:
        print("Warning: tqdm not found. You can install it manually by running 'pip install tqdm' in your terminal.")
        print("Using simple progress bar instead.")
        for i, filepath in enumerate(files):
            result = check_func(filepath)
            if result:
                corrupted_files.append(filepath)
                if args.verbose:
                    print(f"{result}: {filepath}")
            simple_progress_bar(i+1, len(files))
        print()

    print("\n")
    if corrupted_files:
        print(f"Found {len(corrupted_files)} corrupted files:")
        for file in corrupted_files:
            print(file)
    else:
        print("No corrupted files found.")

if __name__ == "__main__":
    main()