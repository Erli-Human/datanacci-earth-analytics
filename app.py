import gradio as gr
import pandas as pd
import numpy as np

# Placeholder data (replace with your actual data source)
data = pd.DataFrame({
    'System': ['Seismic Monitor A', 'Space Weather Station B', 'Satellite C', 'Environmental Sensor D'],
    'Category': ['Seismic', 'Space Weather', 'Satellite Imagery', 'Environmental'],
    'Status': ['Online', 'Online', 'Offline', 'Online'],
    'Value': [4.5, 7.2, np.nan, 25.1]
})

def display_systems(category, system_type, query):
    """
    Filters and displays earth monitoring systems based on category, type, and query.
    """
    filtered_data = data.copy()

    if category != "All":
        filtered_data = filtered_data[filtered_data['Category'] == category]

    if system_type != "All":
        # Add more specific filtering logic if needed
        pass

    if query:
        filtered_data = filtered_data[filtered_data['System'].str.contains(query, case=False)]

    return filtered_data


with gr.Blocks() as demo:
    gr.Markdown("# Earth Analytics Dashboard")

    with gr.Row():
        category_dropdown = gr.Dropdown(
            choices=["All", "Seismic", "Space Weather", "Satellite Imagery", "Environmental"],
            label="Category",
            value="All",
        )
        system_type_dropdown = gr.Dropdown(
            choices=["All", "Monitor", "Station", "Sensor"],
            label="System Type",
            value="All",
        )
        query_textbox = gr.Textbox(label="Search")

    submit_button = gr.Button("Submit")

    output_dataframe = gr.DataFrame(headers=list(data.columns), row_count=(len(data)), col_count=(len(data.columns)))

    submit_button.click(
        fn=display_systems,
        inputs=[category_dropdown, system_type_dropdown, query_textbox],
        outputs=output_dataframe,
    )


if __name__ == "__main__":
    demo.launch()