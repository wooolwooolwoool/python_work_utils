import japanize_matplotlib
import matplotlib
matplotlib.use('agg')
from common.path import *
from common.graphplot import *
import panel as pn
import pandas as pd
import matplotlib.pyplot as plt

# おまじない
pn.extension()

df = None

# figure（描画領域）の定義
fig1 = plt.figure()
# axes（グラフ）の定義
ax1 = fig1.add_subplot(1,1,1)

# テキスト（ファイルパス）を入力するウィジェットの定義
# ファイルパスを入力するウィジェットとしてTextAreaInputを使用する
filename_input = pn.widgets.TextAreaInput(name="CSVファイルパス入力", placeholder="ここにCSVファイルのパスを入力")

# ファイル読み込みボタンの定義
load_file_but = pn.widgets.Button(name="ファイル読み込み", button_type= "primary", width=140)
load_file_maxmin = pn.pane.Str()

# MarkerStyleのmarkersを取得
markers_list = [""]
markers_dict = matplotlib.markers.MarkerStyle.markers
markers = [key for key in markers_dict.keys() if isinstance(key, str) and not key.isdigit() and key not in ['None', ' ', '']]
markers_list.extend(list(markers))

# Line2DのlineStyles辞書を取得
linestyles_list = [""]
linestyles_dict = matplotlib.lines.Line2D.lineStyles
linestyles = [key for key in linestyles_dict.keys() if isinstance(key, str) and key not in ['None', ' ', '']]
linestyles_list.extend(list(linestyles))

# X軸、Y軸を選択するセレクトウィジェットの定義
graph_mark_sel = pn.widgets.Select(name="マーカー種類", width=140, options=markers_list, value="")
graph_line_sel = pn.widgets.Select(name="ライン種類", width=140, options=linestyles_list, value="")
graph_mark_size = pn.widgets.IntInput(name="マーカーサイズ", value=1, step=1, start=1, width=140)
graph_line_width = pn.widgets.IntInput(name="ライン幅", value=1, step=1, start=1, width=140)
x_axis_not_use = pn.widgets.Checkbox(name="X軸を指定しない")
x_axis_sel = pn.widgets.Select(name="X軸", width=300)
x_axis_datetime = pn.widgets.Checkbox(name="X軸がDatetime")
x_axis_datetime_format = pn.widgets.TextInput(name="Datetimeフォーマット", width=300, value="%Y%m%d %H%M%S")
y_axis_sel = pn.widgets.Select(name="Y軸_1", width=300)
add_button = pn.widgets.Button(name="追加", button_type="default")
del_button = pn.widgets.Button(name="削除", button_type="default")
x_label_sel = pn.widgets.TextInput(name="X軸ラベル", width=300)
y_label_sel = pn.widgets.TextInput(name="Y軸ラベル", width=300)
graph_fig_w = pn.widgets.IntInput(name="グラフ幅", value=8, step=1, start=1, end=5000, width=140)
graph_fig_h = pn.widgets.IntInput(name= "グラフ高さ", value=6, step=1, start=1, end=5000, width=140)
num_divx = pn.widgets.IntInput(name= "X軸分割数", value=6, step=1, start=1, end=5000, width=140)
num_divy = pn.widgets.IntInput(name= "Y軸分割数", value=6, step=1, start=1, end=5000, width=140)
graph_range_autoset_button = pn.widgets.Button(name="下限上限を自動セット", button_type="default")
graph_x_u = pn.widgets.FloatInput(name="X軸上限", value=None, step=0.001, width=140)
graph_x_l = pn.widgets.FloatInput(name="X軸下限", value=None, step=0.001, width=140)
graph_x_u_datetime = pn.widgets.DatetimePicker(name="X軸上限 Datetime", disabled= True, width=140)
graph_x_l_datetime = pn.widgets.DatetimePicker(name="X軸下限 Datetime", disabled= True, width=140)
graph_y_u = pn.widgets.FloatInput(name="Y軸上限", value=None, step=0.001, width=140)
graph_y_l = pn.widgets.FloatInput(name="Y軸下限", value=None, step=0.001, width=140)
graph_range_round_button = pn.widgets.Button(name="Y軸範囲を丸める", button_type="default")

# グラフ表示領域の幅、高さ
graph_w = pn.widgets.IntInput(name="幅", value=1200, step=1, start=1, end=5000)
graph_h = pn.widgets.IntInput(name= "高さ", value=900, step=1, start=1, end=5000)

