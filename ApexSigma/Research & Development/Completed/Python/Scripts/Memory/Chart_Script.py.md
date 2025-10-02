---
tags:
  - Chart
  - Python
  - Script
---
import plotly.graph_objects as go

import numpy as np

  

# Define the components with better positioning for balanced layout

components_data = {

    # Layer 1: User Interface (top center)

    "User Interface": {"x": 0, "y": 5, "type": "interface", "color": "#1FB8CD"},

    # Layer 2: API Server (spread horizontally)

    "MCP Server": {"x": -2, "y": 4, "type": "server", "color": "#DB4545"},

    "REST API": {"x": -0.7, "y": 4, "type": "server", "color": "#DB4545"},

    "Auth & Rate": {"x": 0.7, "y": 4, "type": "server", "color": "#DB4545"},

    # Layer 3: Memory Management (central processing)

    "Context Router": {"x": -1.5, "y": 3, "type": "core", "color": "#2E8B57"},

    "Memory Manager": {"x": 0, "y": 3, "type": "core", "color": "#2E8B57"},

    "Compression": {"x": 1.5, "y": 3, "type": "core", "color": "#2E8B57"},

    "Relevance Score": {"x": 3, "y": 3, "type": "core", "color": "#2E8B57"},

    # Layer 4: Storage (memory types and databases)

    "Short-term": {"x": -2.5, "y": 2, "type": "storage", "color": "#5D878F"},

    "Working": {"x": -1.2, "y": 2, "type": "storage", "color": "#5D878F"},

    "Long-term": {"x": 0.1, "y": 2, "type": "storage", "color": "#5D878F"},

    "Episodic": {"x": 1.4, "y": 2, "type": "storage", "color": "#5D878F"},

    "Vector DB": {"x": 2.7, "y": 2, "type": "database", "color": "#D2BA4C"},

    "User Profile": {"x": 4, "y": 2, "type": "database", "color": "#D2BA4C"},

    # Layer 5: External (bottom layer)

    "Tools & APIs": {"x": -2, "y": 1, "type": "external", "color": "#B4413C"},

    "Databases": {"x": -0.5, "y": 1, "type": "external", "color": "#B4413C"},

    "File Systems": {"x": 1, "y": 1, "type": "external", "color": "#B4413C"},

    "Web Services": {"x": 2.5, "y": 1, "type": "external", "color": "#B4413C"}

}

  

# Define data flows with clear direction

flows = [

    ("User Interface", "MCP Server"),

    ("User Interface", "REST API"),

    ("MCP Server", "Context Router"),

    ("REST API", "Memory Manager"),

    ("Auth & Rate", "Memory Manager"),

    ("Context Router", "Memory Manager"),

    ("Memory Manager", "Short-term"),

    ("Memory Manager", "Working"),

    ("Memory Manager", "Long-term"),

    ("Memory Manager", "Episodic"),

    ("Memory Manager", "Vector DB"),

    ("Relevance Score", "Vector DB"),

    ("Context Router", "User Profile"),

    ("Compression", "Long-term"),

    ("REST API", "Tools & APIs"),

    ("MCP Server", "Databases"),

    ("REST API", "Web Services"),

    ("REST API", "File Systems")

]

  

# Create the figure

fig = go.Figure()

  

# Add flow lines with arrows

for flow in flows:

    from_comp, to_comp = flow

    if from_comp in components_data and to_comp in components_data:

        x0, y0 = components_data[from_comp]["x"], components_data[from_comp]["y"]

        x1, y1 = components_data[to_comp]["x"], components_data[to_comp]["y"]

        # Calculate arrow position (80% along the line)

        arrow_x = x0 + 0.8 * (x1 - x0)

        arrow_y = y0 + 0.8 * (y1 - y0)

        # Calculate arrow direction

        dx, dy = x1 - x0, y1 - y0

        length = np.sqrt(dx**2 + dy**2)

        if length > 0:

            dx, dy = dx/length, dy/length

        fig.add_trace(go.Scatter(

            x=[x0, x1],

            y=[y0, y1],

            mode='lines',

            line=dict(color='rgba(100,100,100,0.7)', width=2.5),

            showlegend=False,

            hoverinfo='skip'

        ))

        # Add arrowhead

        fig.add_trace(go.Scatter(

            x=[arrow_x],

            y=[arrow_y],

            mode='markers',

            marker=dict(

                size=8,

                color='rgba(100,100,100,0.8)',

                symbol='triangle-up',

                angle=np.degrees(np.arctan2(dy, dx)) - 90

            ),

            showlegend=False,

            hoverinfo='skip'

        ))

  

# Group components by type for legend

component_types = {}

for name, data in components_data.items():

    comp_type = data["type"]

    if comp_type not in component_types:

        component_types[comp_type] = []

    component_types[comp_type].append((name, data))

  

# Define better type names and symbols

type_names = {

    "interface": "UI Layer",

    "server": "API Server",

    "core": "Memory Mgmt",

    "storage": "Memory Store",

    "database": "Databases",

    "external": "External"

}

  

symbols = {

    "interface": "circle",

    "server": "square",

    "core": "diamond",

    "storage": "hexagon",

    "database": "star",

    "external": "triangle-up"

}

  

# Add nodes for each component type with better text visibility

for comp_type, components in component_types.items():

    x_coords = [comp[1]["x"] for comp in components]

    y_coords = [comp[1]["y"] for comp in components]

    names = [comp[0] for comp in components]

    color = components[0][1]["color"]

    fig.add_trace(go.Scatter(

        x=x_coords,

        y=y_coords,

        mode='markers+text',

        marker=dict(

            size=35,

            color=color,

            symbol=symbols.get(comp_type, "circle"),

            line=dict(width=3, color='white')

        ),

        text=names,

        textposition="middle center",

        textfont=dict(size=11, color='white', family='Arial Black'),

        name=type_names.get(comp_type, comp_type),

        hovertemplate='<b>%{text}</b><br>Type: ' + type_names.get(comp_type, comp_type) + '<extra></extra>'

    ))

  

# Add layer background rectangles for better grouping

layer_boxes = [

    {"x0": -4.5, "x1": 4.5, "y0": 4.7, "y1": 5.3, "color": "rgba(31,184,205,0.1)", "name": "UI Layer"},

    {"x0": -2.5, "x1": 1.2, "y0": 3.7, "y1": 4.3, "color": "rgba(219,69,69,0.1)", "name": "API Layer"},

    {"x0": -2, "x1": 3.5, "y0": 2.7, "y1": 3.3, "color": "rgba(46,139,87,0.1)", "name": "Memory Mgmt"},

    {"x0": -3, "x1": 4.5, "y0": 1.7, "y1": 2.3, "color": "rgba(93,135,143,0.1)", "name": "Storage"},

    {"x0": -2.5, "x1": 3, "y0": 0.7, "y1": 1.3, "color": "rgba(180,65,60,0.1)", "name": "External"}

]

  

for box in layer_boxes:

    fig.add_shape(

        type="rect",

        x0=box["x0"], y0=box["y0"], x1=box["x1"], y1=box["y1"],

        fillcolor=box["color"],

        line=dict(color="rgba(128,128,128,0.3)", width=1),

        layer="below"

    )

  

# Update layout

fig.update_layout(

    title="memOS Memory System Architecture",

    showlegend=True,

    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),

    xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[-5, 5]),

    yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[0.5, 5.5]),

    plot_bgcolor='rgba(0,0,0,0)',

    hovermode='closest'

)

  

fig.update_traces(cliponaxis=False)

  

# Save the chart

fig.write_image("memos_architecture.png", width=1200, height=800)