import plotly.graph_objects as go
import plotly.express as px
import json

# Parse the data
data = {
  "components": [
    {
      "name": "WeatherApp (main_app.py)",
      "type": "Main Application",
      "x": 400,
      "y": 50,
      "width": 200,
      "height": 60,
      "color": "#3498DB"
    },
    {
      "name": "ModernSearchEntry",
      "type": "UI Widget",
      "x": 50,
      "y": 150,
      "width": 140,
      "height": 40,
      "color": "#E74C3C"
    },
    {
      "name": "WeatherCard",
      "type": "UI Widget", 
      "x": 210,
      "y": 150,
      "width": 140,
      "height": 40,
      "color": "#E74C3C"
    },
    {
      "name": "ForecastCard",
      "type": "UI Widget",
      "x": 370,
      "y": 150,
      "width": 140,
      "height": 40,
      "color": "#E74C3C"
    },
    {
      "name": "SettingsPanel",
      "type": "UI Widget",
      "x": 530,
      "y": 150,
      "width": 140,
      "height": 40,
      "color": "#E74C3C"
    },
    {
      "name": "StatusBar",
      "type": "UI Widget",
      "x": 690,
      "y": 150,
      "width": 140,
      "height": 40,
      "color": "#E74C3C"
    },
    {
      "name": "WeatherAPIClient (api_client.py)",
      "type": "API Layer",
      "x": 200,
      "y": 250,
      "width": 200,
      "height": 60,
      "color": "#27AE60"
    },
    {
      "name": "Utils (utils.py)",
      "type": "Utilities",
      "x": 450,
      "y": 250,
      "width": 150,
      "height": 60,
      "color": "#F39C12"
    },
    {
      "name": "Config (config.py)",
      "type": "Configuration",
      "x": 650,
      "y": 250,
      "width": 150,
      "height": 60,
      "color": "#9B59B6"
    },
    {
      "name": "OpenWeatherMap API",
      "type": "External Service",
      "x": 100,
      "y": 370,
      "width": 180,
      "height": 50,
      "color": "#34495E"
    },
    {
      "name": "Weather Icons Service",
      "type": "External Service",
      "x": 320,
      "y": 370,
      "width": 180,
      "height": 50,
      "color": "#34495E"
    },
    {
      "name": "Cache System",
      "type": "Storage",
      "x": 540,
      "y": 370,
      "width": 120,
      "height": 50,
      "color": "#7F8C8D"
    }
  ],
  "connections": [
    {"from": "WeatherApp (main_app.py)", "to": "ModernSearchEntry"},
    {"from": "WeatherApp (main_app.py)", "to": "WeatherCard"},
    {"from": "WeatherApp (main_app.py)", "to": "ForecastCard"},
    {"from": "WeatherApp (main_app.py)", "to": "SettingsPanel"},
    {"from": "WeatherApp (main_app.py)", "to": "StatusBar"},
    {"from": "WeatherApp (main_app.py)", "to": "WeatherAPIClient (api_client.py)"},
    {"from": "WeatherApp (main_app.py)", "to": "Utils (utils.py)"},
    {"from": "WeatherApp (main_app.py)", "to": "Config (config.py)"},
    {"from": "WeatherAPIClient (api_client.py)", "to": "OpenWeatherMap API"},
    {"from": "Utils (utils.py)", "to": "Weather Icons Service"},
    {"from": "WeatherAPIClient (api_client.py)", "to": "Cache System"}
  ]
}

# Create component name to position mapping
comp_positions = {comp["name"]: (comp["x"] + comp["width"]/2, comp["y"] + comp["height"]/2) for comp in data["components"]}

# Create the figure
fig = go.Figure()

# Brand colors mapping
type_colors = {
    "Main Application": "#1FB8CD",
    "UI Widget": "#DB4545", 
    "API Layer": "#2E8B57",
    "Utilities": "#5D878F",
    "Configuration": "#D2BA4C",
    "External Service": "#B4413C",
    "Storage": "#964325"
}

# Function to abbreviate component names to fit 15 char limit
def abbreviate_name(name):
    abbreviations = {
        "WeatherApp (main_app.py)": "WeatherApp",
        "ModernSearchEntry": "SearchEntry",
        "WeatherCard": "WeatherCard",
        "ForecastCard": "ForecastCard", 
        "SettingsPanel": "SettingsPanel",
        "StatusBar": "StatusBar",
        "WeatherAPIClient (api_client.py)": "APIClient",
        "Utils (utils.py)": "Utils",
        "Config (config.py)": "Config",
        "OpenWeatherMap API": "OpenWeather",
        "Weather Icons Service": "WeatherIcons",
        "Cache System": "Cache"
    }
    return abbreviations.get(name, name[:15])

# Add connection lines with arrows
for connection in data["connections"]:
    from_pos = comp_positions[connection["from"]]
    to_pos = comp_positions[connection["to"]]
    
    # Calculate arrow position (90% along the line)
    arrow_x = from_pos[0] + 0.9 * (to_pos[0] - from_pos[0])
    arrow_y = from_pos[1] + 0.9 * (to_pos[1] - from_pos[1])
    
    # Add line
    fig.add_trace(go.Scatter(
        x=[from_pos[0], to_pos[0]],
        y=[from_pos[1], to_pos[1]],
        mode='lines',
        line=dict(color='#7F8C8D', width=2),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add arrowhead
    fig.add_trace(go.Scatter(
        x=[arrow_x],
        y=[arrow_y],
        mode='markers',
        marker=dict(
            symbol='triangle-up',
            size=8,
            color='#7F8C8D',
            angle=0
        ),
        showlegend=False,
        hoverinfo='skip'
    ))

# Add component rectangles and labels
for comp in data["components"]:
    # Add rectangle shape
    fig.add_shape(
        type="rect",
        x0=comp["x"],
        y0=comp["y"],
        x1=comp["x"] + comp["width"],
        y1=comp["y"] + comp["height"],
        fillcolor=type_colors.get(comp["type"], "#1FB8CD"),
        line=dict(color="white", width=2),
        opacity=0.8
    )
    
    # Add text label
    fig.add_trace(go.Scatter(
        x=[comp["x"] + comp["width"]/2],
        y=[comp["y"] + comp["height"]/2],
        mode='text',
        text=[abbreviate_name(comp["name"])],
        textfont=dict(color="white", size=10, family="Arial Black"),
        showlegend=False,
        hovertemplate=f'<b>{comp["name"]}</b><br>Type: {comp["type"]}<extra></extra>'
    ))

# Add legend traces (invisible markers just for legend)
added_types = set()
for comp in data["components"]:
    comp_type = comp["type"]
    if comp_type not in added_types:
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(
                size=15,
                color=type_colors.get(comp_type, "#1FB8CD"),
                symbol='square'
            ),
            name=comp_type,
            showlegend=True
        ))
        added_types.add(comp_type)

# Update layout
fig.update_layout(
    title="WeatherPy App Architecture",
    showlegend=True,
    legend=dict(orientation='v', yanchor='top', y=0.95, xanchor='left', x=1.02),
    plot_bgcolor='white',
    xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[-50, 950]),
    yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[0, 450])
)

fig.update_traces(cliponaxis=False)

# Save the chart
fig.write_image("architecture_diagram.png")
fig.write_image("architecture_diagram.svg", format="svg")

fig.show()