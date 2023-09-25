import pandas as pd
from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.layouts import column as plot_column
from bokeh.models import Legend, CheckboxGroup, CustomJS
from bokeh.palettes import Category10
import numpy as np
import os

# Get the current working directory
current_dir = os.getcwd()

# Specify the output directory as the current working directory
output_dir = current_dir

# Specify the number of rows to skip (including header rows)
rows_to_skip = 20  # Skip the first 20 rows (including header rows)

# Load the CSV data into a DataFrame, skipping the specified number of rows
df = pd.read_csv("C:\\Users\\omgim\\OneDrive\\Documents\\Anno 1800\\benchmarks\\anno1800_benchmark_dx11_2023-09-20-15-57-11_output.csv", delimiter=';', skiprows=range(rows_to_skip))

# Extract relevant information
frame_time_columns = [col for col in df.columns if 'FrameTime' in col or 'PresentTime' in col]

# Define a function to remove outliers using the Z-score method
def remove_outliers(data):
    z_scores = np.abs((data - data.mean()) / data.std())
    threshold = 10  # Adjust this threshold as needed
    return data[z_scores < threshold]

# Remove outliers from frame_time_data and present_time_data
df_cleaned = df[frame_time_columns].apply(remove_outliers)

# Create a Bokeh plot
p = figure(title="FrameTime and PresentTime (ms) Over Frames and Multiple Runs", x_axis_label="Frame", y_axis_label="Time (ms)", width=1000, height=500)

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

# Add the layout to the Bokeh document
curdoc().add_root(layout)

# Customize plot properties
p.grid.grid_line_color = None
p.background_fill_color = "black"
p.title.text_color = "white"
p.xaxis.axis_label_text_color = "white"
p.yaxis.axis_label_text_color = "white"
p.legend.label_text_color = "white"
p.legend.background_fill_alpha = 0.7

# Specify the output file
output_file("interactive_chart.html")

# Show the interactive Bokeh plot in the HTML file
curdoc().add_root(plot_column(p, checkbox_group))
show(p)