# グラフを描画するボタンの定義
display_graph_but = pn.widgets.Button(name= "グラフ描画", button_type= "primary", width=140, disabled= True)
graph_update_but = pn.widgets.Button(name= "グラフ更新", button_type= "primary", width=140, disabled= True)

# グラフ（HoloViews）描画パネルの定義
# データ未入力だとウィジェットエラー出るので仮のグラフデータ格納
blank_hv = fig1
graph_pane = pn.pane.Matplotlib(blank_hv, visible = False)

wb2_input = pn.Column()
col_name = []

# ファイル読み込みのイベント関数規定
def load_file(event):
    try:
        global df
        global col_name
        # csvファイルをデータフレームとして読み込み
        filename_input.value = filename_input.value.replace('"', "")
        df = pd.read_csv(convert_to_wsl_path(filename_input.value))
        # 読み込んだCSVデータフレームの列名を取得
        col_name = list(df.columns)
        # 軸項目の選択肢を設定
        x_axis_sel.options = col_name
        y_axis_sel.options = col_name
        load_file_maxmin.object = ""
        for col in df.columns:
            load_file_maxmin.object += "{}: max {}, min {}\n".format(col, df[col].max(), df[col].min())
        # グラフ描画ボタンの無効化を解除
        display_graph_but.disabled = False 
        # ボタンの色を変更
        load_file_but.button_type = "success"
    except:
        load_file_but.button_type = "danger"

def add_data(event):
    """ データ追加 """
    num = len(wb2_input)
    input_widget = pn.widgets.Select(name=f"Y軸_{num}", width=300)
    input_widget.options = col_name
    wb2_input.append(input_widget)

def del_data(event):
    """ データ削除 """
    if len(wb2_input) > 2:
        wb2_input.pop(-1)

@pn.depends(x_axis_sel.param.value)
def sele_x(s):
    x_label_sel.value = s
    return 

@pn.depends(y_axis_sel.param.value)
def sele_y(s):
    y_label_sel.value = s
    return 

@pn.depends(x_axis_not_use.param.value)
def sele_use_x(s):
    x_axis_sel.disabled = s
    x_axis_datetime_format.disabled = s
    x_axis_datetime.disabled = s
    if x_axis_datetime.value:
        x_axis_datetime.value = False
    return 

@pn.depends(x_axis_datetime.param.value)
def sele_x_axis_datetime(s):
    graph_x_u_datetime.disabled = not s
    graph_x_l_datetime.disabled = not s
    graph_x_u.disabled = s
    graph_x_l.disabled = s
    return 

def get_y_minmax(widgets):
    y_min = None
    y_max = None
    for input_widget in widgets:
        if y_min is not None:
            y_min = min(df[input_widget.value].min(), y_min)
            y_max = max(df[input_widget.value].max(), y_max)
        else:
            y_min = df[input_widget.value].min()
            y_max = df[input_widget.value].max()
    return y_min, y_max

def graph_range_autoset(event):
    if x_axis_not_use.value:
        if graph_x_u.value is None:
            graph_x_u.value = len(df[wb2_input[0].value])
        if graph_x_l.value is None:
            graph_x_l.value = 0
    else:
        if x_axis_datetime.value:
            tmp = pd.to_datetime(df[wb2_input[0].value], format=x_axis_datetime_format.value)
            if graph_x_u_datetime.value is None:
                graph_x_u_datetime.value = tmp.max()
            if graph_x_l_datetime.value is None:
                graph_x_l_datetime.value = tmp.min()
        else:
            if graph_x_u.value is None:
                graph_x_u.value = df[wb2_input[0].value].max()
            if graph_x_l.value is None:
                graph_x_l.value = df[wb2_input[0].value].min()
    y_min, y_max = get_y_minmax(wb2_input[1:])
    graph_y_l.value = y_min
    graph_y_u.value = y_max
    return 

def round_min_max(event):
    y_min, y_max = round_to_nearest(graph_y_l.value, graph_y_u.value)    
    graph_y_l.value = y_min
    graph_y_u.value = y_max
    return

