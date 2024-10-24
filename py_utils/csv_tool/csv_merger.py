import pandas as pd
from pathlib import Path
import sys

def merge_csv_files(file1_path: str, file2_path: str, output_path: str = "merged.csv") -> None:
    """
    Merge two CSV files, prefixing each column with its source filename.
    
    Args:
        file1_path: Path to first CSV file
        file2_path: Path to second CSV file
        output_path: Path for output merged CSV file
    """
    try:
        # Read the CSV files
        df1 = pd.read_csv(file1_path)
        df2 = pd.read_csv(file2_path)
        
        # Get filenames without extension for prefixing
        prefix1 = Path(file1_path).stem
        prefix2 = Path(file2_path).stem
        
        # Rename columns with filename prefixes
        df1.columns = [f"{prefix1}_{col}" for col in df1.columns]
        df2.columns = [f"{prefix2}_{col}" for col in df2.columns]
        
        # Merge dataframes side by side
        merged_df = pd.concat([df1, df2], axis=1)
        
        # Save merged dataframe
        merged_df.to_csv(output_path, index=False)
        print(f"Successfully merged files into {output_path}")
        print("\nNew column names:")
        for col in merged_df.columns:
            print(f"  - {col}")
            
    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e.filename}")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print("Error: One or both CSV files are empty")
        sys.exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred - {str(e)}")
        sys.exit(1)

def main():
    if len(sys.argv) < 3:
        print("Usage: python csv_merger.py file1.csv file2.csv [output.csv]")
        sys.exit(1)
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) > 3 else "merged.csv"
    
    merge_csv_files(file1, file2, output)

if __name__ == "__main__":
    main()