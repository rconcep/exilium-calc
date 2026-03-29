def get_bar_chart_template() -> dict:
    """Returns the data to create a plotly bar chart."""
    return {
        "data": [
            {
                "type": "bar",
                "x": [],
                "y": [],
                "hoverinfo": "none",
                "marker": {
                    "color": ["#5da0a6", "#d5a34f"],
                    "line": {"color": "#f1d387", "width": 1.2},
                },
                "textfont": {"color": "#eef4ef", "family": "Inter, sans-serif"},
            },
        ],
        "layout": {
            "title": {"text": "Total Potency"},
            "margin": {"l": 50, "r": 50, "t": 50, "b": 50},
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(10,24,30,0.9)",
            "font": {"color": "#eef4ef", "family": "Inter, sans-serif"},
            "title_font": {"family": "Josefin Sans, sans-serif", "size": 18},
            "xaxis": {
                "gridcolor": "rgba(143,214,208,0.08)",
                "linecolor": "rgba(143,214,208,0.24)",
                "tickfont": {"color": "#c8d4d4"},
            },
            "yaxis": {
                "gridcolor": "rgba(143,214,208,0.08)",
                "showticklabels": False,
                "linecolor": "rgba(143,214,208,0.24)",
            },
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
                "marker": {
                    "colors": [
                        "#d5a34f",
                        "#65bbc4",
                        "#8fd6d0",
                        "#88b2b8",
                        "#dfc27d",
                        "#437b83",
                    ],
                    "line": {"color": "#0b161b", "width": 1.5},
                },
                "textfont": {"color": "#eef4ef", "family": "Inter, sans-serif"},
            },
        ],
        "layout": {
            "margin": {"l": 5, "r": 5, "t": 5, "b": 5},
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(10,24,30,0.9)",
            "font": {"color": "#eef4ef", "family": "Inter, sans-serif"},
            "showlegend": False,
        },
    }
