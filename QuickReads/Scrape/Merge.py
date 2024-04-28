import pandas as pd

# List of CSV files
csv_files = ['Business_articles.csv', 'healthline_articles.csv', 
             'Education_articles.csv','Movies_articles.csv',
             'Nature_articles.csv','Politics_articles.csv',
             'Sports_articles.csv','Technology_articles.csv',
             'Travel_articles.csv']  # Add more CSV files as needed

# List to store all dataframes
dfs = []

# Loop through each CSV file
for filename in csv_files:
    # Read CSV file into a dataframe
    df = pd.read_csv(filename, encoding='utf-8-sig')
    # Append dataframe to list
    dfs.append(df)

# Concatenate all dataframes into one
combined_df = pd.concat(dfs, ignore_index=True)

# Output combined dataframe to a new CSV file
combined_df.to_csv('Final.csv', index=False,encoding='utf-8-sig')

print("CSV files successfully combined!")