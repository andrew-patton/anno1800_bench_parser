import argparse
import csv
import pandas as pd
from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.layouts import column as plot_column
from bokeh.models import Legend, CheckboxGroup, CustomJS
from bokeh.palettes import Category10
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
        output_csv_file = csv_file_path.replace(".csv", "_cleaned.csv")

        # Open the input CSV file for reading and the output CSV file for writing
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as infile, \
             open(output_csv_file, 'w', newline='', encoding='utf-8') as outfile:

            # Create CSV reader and writer objects with semicolon as the delimiter
            csv_reader = csv.reader(infile, delimiter=';')
            csv_writer = csv.writer(outfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)

            # Iterate through rows in the input CSV, clean the data, and write to the output CSV
            for row in csv_reader:
                cleaned_row = [clean_string(cell) for cell in row]
                csv_writer.writerow(cleaned_row)

        print(f"CSV data from '{csv_file_path}' has been cleaned and saved to '{output_csv_file}'")
        
        return output_csv_file

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Function to create the Bokeh plot
def create_bokeh_plot(df_cleaned):
    # Create a Bokeh plot
    p = figure(title="FrameTime and PresentTime (ms) Over Frames and Multiple Runs", x_axis_label="Time (ms)", y_axis_label="FrameTime", width=1000, height=500)

    # Create a list of line renderers and labels for the legend
    renderers = []
    legend_labels = []

    # Add each line as a separate series to the plot
    for i, column in enumerate(df_cleaned.columns):
        label = column.split('(')[0].strip()  # Extract the label without units
        color = Category10[10][i % 10]  # Choose a color from the Category10 palette
        line_renderer = p.line(df_cleaned.index, df_cleaned[column], line_color=color, line_width=2, line_alpha=0.7)
        renderers.append((label, [line_renderer]))
        legend_labels.append((label, [line_renderer]))

    # Create a legend
    legend = Legend(items=legend_labels, location="top_left")
    p.add_layout(legend)
    p.legend.title = "click to hide"
    p.legend.label_text_font_size = "12pt"
    p.legend.click_policy="mute"

    # Create a checkbox group to toggle line visibility
    checkbox_group = CheckboxGroup(labels=df_cleaned.columns.tolist(), active=list(range(len(df_cleaned.columns))))

    # Create the layout with the checkbox group
    layout = plot_column(p, checkbox_group)

    # JavaScript callback to toggle line visibility
    callback = CustomJS(code="""
        var active = cb_obj.active;
        for (var i = 0; i < renderers.length; i++) {
            renderers[i].glyph.visible = active.includes(i);
        }
    """, args={'renderers': renderers})

    # Attach the callback to the checkbox group
    checkbox_group.js_on_change('active', callback)

    # Customize plot properties
    p.grid.grid_line_color = None
    p.background_fill_color = "black"
    p.title.text_color = "black"
    p.xaxis.axis_label_text_color = "black"
    p.yaxis.axis_label_text_color = "black"
    p.legend.label_text_color = "black"
    p.legend.background_fill_alpha = 0.7

    # Specify the output file
    output_file("interactive_chart.html")

    # Show the interactive Bokeh plot in the HTML file
    curdoc().add_root(layout)
    show(p)

# Initialize the parser
parser = argparse.ArgumentParser(description="Clean and plot CSV data.")
# Add arguments
parser.add_argument('csv_file', type=str, help='The path to the CSV file to process')
parser.add_argument('--rows_to_skip', type=int, default=20, help='The number of rows to skip')

# Parse the arguments
args = parser.parse_args()

if __name__ == "__main__":
    # Use the provided arguments to process the CSV file
    if args.csv_file.endswith(".csv"):
        # Clean and process the CSV file
        output_csv_file = csv_to_csv(args.csv_file)

        if output_csv_file:
            # Load the cleaned CSV data into a DataFrame
            df_cleaned = pd.read_csv(output_csv_file, delimiter=';', skiprows=range(args.rows_to_skip))

            # Create and display the Bokeh plot
            create_bokeh_plot(df_cleaned)
    else:
        print("Error: The provided file path must have a .csv extension.")

if __name__ == "__main__":
    # Specify the number of rows to skip (including header rows)
    rows_to_skip = 20  # Skip the first 20 rows (including header rows)
    select_file_and_process(rows_to_skip)