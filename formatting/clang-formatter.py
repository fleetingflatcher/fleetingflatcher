#!/usr/bin/env python3

import subprocess
import os
import sys
from pathlib import Path
from typing import List, Optional

# Global verbose flag
verbose = False

def print_cmd(cmd: List[str]):
    """Print a command if verbose mode is enabled."""
    if verbose:
        for token in cmd:
            print(token, sep=' ', end=' ')
        print()

def print_verbose(msg: str):
    """Print a message if verbose mode is enabled."""
    if verbose:
        print(msg)



def check_dependencies() -> bool:
    """Check if required tools (clang-format and git) are available."""
    for tool in ['clang-format', 'git']:
        try:
            subprocess.run([tool, '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"Error: {tool} is not installed or not in PATH")
            return False
    return True

def check_config_files() -> bool:
    """Check if required configuration files exist."""
    if not Path('.clang-format').is_file():
        print("Error: .clang-format file not found in current directory")
        return False
    
    if not Path('.gitignore').is_file():
        print("Warning: .gitignore file not found in current directory")
    
    return True

def get_files_to_format(directory: str = "") -> Optional[List[str]]:
    """Get list of .c and .h files respecting .gitignore."""
    try:

        # Get only tracked files (removing --others flag)
        cmd = ['git', 'ls-files', '--cached', f'{directory}/*.c', f'{directory}/*.h']

        print_cmd(cmd)

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        print_verbose("\n\nResult\n\n" + result.stdout)

        # Split output into lines and filter out empty lines
        files = [f for f in result.stdout.splitlines() if f.strip()]
        
        print_verbose("\n\nFiles\n\n" + str(files))

        # Filter to ensure files still exist
        files = [f for f in files if Path(f).is_file()]

        print_verbose("\n\nValid Files\n\n" + str(files))

        return files
    
    except subprocess.CalledProcessError as e:
        print(f"Error getting files from git: {e}")
        print(f"git stderr: {e.stderr}")
        return None
    except OSError as e:
        print(f"Error accessing directory {directory}: {e}")
        return None

def format_file(file_path: str, idx: int, total_num: int) -> bool:
    """Format a single file using clang-format."""
    try:
        cmd = ['clang-format', '-i', '--verbose', '--style=file', file_path]
        print(f"Formatting [{idx} / {total_num}]: {file_path}")
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error formatting {file_path}: {e}")
        print(f"clang-format stderr: {e.stderr}")
        return False

def main():
    print("Starting code formatting...")
    
    # Check dependencies and config files
    if not check_dependencies() or not check_config_files():
        sys.exit(1)
    
    if len(sys.argv) <= 1:
        print("No directory provided. Formatting all files in current directory.")
        directory = os.getcwd()
    else:
        print("Directory provided: ", sys.argv[1])
        directory = sys.argv[1]

    # Get files to format
    files = get_files_to_format(directory)

    if files is None:
        sys.exit(1)
    
    if not files:
        print("No .c or .h files found to format")
        sys.exit(0)
    
    print(f"Found {len(files)} files to format")
    
    # Format each file
    success = True
    index = 0
    for file_path in files:
        index += 1
        if not format_file(file_path, index, len(files)):
            success = False
    
    if success:
        print("Formatting complete!")
        sys.exit(0)
    else:
        print("Error occurred during formatting")
        sys.exit(1)

if __name__ == "__main__":
    main()