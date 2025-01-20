import pandas as pd
import folium
from folium.plugins import MarkerCluster

# LED lighting locations
data = {
    "Loc": [
        "1 Paiute Dr Sls",
        "10 N 30Th St Sl Stlt",
        "516 E Saint Louis Ave Sls",
        "599 W Washington Ave Sls",
        "601 S 4Th St Sl Stlt",
        "1000 A St Sls",
        "1003 Torington Dr Sls",
        "1008 N Bruce St Sls",
        "1013 Meyer St Sls",
        "6012 Heather Mist Ln Sls",
        "6101 W Charleston Blvd Sl Stlt",
        "7192 Maple Sugar St Sl Sl",
        "7199 N Campbell Rd Sl Sl",
        "7203 W Tropical Pkwy Sl Sl",
        "9208 Estrada Ave Sls"
    ],
    "Latitude": [
        36.21046030173856,
        36.17708166948882,
        36.14288700438675,
        36.182127608311355,
        36.16810803751586,
        36.1868601495105,
        36.185822994715735,
        36.18337932239233,
        36.18734494965679,
        36.22286125008315,
        36.163564816790775,
        36.291391251770484,
        36.291116123705024,
        36.28927712707203,
        36.2247897167775
    ],
    "Longitude": [
        -115.1403531125007,
        -115.10205363417863,
        -115.14892135098557,
        -115.14913366331275,
        -115.14302011684599,
        -115.14237386902917,
        -115.23278781568811,
        -115.12415208357798,
        -115.08563182832577,
        -115.20299102035835,
        -115.17737597206957,
        -115.29140611834417,
        -115.29354566316383,
        -115.18534589599543,
        -115.28695101170365
    ]
}

# Colours
colors = [
    'red', 'blue', 'green', 'purple', 'orange',
    'darkred', 'saddlebrown', 'cyan', 'darkblue', 'darkgreen',
    'cadetblue', 'blueviolet', 'magenta', 'darkgoldenrod', 'mediumvioletred',
    'lightgreen', 'dimgray', 'black', 'indigo'
]

led = pd.DataFrame(data)

# Create a map
map = folium.Map(location=[36.21046030173856, -115.1403531125007], zoom_start=11)


# Add markers to the map
for index, row in led.iterrows():
    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=3,
        color=colors[index % len(colors)],
        fill=True,
        fill_color=colors[index % len(colors)],
        fill_opacity=0.6,
        popup=row["Loc"],
    ).add_to(map)

# HTML for legend
legend_html = '''
<div style="position: fixed; 
     bottom: 50px; left: 50px; width: 150px; height: {}px; 
     border:2px solid grey; z-index:9999; font-size:8px;
     background-color:white; padding: 5px 10px;">
     <b>Legend</b> <br>
     {} 
</div>
'''
# Create legend entries
legend_entries = ""
for i, loc in enumerate(data["Loc"]):
    color = colors[i % len(colors)]
    legend_entries += f'<i style="background: {color};width: 10px;height: 10px;display:inline-block;"></i> {loc}<br>'

# Height of the legend
legend_height = len(data["Loc"]) * 15

# legend HTML created
legend_html = legend_html.format(legend_height, legend_entries)

# Add legend to the map
map.get_root().html.add_child(folium.Element(legend_html))

# Save the map
map.save("Images/led_lighting_locations_map.html")
