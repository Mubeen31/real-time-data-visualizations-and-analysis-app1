import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input
import pandas as pd
from datetime import datetime

metaTags = [
    {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5'}]

app = dash.Dash(__name__, meta_tags=metaTags)

app.layout = html.Div([

    dcc.Interval(id='update_value',
                 interval=1 * 16000,
                 n_intervals=0),

    html.Div([
        html.Div([

            html.Div([
                html.Img(src=app.get_asset_url('real-time.png'),
                         className='image'),
                html.Div('Real Time Data Visualizations and Analysis',
                         className='title_text')
            ], className='title_image_row'),

            html.Div([
                html.Div('Sensor location:'),
                html.Div('Walsall, England', className='location_name')
            ], className='location_row'),

            html.Div(id='data_update_time')

        ], className='title_background twelve columns')
    ], className='row'),

    html.Div([
        html.Div([
            html.Div(id='temp', className='card_bg'),
            html.Div(id='hum', className='card_bg'),
            html.Div(id='light_intensity', className='card_bg'),
            html.Div(id='co2', className='card_bg'),
        ], className='temp_humidity eight columns')
    ], className='display_row_center row'),

])


@app.callback(Output('data_update_time', 'children'),
              [Input('update_value', 'n_intervals')])
def update_value(n_intervals):
    url = 'https://api.thingspeak.com/channels/2007583/fields/1/last.csv'
    df = pd.read_csv(url)
    date_time = df['created_at'].iloc[0]
    get_date_time = datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%SZ')
    last_date_time = get_date_time.strftime('%Y-%m-%d %H:%M:%S')

    return [
        html.Div([
            html.Div('Last data update time:'),
            html.Div(last_date_time, className='location_name')
        ], className='date_time_row')
    ]


@app.callback(Output('temp', 'children'),
              [Input('update_value', 'n_intervals')])
def update_value(n_intervals):
    url = 'https://api.thingspeak.com/channels/2007583/fields/2/last.csv'
    df = pd.read_csv(url)
    df_temp = df['field2'].iloc[0]

    return [
        html.Div([
            html.Img(src=app.get_asset_url('hot.png'),
                     style={'height': '50px'}),
            html.Div([
                html.Div('°C', className='symbol'),
                html.Div('{0:.1f}'.format(df_temp),
                         className='numeric_value')
            ], className='temp_symbol_column')
        ], className='temp_image_row'),

        html.P('Temperature', style={'color': '#666666',
                                     'margin-top': '-10px'})
    ]


@app.callback(Output('hum', 'children'),
              [Input('update_value', 'n_intervals')])
def update_value(n_intervals):
    url = 'https://api.thingspeak.com/channels/2007583/fields/1/last.csv'
    df = pd.read_csv(url)
    df_hum = df['field1'].iloc[0]

    return [
        html.Div([
            html.Img(src=app.get_asset_url('humidity.png'),
                     style={'height': '50px'}),
            html.Div([
                html.Div('%', className='symbol'),
                html.Div('{0:.1f}'.format(df_hum),
                         className='numeric_value')
            ], className='temp_symbol_column')
        ], className='temp_image_row'),

        html.P('Humidity', style={'color': '#666666',
                                  'margin-top': '-10px'})
    ]


@app.callback(Output('light_intensity', 'children'),
              [Input('update_value', 'n_intervals')])
def update_value(n_intervals):
    url = 'https://api.thingspeak.com/channels/2007583/fields/3/last.csv'
    df = pd.read_csv(url)
    df_light_inten = df['field3'].iloc[0]

    return [
        html.Div([
            html.Img(src=app.get_asset_url('sunny.png'),
                     style={'height': '50px'}),
            html.Div([
                html.Div('lux', className='symbol'),
                html.Div('{0:.1f}'.format(df_light_inten),
                         className='numeric_value')
            ], className='temp_symbol_column')
        ], className='temp_image_row'),

        html.P('Light Intensity', style={'color': '#666666',
                                         'margin-top': '-10px'})
    ]


@app.callback(Output('co2', 'children'),
              [Input('update_value', 'n_intervals')])
def update_value(n_intervals):
    url = 'https://api.thingspeak.com/channels/2007583/fields/4/last.csv'
    df = pd.read_csv(url)
    df_co2 = df['field4'].iloc[0]

    return [
        html.Div([
            html.Img(src=app.get_asset_url('co2.png'),
                     style={'height': '50px'}),
            html.Div([
                html.Div('ppm', className='symbol'),
                html.Div('{0:.0f}'.format(df_co2),
                         className='numeric_value')
            ], className='temp_symbol_column')
        ], className='temp_image_row'),

        html.P('CO2 Level in Air', style={'color': '#666666',
                                          'margin-top': '-10px'})
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
