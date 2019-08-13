from flask import Flask, send_from_directory, render_template, request, redirect, url_for, flash
import pandas as pd
import joblib
from collections import Counter
import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_bootstrap_components as dbc



app = Flask(__name__, static_url_path='')
app.secret_key = 'random string'

df = pd.read_csv('dataclean.csv', index_col=0)
model = joblib.load('modelmobil1')
dfX = pd.read_csv('nilaiX.csv', index_col=0)

premium = df['car'][df['carClass'] == 4].unique()
high = df['car'][df['carClass'] == 3].unique()
normal = df['car'][df['carClass'] == 2].unique()
low = df['car'][df['carClass'] == 1].unique()


@app.route('/')
def welcome():
    listbrand = df['car'].unique()
    listsize = df['sizeCat'].unique()
    listeng = df['engType'].unique()
    drivetype = df['drive2'].unique()
    print(df.columns)

    return render_template('mobil2.html', brand=listbrand, size=listsize, mesin=listeng, drive=drivetype)


@app.route('/predictionresult', methods=['post'])
def hasil():
    try:
        brand = request.form['brand']
        jarak = request.form['jarak']
        tahun = request.form['tahun']
        volume = request.form['volume']
        size = request.form['size']
        drive = request.form['drive']
        mesin = request.form['mesin']
        regis = request.form['regis']

        if brand == "" or jarak == "" or tahun == "" or volume == "" or size == "" or drive == "" \
                or mesin == "" or regis == "":

            return render_template('mobil2.html', b='kosong')

        else:
            if brand in premium:
                carclass = 4
            elif brand in high:
                carclass = 3
            elif brand in normal:
                carclass = 2
            else:
                carclass = 1

            if size == 'big car':
                bigcar = 1
                mediumcar = 0
                smallcar = 0

            elif size == 'medium car':
                bigcar = 0
                mediumcar = 1
                smallcar = 0

            else:
                bigcar = 0
                mediumcar = 0
                smallcar = 1

            if drive == 'full':
                wd4 = 1
                wd2 = 0
            else:
                wd4 = 0
                wd2 = 1

            if mesin == 'Diesel':
                diesel = 1
                gas = 0
                other = 0
                petrol = 0
            elif mesin == 'Gas':
                diesel = 0
                gas = 1
                other = 0
                petrol = 0
            elif mesin == 'Other':
                diesel = 0
                gas = 0
                other = 1
                petrol = 0
            else:
                diesel = 0
                gas = 0
                other = 0
                petrol = 1
            if regis == 'yes':
                yes = 1
                no = 0
            else:
                yes = 0
                no = 1

            print(brand)
            print(jarak)
            print(tahun)
            print(volume)
            print(size)
            print(drive)
            print(mesin)
            print(carclass)
            print(regis)

            data = [float(jarak), float(tahun), float(volume), carclass, bigcar, mediumcar, smallcar, wd2,
                    wd4, diesel, gas, other, petrol, no, yes]
            prediksi = model.predict([data])[0]

            print(data)
            print(prediksi)

            # For Filter Recommendation ======================================================
            harga = df['price']
            dict1 = dict(harga)

            list1 = []
            for i in harga:
                harga = 100 - abs(i - prediksi) / 100
                list1.append(harga)

            i = 0
            for x in dict1.keys():
                dict1[x] = list1[i]
                i += 1

            c = dict(Counter(dict1).most_common())
            b = list(c.keys())[0:5]
            print(df[['model', 'price']].loc[b])

            dfrec = pd.DataFrame(columns=['car', 'model', 'year', 'mileage', 'price'], index=range(1, len(b) + 1))

            index = 0
            for i in b:
                dfrec.iloc[index, 0] = df['car'].loc[i]
                dfrec.iloc[index, 1] = df['model'].loc[i]
                dfrec.iloc[index, 2] = df['year'].loc[i]
                dfrec.iloc[index, 3] = df['mileage'].loc[i]
                dfrec.iloc[index, 4] = df['price'].loc[i]
                index += 1
            print(dfrec)

            return render_template('mobil2.html', a=round(prediksi), b='isi', brand1=brand, year1=tahun,jarak1=jarak, volume1=volume,
                                   size1=size, drive1=drive, mesin1=mesin, regis1=regis, rec=dfrec)

    except:
        return redirect(url_for('error'))

@app.route('/error')
def error():
    return render_template('error.html')



appdash = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN], server=app, routes_pathname_prefix='/historical/')


dfdash = pd.read_csv('datadash.csv', index_col=0)
df1 = pd.read_csv('dataclean.csv', index_col=0)

dfdash['id'] = dfdash['Car']
dfdash.set_index('id', inplace=True, drop=False)
text1 = str('This dataset contains data for more than 9.5K cars sale in Ukraine year 2016. '
            'Most of them are used cars so it opens the possibility to analyze features related to car operation.'
            ' But after cleaning and checking, we only use around 9.2K data, removing some outliers and bad data.'
            ' Based on this dataset, we try to predict Price with some features that car have. '
            'To check our source, click ')

source = 'https://www.kaggle.com/antfarol/car-sale-advertisements'

