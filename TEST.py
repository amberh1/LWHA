import dash
from dash import dcc, html, Input, Output, State

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Tab 1', value='tab-1', children=[
            dcc.Input(id='input1', placeholder='Required field', type='text')
        ]),
        dcc.Tab(label='Tab 2', value='tab-2', children=[
            dcc.Input(id='input2', placeholder='Required field', type='text')
        ])
    ]),
    html.Button('Submit', id='submit-btn'),
    html.Div(id='error-msg')
])

@app.callback(
    [Output('tabs', 'value'),
     Output('error-msg', 'children')],
    Input('submit-btn', 'n_clicks'),
    [State('input1', 'value'),
     State('input2', 'value')]
)
def validate_form(n_clicks, input1, input2):
    if n_clicks:
        if not input1:
            return 'tab-1', 'Please complete the required field in Tab 1.'
        elif not input2:
            return 'tab-2', 'Please complete the required field in Tab 2.'
        return dash.no_update, 'Form submitted successfully!'
    return dash.no_update, dash.no_update

if __name__ == '__main__':
    app.run_server(debug=True)
