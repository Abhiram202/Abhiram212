import pandas as pd
import os

# These are the variables for the file paths for the folders on your computer.
# Need to create one for the folder input and one for the finished output excel file
input_loc = 'C:\\Users\\uska1c74\\OneDrive - Kellogg Company\\Desktop\\input\\'
output_loc = 'C:\\Users\\uska1c74\\OneDrive - Kellogg Company\\Desktop\\output\\'

# Created variable to store the list of input files
fileList = os.listdir(input_loc)

# Using a for loop to merge the files altogether for the final excel file.
finalDf = pd.DataFrame()

for files in fileList:
    fileName = os.path.join(input_loc, files)

    try:
        # Checks if the file is either an excel file or csv file and uses the appropriate pandas function
        if files.endswith(".csv"):
            df = pd.read_csv(fileName)
        elif files.endswith(".xlsx") or files.endswith(".xls"):
            df = pd.read_excel(fileName)

        # Added a new column for the source file name for the user names and email addresses.
        df['Source File'] = files

        # Concatenates the DataFrame to the final DataFrame.
        finalDf = pd.concat([finalDf, df], ignore_index=True)

    # This will ignore any empty files.
    except pd.errors.EmptyDataError:
        pass  
    except Exception as e:
        pass  

# Exports to the output file location with an excel file.
merged_file = os.path.join(output_loc, 'merged_files.xlsx')
finalDf.to_excel(merged_file, index=False)

# Terminal output to show that code has run and been saved to the output file
print("Merging completed and saved to", merged_file)
