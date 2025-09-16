import plotly.graph_objects as go
import json

# Parse the data
data = {
  "steps": [
    {"id": 1, "text": "App Startup", "description": "Initialize CustomTkinter UI\\nLoad configuration\\nSetup API client", "type": "start", "x": 400, "y": 50},
    {"id": 2, "text": "User Input", "description": "Enter city name\\nin search box", "type": "input", "x": 400, "y": 150},
    {"id": 3, "text": "Validate Input", "description": "City name\\nvalid?", "type": "decision", "x": 400, "y": 250},
    {"id": 4, "text": "Show Error", "description": "Display error\\nmessage", "type": "process", "x": 600, "y": 250},
    {"id": 5, "text": "API Call", "description": "Fetch weather data\\nfrom OpenWeatherMap", "type": "process", "x": 400, "y": 350},
    {"id": 6, "text": "Check Response", "description": "API response\\nsuccessful?", "type": "decision", "x": 400, "y": 450},
    {"id": 7, "text": "Parse Data", "description": "Extract temperature\\nweather conditions\\nforecast data", "type": "process", "x": 400, "y": 550},
    {"id": 8, "text": "Apply Theme", "description": "Select color theme\\nbased on temperature", "type": "process", "x": 200, "y": 650},
    {"id": 9, "text": "Update UI", "description": "Display current weather\\nUpdate weather cards\\nShow forecast", "type": "process", "x": 400, "y": 650},
    {"id": 10, "text": "Change Background", "description": "Apply weather-appropriate\\nbackground image", "type": "process", "x": 600, "y": 650},
    {"id": 11, "text": "Schedule Refresh", "description": "Set 5-minute timer\\nfor auto-update", "type": "process", "x": 400, "y": 750},
    {"id": 12, "text": "Wait for Next Event", "description": "User input or\\nauto-refresh timer", "type": "wait", "x": 400, "y": 850}
  ],
  "connections": [
    {"from": 1, "to": 2, "label": ""}, {"from": 2, "to": 3, "label": ""},
    {"from": 3, "to": 4, "label": "No"}, {"from": 3, "to": 5, "label": "Yes"},
    {"from": 4, "to": 2, "label": "Try again"}, {"from": 5, "to": 6, "label": ""},
    {"from": 6, "to": 4, "label": "Error"}, {"from": 6, "to": 7, "label": "Success"},
    {"from": 7, "to": 8, "label": ""}, {"from": 7, "to": 9, "label": ""},
    {"from": 7, "to": 10, "label": ""}, {"from": 8, "to": 11, "label": ""},
    {"from": 9, "to": 11, "label": ""}, {"from": 10, "to": 11, "label": ""},
    {"from": 11, "to": 12, "label": ""}, {"from": 12, "to": 2, "label": "New search or refresh"}
  ]
}

# Create figure
fig = go.Figure()

# Define colors and symbols for different step types
type_colors = {
    'start': '#1FB8CD',
    'input': '#DB4545', 
    'decision': '#2E8B57',
    'process': '#5D878F',
    'wait': '#D2BA4C'
}

type_symbols = {
    'start': 'circle',
    'input': 'square',
    'decision': 'diamond',
    'process': 'hexagon',
    'wait': 'star'
}

# Group steps by type for legend
step_types = {}
for step in data['steps']:
    step_type = step['type']
    if step_type not in step_types:
        step_types[step_type] = []
    step_types[step_type].append(step)

# Add scatter traces for each step type
for step_type, steps in step_types.items():
    x_coords = [step['x'] for step in steps]
    y_coords = [step['y'] for step in steps]
    texts = [step['text'] for step in steps]
    descriptions = [step['description'].replace('\\n', '<br>') for step in steps]
    
    # Abbreviate step type for legend (15 char limit)
    legend_name = step_type.capitalize()[:15]
    
    fig.add_trace(go.Scatter(
        x=x_coords,
        y=y_coords,
        mode='markers',
        marker=dict(
            size=20,
            color=type_colors[step_type],
            symbol=type_symbols[step_type],
            line=dict(width=2, color='white')
        ),
        name=legend_name,
        hovertemplate='<b>%{customdata[0]}</b><br>%{customdata[1]}<extra></extra>',
        customdata=list(zip(texts, descriptions))
    ))

# Create lookup for step positions
step_positions = {step['id']: (step['x'], step['y']) for step in data['steps']}

# Add connection lines
for conn in data['connections']:
    from_pos = step_positions[conn['from']]
    to_pos = step_positions[conn['to']]
    
    fig.add_trace(go.Scatter(
        x=[from_pos[0], to_pos[0]],
        y=[from_pos[1], to_pos[1]],
        mode='lines',
        line=dict(color='gray', width=2),
        showlegend=False,
        hoverinfo='skip'
    ))

# Add arrowheads for direction
for conn in data['connections']:
    from_pos = step_positions[conn['from']]
    to_pos = step_positions[conn['to']]
    
    # Calculate arrow position (90% along the line)
    arrow_x = from_pos[0] + 0.9 * (to_pos[0] - from_pos[0])
    arrow_y = from_pos[1] + 0.9 * (to_pos[1] - from_pos[1])
    
    fig.add_trace(go.Scatter(
        x=[arrow_x],
        y=[arrow_y],
        mode='markers',
        marker=dict(
            size=8,
            color='gray',
            symbol='triangle-up',
        ),
        showlegend=False,
        hoverinfo='skip'
    ))

# Update layout
fig.update_layout(
    title="WeatherPy App User Flow",
    xaxis_title="",
    yaxis_title="",
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
    showlegend=True
)

# Remove axis ticks and grid
fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False)
fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False)

# Invert y-axis to match the flow direction
fig.update_yaxes(autorange='reversed')

# Update traces
fig.update_traces(cliponaxis=False)

# Save the chart
fig.write_image("user_flow.png")
fig.write_image("user_flow.svg", format="svg")

fig.show()