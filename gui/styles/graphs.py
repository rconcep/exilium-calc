def get_bar_chart_template() -> dict:
    """Returns the data to create a plotly bar chart."""
    return {
        "data": [
            {
                "type": "bar",
                "x": [],
                "y": [],
                "hoverinfo": "none",
            },
        ],
        "layout": {
            "title": {"text": "Total Potency"},
            "margin": {"l": 50, "r": 50, "t": 50, "b": 50},
            "plot_bgcolor": "#E5ECF6",
            "xaxis": {"gridcolor": "white"},
            "yaxis": {"gridcolor": "white", "showticklabels": False},
        },
    }


def get_donut_chart_template() -> dict:
    """Returns the data to create a plotly donut chart."""
    return {
        "data": [
            {
                "type": "pie",
                "labels": [],
                "values": [],
                "hole": 0.5,
                "textinfo": "label+percent",
                "textposition": "outside",
                "automargin": True,
                "insidetextorientation": "radial",
            },
        ],
        "layout": {
            "margin": {"l": 5, "r": 5, "t": 5, "b": 5},
            "plot_bgcolor": "#E5ECF6",
            "showlegend": False,
        },
    }
