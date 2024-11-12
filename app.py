import plotly.express as px
from shiny.express import input, ui, render
from shinywidgets import render_plotly
from palmerpenguins import load_penguins
import matplotlib.pyplot as plt
import seaborn as sns
from shiny import reactive

# Load the penguins dataset
penguins_df = load_penguins()

# Set up page options
ui.page_opts(title="Moses Penguins Data", fillable=True)

# Sidebar for user input controls
with ui.sidebar(open="open"):
    ui.h2("Sidebar")
    ui.input_selectize(
        "selected_attribute",
        "Select attributes",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
        selected=["bill_length_mm"],
        multiple=True
    )
    ui.input_numeric("plotly_bin_count", "Input number", 0)
    ui.input_slider("seaborn_bin_count", "Bin Count", min=0, max=20, value=10)
    ui.input_checkbox_group(
        "selected_species_list",
        "Species:", 
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
        inline=True
    )
    ui.hr()
    ui.a("GitHub", href="https://github.com/mokeyzz1/cintel-02-data", target="_blank")

# Reactive function to filter penguins_df based on selected species
@reactive.calc
def filtered_data():
    selected_species = input.selected_species_list()
    return penguins_df[penguins_df["species"].isin(selected_species)]

# Layout for data table and grid
with ui.layout_columns():
    with ui.card():
        ui.card_header("Penguins Data Table")
        
        @render.data_frame
        def penguinstable_df():
            return render.DataTable(filtered_data(), filters=False, selection_mode='row')

    with ui.card():
        ui.card_header("Penguins Data Grid")
        
        @render.data_frame
        def penguinsgrid_df():
            return render.DataGrid(filtered_data(), filters=False, selection_mode="row")

# Layout for Plotly and Seaborn visualizations
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Plotly Histogram: Species")
        
        @render_plotly
        def plot1():
            fig = px.histogram(
                filtered_data(),
                x="body_mass_g",
                color="species",
                title="Penguin Body Mass by Species",
                labels={"body_mass_g": "Body Mass (g)", "count": "Count"},
                marginal="box"
            )
            return fig

    with ui.card(full_screen=True):
        ui.card_header("Seaborn Histogram: Species")
        
        @render.plot
        def seaborn_histogram():
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(data=filtered_data(), x="body_mass_g", hue="species", multiple="stack", ax=ax)
            ax.set_title("Penguin Body Mass by Species")
            ax.set_xlabel("Body Mass (g)")
            ax.set_ylabel("Count")
            return fig

with ui.card(full_screen=True):
    ui.card_header("Plotly Scatterplot: Penguin Flipper & Bill Length")
    
    @render_plotly
    def plotly_scatterplot():
        fig = px.scatter(
            filtered_data(),
            x="flipper_length_mm",
            y="bill_length_mm",
            color="species",
            title="Penguins Scatterplot: Body Mass vs. Flipper Length",
            labels={
                "flipper_length_mm": "Flipper Length (mm)",
                "bill_length_mm": "Bill Length (mm)"
            }
        )
        return fig
