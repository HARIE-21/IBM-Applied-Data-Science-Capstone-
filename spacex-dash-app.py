# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)
launch_sites = []
launch_sites.append({'label': 'All Sites', 'value': 'All Sites'})
for item in spacex_df["Launch Site"].value_counts().index:
    launch_sites.append({'label': item, 'value': item})

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options=launch_sites,value="All Sites",placeholder="Select a Launch Site here", searchable= True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0,max=16000,step=1000,value=[min_payload,max_payload], marks={ 2500:{'label':'2500 (Kg)'},5000:{'label':'5000(Kg)'},7500:{'label':'7500 (Kg)'},10000:{'label':'10000(Kg)'},12500:{'label':'12500(Kg)'},15000:{'label':'15000(Kg)'}}),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart',component_property='figure'),
              Input(component_id='site-dropdown',component_property='value')  ) 

def feature(input_value):
    if input_value == 'All Sites':
        df=spacex_df.groupby(['Launch Site'])['class'].sum().to_frame()
        df=df.reset_index()
        fig=px.pie(df,values='class',names='Launch Site',title='Total Success Launches for'+input_value)
    else:
        df=spacex_df[spacex_df["Launch Site"] == input_value]["class"].value_counts().to_frame
        df["name"]=["Success","Failure"]
        fig=px.pie(df,values='class',names='name',title='Total Success Launches for'+ input_value)
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
              Input(component_id='site-dropdown',component_property='value'),Input(component_id='payload-slider',component_property='value')
)                 

def plot(input1,input2):
    print(input1)
    print(input2)
    if input1=='All Sites':
       df1=spacex_df 
       df2=df1[df1["Payload Mass (kg)"] >= input2[0]]
       df3=df2[df1["Payload Mass (kg)"] <= input2[1]]
       fig2=px.scatter(df3,y="class",x="Payload Mass (kg)",color="Booster Version Category",title='Success and Failure outcomes for selected Payload Mass at all Launch sites')
    else:
        df1=spacex_df[spacex_df["Launch Site"]==input1] 
        df2=df1[df1["Payload Mass (kg)"] >= input2[0]]
        df3=df2[df1["Payload Mass (kg)"] <= input2[1]]
        fig2=px.scatter(df3,y="class",x="Payload Mass (kg)",color="Booster Version Category",title='Success and Failure outcomes for selected Payload Mass at all Launch sites')
    return fig2
    

# Run the app
if __name__ == '__main__':
    app.run(debug=True,port=8051)