appdash.layout = html.Div([
        html.Div([html.Button(html.A('Home', href="http://127.0.0.1:5000/"),  style={'fontSize': 20, 'text-align': 'left', 'margin-left':5}), html.P('Dataset Information',
                                style={'font-family': "Comic Sans MS, sans-serif", 'fontSize': 30, 'text-align': 'center', 'margin-top': 5, 'margin-bottom': 10, 'fontWeight': 'bold'})],
                 style={'margin-top': 5, 'margin-bottom': 10}),

        html.Details([html.P([text1, html.A('Here', href=source, target="_blank")],
                             style={'fontSize': 20, 'font-family': "Comic Sans MS, sans-serif", 'margin-top': 5,  'margin-bottom': 15, "padding-left": 60}), html.Summary('Data set history')],
                     style={'fontSize': 25, 'width': '60%', 'margin-left': 10}),
        html.Div([
            html.Div(dash_table.DataTable(
                id='datatable-row-ids',
                columns=[
                    {'name': i, 'id': i, 'deletable': False} for i in dfdash.columns
                    # omit the id column
                    if i != 'id'
                    ],
                data=dfdash.to_dict('records'),
                editable=False,
                filter_action="native",
                sort_action="native",
                sort_mode='multi',
                row_selectable='multi',
                row_deletable=False,
                selected_rows=[],
                page_action='native',
                page_current=0,
                page_size=14,
                style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white', 'fontWeight': 'bold', 'fontSize': 18},
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'Car'},
                        'textAlign': 'left'
                    }],
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(200, 248, 250)'
                    }
                ],
                style_data={'fontSize': 18})
                , style={'width': '39%', 'display': 'inline-block', 'margin-left': 10}),
            html.Div([
                    dcc.Graph(
                        id='Piechart1',
                        figure=go.Figure(
                            data=[
                                go.Pie(
                                    labels=df1['drive2'].value_counts().index,
                                    values=df1['drive2'].value_counts().values,
                                    marker=dict(colors=['gold', 'mediumturquoise', 'darkorange'], line=dict(color='#000000', width=1)),
                                    textfont_size=25,

                                )],
                            layout=go.Layout(
                                title=go.layout.Title(
                                  text='Wheel Drive Category',
                                  font={
                                    'size': 25,
                                    'color': '#000000',
                                    'family': "Comic Sans MS, cursive, sans-serif"
                                  },
                                  x=0.5,
                                  y=0.99,

                                ),
                                showlegend=True,
                                legend=go.layout.Legend(x=0, y=1.0),
                                margin=go.layout.Margin(l=0, r=0, t=40, b=10),
                                font=dict(size=18, family="Comic Sans MS, cursive, sans-serif", color='#040302'),
                                height=500,)
                                # paper_bgcolor="lightblue",)
                        ))], style={'width': '30%', 'display': 'inline-block', 'margin-left': 5}),
            html.Div([
                dcc.Graph(
                    id='Piechart2',
                    figure=go.Figure(
                        data=[
                            go.Pie(
                                labels=df1['sizeCat'].value_counts().index,
                                values=df1['sizeCat'].value_counts().values,
                                marker=dict(line=dict(color='#000000', width=1)),
                                hole=0.2,
                                textfont_size=25
                                )],
                        layout=go.Layout(
                            title=go.layout.Title(
                                  text='Car Size Category',
                                  font = {
                                    'size': 25,
                                    'color': '#000000',
                                    'family': "Comic Sans MS, cursive, sans-serif"
                                  },
                                  x=0.5,
                                  y=0.99,
                                ),
                            showlegend=True,
                            legend=go.layout.Legend(x=0, y=1.0),
                            margin=go.layout.Margin(l=0, r=0, t=40, b=10),
                            font=dict(size=18, color='#040302'),
                            height=500,
                            # paper_bgcolor="lightblue",
                        )))], style={'width': '30%', 'display': 'inline-block', 'margin-left': 5})
        ],
                        style={'margin-top': 5, 'width': '100%', 'display': 'inline-block'}),

        dcc.Dropdown(id='dropdown1',
            options=[
                    {'label': i, 'value': i, } for i in dfdash.columns
                    if i != 'id' and i != 'Car'],
            multi=True,
            value="",
            style={'fontSize': 18, 'margin-top': 15},
            placeholder='Select your Graph'
            ),
        html.Div(id='datatable-row-ids-container', )
])


@appdash.callback(
    Output('datatable-row-ids-container', 'children'),
    [Input('datatable-row-ids', 'derived_virtual_row_ids'),
     Input('datatable-row-ids', 'selected_row_ids'),
     Input('datatable-row-ids', 'active_cell'),
     Input('dropdown1', 'value')])
def update_graphs(row_ids, selected_row_ids, active_cell, value):
    selected_id_set = set(selected_row_ids or [])

    if row_ids is None:
        dfdashf = dfdash
        # pandas Series works enough like a list for this to be OK
        row_ids = dfdash['Car']
    else:
        dfdashf = dfdash.loc[row_ids]

    active_row_id = active_cell['row_id'] if active_cell else None
    colors = ['#FF69B4' if id == active_row_id
              else '#FF0000' if id in selected_id_set
              else '#0074D9'
              for id in row_ids]

    return html.Div([
        dcc.Graph(
            id=column + '--row-ids',
            figure={
                'data': [
                    {
                        'x': dfdashf['Car'],
                        'y': dfdashf[column],
                        'type': 'bar',
                        'marker': {'color': colors},
                    }
                ],
                'layout': {
                    'xaxis': {
                        'automargin': True,
                        },
                    'yaxis': {
                        'automargin': True,
                        'title': {'text': column},
                        'gridcolor': '#faf7f7'},
                    'height': 450,
                    'margin': {'t': 15, 'l': 10, 'r': 10},
                    'plot_bgcolor': '#e3e3e3',
                },
            },
        )
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        for column in value if column in dfdashf])


if __name__ == '__main__':
    app.run(debug=True)




