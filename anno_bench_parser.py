import csv
import argparse
import re
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os

# Function to remove null characters and special characters from a string
def clean_string(input_string):
    cleaned_string = input_string.replace('\0', '')
    cleaned_string = cleaned_string.replace(']', '')
    return cleaned_string

# Function to convert CSV to CSV with cleaned data
def csv_to_csv(csv_file_path):
    try:
        # Determine the output CSV file path based on the input CSV file
        output_csv_file = csv_file_path.replace(".csv", "_output.csv")

        # Open the input CSV file for reading and the output CSV file for writing
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as infile, \
             open(output_csv_file, 'w', newline='', encoding='utf-8') as outfile:

            # Create CSV reader and writer objects with semicolon as the delimiter
            csv_reader = csv.reader(infile, delimiter=';')
            csv_writer = csv.writer(outfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)

            # Iterate through rows in the input CSV, clean the data, and write to the output CSV
            for row in csv_reader:
                cleaned_row = [clean_string(cell) for cell in row]
                cleaned_row = [row for row in cleaned_row if any(item.strip() for item in row)]
                cleaned_row = [''.join([item for item in row if isinstance(item, str)]) for row in cleaned_row]
                csv_writer.writerow(cleaned_row)

        print(f"CSV data from '{csv_file_path}' has been cleaned and saved to '{output_csv_file}'")

        # Open the folder containing the output CSV file (with double quotes around the path)
        output_folder = os.path.dirname(output_csv_file)
        os.system(f'start "" "{output_folder}"')

        # Show a "Done" message pop-up
        messagebox.showinfo("Done", "CSV data has been cleaned and saved.")

    except Exception as e:
        # Show an error message pop-up
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(
        title="Select Input CSV File",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )

    if file_path:
        if file_path.endswith(".csv"):
            csv_to_csv(file_path)
        else:
            print("Error: Selected file must have a .csv extension.")

if __name__ == "__main__":
    select_file()
