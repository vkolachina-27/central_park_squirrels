import pandas as pd
import plotly.express as px
from preswald import connect, get_df, text, plotly, table

connect()
df = get_df("data/Central_Park_Squirrel_Data.csv")

df.columns = [col.lower().replace(' ', '_') for col in df.columns]

if 'lat' not in df.columns and 'lat/long' in df.columns:
    df['lat'] = df['lat/long'].str.extract(r'POINT \([^ ]+ ([^ ]+)\)')
    df['long'] = df['lat/long'].str.extract(r'POINT \(([^ ]+) [^ ]+\)')
    
    df['lat'] = pd.to_numeric(df['lat'])
    df['long'] = pd.to_numeric(df['long'])

fig = px.scatter_mapbox(
    df, 
    lat="lat", 
    lon="long", 
    color="primary_fur_color",
    hover_name="unique_squirrel_id",
    hover_data=["age", "running", "chasing", "climbing", "eating", "foraging"],
    zoom=14,
    height=600,
    title="Squirrel Sightings in Central Park"
)

fig.update_layout(
    mapbox_style="open-street-map",
    mapbox=dict(
        center=dict(lat=40.7826, lon=-73.9656),
    ),
    margin={"r":0,"t":50,"l":0,"b":0}
)

text("# Squirrels in Central Park")
text("Map of squirrel sightings in Central Park (hover for squirrel details)")
plotly(fig)

activity_columns = ['running', 'chasing', 'climbing', 'eating', 'foraging']

activity_by_shift = pd.DataFrame()

for activity in activity_columns:
    am_count = df[df['shift'] == 'AM'][activity].astype(str).str.lower().eq('true').sum()
    pm_count = df[df['shift'] == 'PM'][activity].astype(str).str.lower().eq('true').sum()
    
    activity_by_shift = pd.concat([activity_by_shift, 
                                  pd.DataFrame({'Activity': [activity.capitalize()],
                                               'AM': [am_count], 
                                               'PM': [pm_count]})])

activity_long = pd.melt(activity_by_shift, 
                        id_vars=['Activity'],
                        value_vars=['AM', 'PM'],
                        var_name='Shift', 
                        value_name='Count')

activity_fig = px.bar(activity_long, 
                     x='Activity', 
                     y='Count', 
                     color='Shift', 
                     barmode='group',
                     title='Squirrel Activities by Time of Day',
                     labels={'Activity': 'Behavior', 'Count': 'Number of Squirrels'})
text("## Squirrel Activities")
text("Comparison of what squirrels are doing morning vs afternoon")
plotly(activity_fig)

interaction_columns = ['approaches', 'indifferent', 'runs_from']

interaction_by_shift = pd.DataFrame()

for interaction in interaction_columns:
    am_count = df[df['shift'] == 'AM'][interaction].astype(str).str.lower().eq('true').sum()
    pm_count = df[df['shift'] == 'PM'][interaction].astype(str).str.lower().eq('true').sum()
    
    interaction_by_shift = pd.concat([interaction_by_shift, 
                                  pd.DataFrame({'Interaction': [interaction.capitalize()],
                                               'AM': [am_count], 
                                               'PM': [pm_count]})])

interaction_long = pd.melt(interaction_by_shift, 
                        id_vars=['Interaction'],
                        value_vars=['AM', 'PM'],
                        var_name='Shift', 
                        value_name='Count')

interaction_fig = px.bar(interaction_long, 
                     x='Interaction', 
                     y='Count', 
                     color='Shift', 
                     barmode='group',
                     title='Squirrel Human Interactions by Time of Day',
                     labels={'Interaction': 'Behavior', 'Count': 'Number of Squirrels'})

text("## Squirrel Human Interactions")
text("Comparison of how squirrels interact with humans in morning vs afternoon")
plotly(interaction_fig)

fur_color_counts = df["primary_fur_color"].value_counts().reset_index()
fur_color_counts.columns = ["Fur Color", "Count"]
fur_color_fig = px.pie(fur_color_counts, values="Count", names="Fur Color", title="Squirrels by Fur Color")
text("## Squirrel Colors")
text("Comparison of the frequency of squirrel fur colors")
plotly(fur_color_fig)