# グラフ描画のイベント関数規定
def display_graph(event):
    try:
        display_graph_but.disabled = True 
        display_graph_but.name = "描画中..."
        # figure（描画領域）の定義
        fig1 = plt.figure(figsize=(graph_fig_w.value, graph_fig_h.value))
        # axes（グラフ）の定義
        ax1 = fig1.add_subplot(1,1,1)

        x_col = ""
        # 描画するグラフデータの生成    
        for input_widget in wb2_input:
            if x_col  == "":
                x_col = input_widget.value
                if x_axis_datetime.value:
                    df[input_widget.value] = pd.to_datetime(df[input_widget.value], format=x_axis_datetime_format.value)
            else:
                if x_axis_not_use.value:
                    ax1.plot(range(len(df[input_widget.value])), df[input_widget.value], graph_mark_sel.value + graph_line_sel.value,
                            markersize=graph_mark_size.value, linewidth=graph_line_width.value,
                            label=input_widget.value)            
                else:
                    ax1.plot(df[x_col], df[input_widget.value], graph_mark_sel.value + graph_line_sel.value,
                            markersize=graph_mark_size.value, linewidth=graph_line_width.value,
                            label=input_widget.value)

        y_min, y_max = get_y_minmax(wb2_input[1:])

        if x_label_sel.value != "":
            ax1.set_xlabel(x_label_sel.value)
        if y_label_sel.value != "":
            ax1.set_ylabel(y_label_sel.value)

        if x_axis_datetime.value:
            x_max = graph_x_u_datetime.value
            x_min = graph_x_l_datetime.value
        else:
            x_max = graph_x_u.value
            x_min = graph_x_l.value

        ax1.set_xlim(x_min, x_max)
        ax1.set_ylim(graph_y_l.value, graph_y_u.value)
        ax1.set_xticks(divide_ticks(x_min, x_max, num_divx.value))
        ax1.set_yticks(divide_ticks(graph_y_l.value, graph_y_u.value, num_divy.value))

        ax1.legend()
        # ウィジェットで描画するグラフデータの指定と表示
        graph_pane.object = fig1
        # ボタンの色を変更
        display_graph_but.button_type = "success"
    except:
        display_graph_but.button_type = "danger"
    display_graph_but.disabled = False 
    display_graph_but.name = "グラフ描画"
    graph_pane.visible = True
    graph_update_but.disabled = False 

# グラフ描画のイベント関数規定
def graph_update(event):        
    graph_pane.width = graph_w.value
    graph_pane.height = graph_h.value

# ファイル読み込みボタンへのイベント登録
load_file_but.on_click(load_file)
# グラフ出力ボタンへのイベント登録
display_graph_but.on_click(display_graph)
graph_update_but.on_click(graph_update)
add_button.on_click(add_data)
del_button.on_click(del_data)
graph_range_autoset_button.on_click(graph_range_autoset)
graph_range_round_button.on_click(round_min_max)

# ボタンサイズの指定
load_file_but.width = display_graph_but.width = 150
# グラフパネルのサイズ指定
graph_pane.width = graph_w.value
graph_pane.height = graph_h.value

# ウィジェットボックスwb1へファイル読み込み関するウィジェットを格納
wb1 = pn.WidgetBox("# ファイル読み込み", filename_input, load_file_but, load_file_maxmin)
# ウィジェットボックスwb2へグラフ読み込みに関するウィジェットを格納
wb2 = pn.WidgetBox("# グラフ出力", 
                   "### プロットするデータ", x_axis_not_use, x_axis_datetime, x_axis_datetime_format,
                   wb2_input, pn.Row(add_button, del_button), 
                   "### プロット設定", 
                   pn.Row(graph_mark_sel, graph_line_sel), 
                   pn.Row(graph_mark_size, graph_line_width), 
                   x_label_sel, y_label_sel, 
                   pn.Row(num_divx, num_divy), 
                   pn.Row(graph_fig_w, graph_fig_h),
                   graph_range_autoset_button,
                   pn.Row(graph_x_l, graph_x_u),
                   pn.Row(graph_x_l_datetime, graph_x_u_datetime),
                   pn.Row(graph_y_l, graph_y_u),
                   graph_range_round_button,
                   display_graph_but, visible= True)
wb2_input.extend([x_axis_sel, y_axis_sel])
wb3 = pn.WidgetBox("# グラフ表示更新", graph_w, graph_h, graph_update_but, visible= True)
wb999 = pn.WidgetBox(sele_x, sele_y, sele_use_x, sele_x_axis_datetime, visible= False)

# 出力
dashboard_layout = pn.Row(pn.Column(wb1, wb2, wb3, wb999), graph_pane)

dashboard_layout.servable()
