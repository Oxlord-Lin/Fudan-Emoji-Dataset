import os
import glob
import regex
import pandas as pd
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
import gc
import joblib

# Precompile the emoji regex pattern for maximum performance
EMOJI_PATTERN = regex.compile(r'\p{Extended_Pictographic}')

def process_parquet_file(filepath: str) -> Counter:
    """
    Load a single parquet file, extract emojis from the 'content' column,
    and return a local frequency counter.
    """
    # Read only the 'content' column to minimize memory usage
    df = pd.read_parquet(filepath, columns=['content'])
    local_counter = Counter()
    
    for text in tqdm(df['content'].dropna(), total=len(df)):
        if isinstance(text, str):
            # Find all emojis in the text and update the local counter
            local_counter.update(EMOJI_PATTERN.findall(text))        
    del df
    gc.collect()
    
    return local_counter

def main(dataset_dir: str, output_excel: str = "emoji_frequency.xlsx") -> None:
    """
    Process all parquet files in parallel and save emoji counts to an Excel file.
    """
    # Collect all parquet file paths
    parquet_files = sorted(glob.glob(os.path.join(dataset_dir, "*.parquet")))
    if not parquet_files:
        raise FileNotFoundError(f"No .parquet files found in '{dataset_dir}'")
    
    
    global_counter = Counter()
    
        
    for file in tqdm(parquet_files, total=len(parquet_files)):
        local_counter = process_parquet_file(file)
        global_counter.update(local_counter)
        
        joblib.dump(local_counter, f"./local_counters/{os.path.basename(file)}_counter.joblib")
                
    # Convert Counter to DataFrame with requested column names
    result_df = pd.DataFrame(global_counter.items(), columns=["emoji", "total_count"])
    # Sort by frequency in descending order for better readability
    result_df = result_df.sort_values("total_count", ascending=False).reset_index(drop=True)
    
    # Export to Excel
    result_df.to_excel(output_excel, index=False)
    print(f"\n✅ Processing complete. Total unique emojis: {len(result_df)}")
    print(f"📄 Results saved to '{output_excel}'")

if __name__ == "__main__":
    # Update this path to your local dataset directory
    DATASET_PATH = "./cci2_parquet/data"
    main(DATASET_PATH)