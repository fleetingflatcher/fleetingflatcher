#!/usr/bin/env python3

import subprocess
import os
import sys
from pathlib import Path
from typing import List, Optional

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

def get_files_to_format() -> Optional[List[str]]:
    """Get list of .c and .h files respecting .gitignore."""
    try:
        # Get both tracked and untracked files, excluding .gitignore patterns
        cmd = ['git', 'ls-files', '--cached', '--others', '--exclude-standard', '*.c', '*.h']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Split output into lines and filter out empty lines
        files = [f for f in result.stdout.splitlines() if f.strip()]
        
        # Filter to ensure files still exist
        files = [f for f in files if Path(f).is_file()]
        
        return files
    
    except subprocess.CalledProcessError as e:
        print(f"Error getting files from git: {e}")
        print(f"git stderr: {e.stderr}")
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
    
    # Get files to format
    files = get_files_to_format()
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