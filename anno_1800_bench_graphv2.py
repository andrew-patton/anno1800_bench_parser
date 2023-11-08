import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.layouts import column as plot_column
from bokeh.models import Legend, CheckboxGroup, CustomJS
from bokeh.palettes import Category10
import numpy as np
import os

# Function to clean a string
def clean_string(input_string):
    cleaned_string = input_string.replace('\0', '')
    cleaned_string = cleaned_string.replace(']', '')
    return cleaned_string

# Function to clean a DataFrame
def clean_dataframe(df):
    cleaned_df = df.applymap(clean_string)
    cleaned_df = cleaned_df.dropna(how='all')  # Remove rows with all NaN values
    cleaned_df = cleaned_df.dropna(axis=1, how='all')  # Remove columns with all NaN values
    return cleaned_df

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

# Function to handle file selection and processing
def select_file_and_process():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(
        title="Select Input CSV File",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )

    if file_path:
        if file_path.endswith(".csv"):
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path, delimiter=';')

            # Clean the DataFrame
            df_cleaned = clean_dataframe(df)

            # Save the cleaned data to a new CSV file
            output_csv_file = file_path.replace(".csv", "_output.csv")
            df_cleaned.to_csv(output_csv_file, sep=';', index=False)

            print(f"CSV data from '{file_path}' has been cleaned and saved to '{output_csv_file}'")

            # Open the folder containing the output CSV file (with double quotes around the path)
            output_folder = os.path.dirname(output_csv_file)
            os.system(f'start "" "{output_folder}"')

            # Create and display the Bokeh plot
            create_bokeh_plot(df_cleaned)
        else:
            print("Error: Selected file must have a .csv extension.")

if __name__ == "__main__":
    select_file_and_process()
