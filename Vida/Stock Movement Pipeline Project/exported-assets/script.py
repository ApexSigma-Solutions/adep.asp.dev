# Let's examine some of the Excel files to understand the data structure better
import pandas as pd

# First, let's look at the sample data files provided
# Checking the files available in our current directory
import os
files = os.listdir('.')
excel_files = [f for f in files if f.endswith('.xlsx')]
print("Available Excel files:")
for f in excel_files:
    print(f"  {f}")