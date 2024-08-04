import pandas as pd
import os

# These are the variables for the file paths for the folders on your computer.
input_loc = 'input file, file path of your computer'
output_loc = 'output file, file path of your computer'

# Creates a variable to store the list of input files.
fileList = os.listdir(input_loc)

# Uses a for loop to check for errors within the files.
error_logs = []

for files in fileList:
    fileName = os.path.join(input_loc, files)

    try:
        # Check whether the file is in csv or excel format and uses the appropriate pandas function.
        if files.endswith(".csv"):
            df = pd.read_csv(fileName)
        elif files.endswith(".xlsx") or files.endswith(".xls"):
            df = pd.read_excel(fileName)
        else:
            error_logs.append([fileName, "Unsupported file type"])
            continue

        # Check for missing columns.
        required_columns = df.columns.tolist() # Gets all columns from the DataFrame
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            error_logs.append([fileName, f"Missing columns: {', '.join(missing_columns)}"])
            continue

        # Checks for missing values and cells.
        for col in df.columns:
            if df[col].isnull().any():
                missing_rows = df[df[col].isnull()].index.tolist()
                missing_rows = [str(row + 2) for row in missing_rows]  # This adjust the row index in excel so it is easier to read
                error_logs.append([fileName, f"Missing values in column '{col}', rows: {', '.join(missing_rows)}"])

    except pd.errors.EmptyDataError:
        error_logs.append([fileName, "File is empty"])
    except Exception as e:
        error_logs.append([fileName, str(e)])

# Creates a DataFrame for error logs.
error_df = pd.DataFrame(error_logs, columns=['Source File', 'Error'])

# Exports the error logs to an excel file.
error_file = os.path.join(output_loc, 'error_logs.xlsx')
error_df.to_excel(error_file, index=False)

# Terminal output to show that code has run and been saved to the output file.
print("Error checking completed and saved to", error_file)
