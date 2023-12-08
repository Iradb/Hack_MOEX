import dash
from dash import html,dcc
from dash.dependencies import Input, Output, State
from dash import callback
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px
background_Graph = '#2C304D'
paper_backgroud="#252946"
size = '13'
color_green = '#3d9970'
color = 'black'
def get_callback(app,data,ML_d):
    @app.callback(
        Output('id_list_none', 'style'),
        [Input('all_stock', 'n_clicks')])
    def call_display_stocks(n_clicks):
        if n_clicks is not None and n_clicks % 2 == 1:
            return {"display":"block"}
        else:
            return {"display":"none"}
    @app.callback(Output("stocks_val","children"),
                  Output("Graphic_obzor",'figure'),
                  Output("Change_price","children"),
                  State("Date_time","value"),
                  [Input(key,"n_clicks") for key,value in data.dict_name.items()])
    def something_do(*value):
        print(*value)
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        value_one = value[0]
        # button_number = int(changed_id.split('.')[0].split('-')[-1])
        if changed_id.replace(".n_clicks","") == ".":
            return ["",{ 'layout': {'font':{'color': color, 'size': size}
            }},""]
        ticket = data.dict_name[changed_id.replace(".n_clicks","")]
        data_back = data.load_data_from_url(changed_id.replace(".n_clicks",""),value_one)
        last_val_change = data_back["pr_change"].values[-1]
        print(data_back["pr_change"])
        last_val_change = "Изменение цены за"+str(value[1])+" % "+str(last_val_change)
        figure = {
            'data': [
                go.Scatter(x=(data_back['tradedate']),
                    y=data_back['pr_open'],
                    mode='lines+markers'),
                
            ],
            'layout': {
                'xaxis':{"type":'array',
                         "tickvals":data_back['tradedate'][::3],
                        #  "ticktext":data_back['tradedate'].dt.strftime('%Y-%m-%d').where(data_back['tradedate'].diff().dt.days != 0, data_back['tradedate'].dt.strftime('%H:%M')),
                        "ticktext":data_back['tradedate'].dt.strftime('%H:%M').where((data_back['tradedate'] -data_back['tradedate'].shift(1)).dt.days != 0, data_back['tradedate'].dt.strftime('%Y-%m-%d %H:%M')),
                         "tickangle":"-55"}
            }
        }

        return [ticket,figure,last_val_change]
    

    @app.callback(Output("Graphic_obzor_r","figure"),
                  Output("Right_table","columns"),
                  Output("Right_table","data"),
                  Output("Right_table","style_data_conditional"),
                  Input("Obzor","value"),
                  Input("DropDown","value"),)
    def change_drop_down(*value):
        print(value)
        if value[1] != None:
            data_back = data.load_data_from_url(value[1],1,value[0])
            if value[0] == "Svecha":
                style_data_conditional=[
            {
                'if': {'filter_query': '{pr_change} > 0'},
                'color': f'{color_green}'
            },
            {
                'if': {'filter_query': '{pr_change} < 0'},
                'color': 'red'
            }]
                figure = {
                        'data' : [
                                    go.Ohlc(x=data_back['tradedate'],
                                                open=data_back["pr_open"],
                                                high=data_back["pr_high"],
                                                low=data_back["pr_low"],
                                                close=data_back["pr_close"])
                                ],
                        'layout': {
                            "title": "Свечной график - Текущая сессия",
                            'xaxis':{"type":'time',
                                    #  "ticktext":data_back['tradedate'].dt.strftime('%Y-%m-%d').where(data_back['tradedate'].diff().dt.days != 0, data_back['tradedate'].dt.strftime('%H:%M')),
                                    "tickangle":"-55"}
                                }
                            }
                return [figure,[{"name":value,"id":key } for key,value in {'tradetime':'Время','pr_open':'Цена открытия','pr_close':'Цена закрытия','pr_change':'Изменение цены %'}.items()],data_back[['tradetime','pr_open','pr_close','pr_change']].to_dict("records"),style_data_conditional]
            


            elif value[0] == "Obzor":
                # data_back['Color'] = data_back['pr_change'].apply(lambda x: 'green' if x > 0 else 'red')
                # # style_data_conditional = table_value_red_green(data_back,"pr_change")
                style_data_conditional=[
            {
                'if': {'filter_query': '{pr_change} > 0'},
                'color': f'{color_green}'
            },
            {
                'if': {'filter_query': '{pr_change} < 0'},
                'color': 'red'
            }]
                figure = {
                    'data': [
                        go.Scatter(x=(data_back['tradedate']),
                            y=data_back['pr_close'],
                            mode='lines+markers'),
                    ],
                    'layout': {
                        "title": "График закрытия - Текущая сессия",
                        'xaxis':{"type":'time',
                                #  "ticktext":data_back['tradedate'].dt.strftime('%Y-%m-%d').where(data_back['tradedate'].diff().dt.days != 0, data_back['tradedate'].dt.strftime('%H:%M')),
                                # "ticktext":data_back['tradedate'].dt.strftime('%H:%M').where((data_back['tradedate'] -data_back['tradedate'].shift(1)).dt.days != 0, data_back['tradedate'].dt.strftime('%Y-%m-%d %H:%M')),
                                "tickangle":"-55"}
                    }}
                return [figure,[{"name":value,"id":key } for key,value in {'tradetime':'Время','pr_close':'Цена закрытия','pr_change':'Изменение цены %'}.items()],data_back[['tradetime','pr_close','pr_change']].to_dict("records"),style_data_conditional]
            elif value[0] == "Stakan":
                figure = {
                    # 'data': [
                    #     ff.create_distplot(hist_data=[data_back["put_orders_b"],data_back["put_orders_s"]],group_labels=["Открытие","Закрытие"],
                    #                                  colors=['#2BCDC1', '#F66095'])
                    # ],
                    'data': [
                        go.Scatter(y=data_back["put_val_b"], x=data_back["put_val"],mode='lines+markers'),
                        go.Scatter(y=data_back["put_val_s"], x=data_back["put_val"],mode='lines+markers')
                    ],
                    'layout': {
                        "title": "Биржевой стакан - Текущая сессия",
                    }}
                return [figure,[{"name":value,"id":key } for key,value in {'put_val_b':'Сделок на покупку','put_val_s':'Сделок на продажу','put_val':'Объем в деньгах'}.items()],data_back[['put_val_b','put_val_s','put_val']].to_dict("records"),[{}]]
                    # "pr_open","pr_high","pr_low","pr_close","pr_change"
        else:
            return [{'data': [], 'layout': {'font':{'color': color, 'size': size}}},[{"name":" ","id":"1"}],[{}],[{}]]


    def table_value_red_green(data,columns):
        style_data_conditional = []
        for row in data[columns]:
            if row > 0:
                style_data_conditional.append({'if': {'row_index': row}, 'color': 'green'})
            else:
                style_data_conditional.append({'if': {'row_index': row}, 'color': 'red'})
        return style_data_conditional

    @app.callback(Output("Name_stocks","children"),
                  Output("One_graph",'figure'),
                  Output("Second_graph",'figure'),
                  Input("DropDown","value"))
    def something_new_do(value):
        if value is not None:
            ticket = data.dict_name[value]
            data_ML = ML_d.show(value)
            figure = {
            'data': [
                go.Scatter(x=(data_ML['tradetime']),
                    y=data_ML['PrognozValAbs'],
                    mode='lines+markers',name="Прогноз"),
                go.Scatter(x=data_ML['tradetime'],y=data_ML['pr_close'],mode='lines+markers',name="Торги")
            ],
            'layout': {
                "title": "Прогноз и тренд прошлой сессии",
                'xaxis':{"type":'time',
                        #  "ticktext":data_back['tradedate'].dt.strftime('%Y-%m-%d').where(data_back['tradedate'].diff().dt.days != 0, data_back['tradedate'].dt.strftime('%H:%M')),
                         "tickangle":"-55"}
            }
        }
            figure_1 = {
            'data': [
                go.Scatter(x=(data_ML['tradetime']),
                    y=data_ML['PrognozNewAbs'],
                    mode='lines+markers',name="Прогноз"),
            ],
            'layout': {
                "title":'Прогноз на след. сессию',
                'xaxis':{"type":'time',
                        #  "ticktext":data_back['tradedate'].dt.strftime('%Y-%m-%d').where(data_back['tradedate'].diff().dt.days != 0, data_back['tradedate'].dt.strftime('%H:%M')),
                         "tickangle":"-55"}
            }
        }
            return [str(ticket),figure,figure_1]
        else:
            return ["",{ 'layout': {'font':{'color': color, 'size': size}
            }},{ 'layout': {'font':{'color': color, 'size': size}
            }}]