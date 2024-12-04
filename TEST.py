import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import requests
import re
import json

url = "https://us09d.sheltermanager.com/service?method=animal_view_adoptable_js&account=dm1425"

# Function to parse the JavaScript response and extract JSON
def fetch_animals():
    try:
        response = requests.get(url)
        response.raise_for_status()
        # Extract JSON string using regex
        match = re.search(r"var adoptables = (\[.*?\]);", response.text, re.DOTALL)
        if match:
            json_data = match.group(1)  # Extract the JSON array
            data = json.loads(json_data)  # Parse it into Python objects
            return data
        else:
            print("Could not extract JSON from response.")
            return []
    except Exception as e:
        print(f"Error fetching or parsing data: {e}")
        return []

# Fetch data for the dropdown
animal_data = fetch_animals()

# Initialize the app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    dcc.Dropdown(id='animal-dropdown', placeholder="Select an animal..."),
    html.Div(id='selected-animal')
])

@app.callback(
    Output('animal-dropdown', 'options'),
    Input('animal-dropdown', 'id')  # Trigger on load
)
def populate_dropdown(_):
    # Fetch the latest animal data
    animal_data = fetch_animals()
    dropdown_options = [
        {"label": animal.get("ANIMALNAME", "Unknown"), "value": animal.get("ANIMALNAME", "Unknown")}
        for animal in animal_data
    ]
    # print("Dropdown Options:", dropdown_options)  # Debugging
    return dropdown_options

# Callback to display the selected animal
@app.callback(
    Output('selected-animal', 'children'),
    Input('animal-dropdown', 'value')
)
def display_selected_animal(selected):
    if selected:
        return f"You selected: {selected}"
    return "No animal selected."

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
