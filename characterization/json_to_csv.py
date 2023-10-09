#!/usr/bin/env python3

import sys
import pandas as pd

def main():
    args = sys.argv[1:]

    if len(args) not in range(2, 4):
        print("Usage: json_to_csv <input> <output> [delimiter]")
        return
    
    input_file = args[0]
    output_file = args[1]
    delimiter = "," if len(args) <= 2 else args[2]
    
    df = pd.read_json(input_file)
    df.to_csv(output_file, sep=delimiter)
    
if __name__ == "__main__":
    main()