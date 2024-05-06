import matplotlib
matplotlib.use('agg')
from common.path import *
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
load_file_but = pn.widgets.Button(name="ファイル読み込み", button_type= "primary", width=150)

# X軸、Y軸を選択するセレクトウィジェットの定義
graph_mark_sel = pn.widgets.Select(name="マーカー種類", width=150, options=["", ".", "^"], value="")
graph_line_sel = pn.widgets.Select(name="ライン種類", width=150, options=["", "-", "--"], value="")
graph_mark_size = pn.widgets.IntInput(name="マーカーサイズ", value=1, step=1, start=1, width=150)
graph_line_width = pn.widgets.IntInput(name="ライン幅", value=1, step=1, start=1, width=150)
x_axis_not_use = pn.widgets.Checkbox(name="X軸を使用しない")
x_axis_sel = pn.widgets.Select(name="X軸", width=300)
y_axis_sel = pn.widgets.Select(name="Y軸_1", width=300)
add_button = pn.widgets.Button(name="追加", button_type="default")
del_button = pn.widgets.Button(name="削除", button_type="default")
x_label_sel = pn.widgets.TextAreaInput(name="X軸ラベル", width=300)
y_label_sel = pn.widgets.TextAreaInput(name="Y軸ラベル", width=300)
graph_fig_w = pn.widgets.IntInput(name="グラフ幅", value=8, step=1, start=1, end=5000, width=150)
graph_fig_h = pn.widgets.IntInput(name= "グラフ高さ", value=6, step=1, start=1, end=5000, width=150)
graph_x_u = pn.widgets.FloatInput(name="X軸上限", value=None, step=0.001, width=150)
graph_x_l = pn.widgets.FloatInput(name="X軸下限", value=None, step=0.001, width=150)
graph_y_u = pn.widgets.FloatInput(name="Y軸上限", value=None, step=0.001, width=150)
graph_y_l = pn.widgets.FloatInput(name="Y軸下限", value=None, step=0.001, width=150)

# グラフ表示領域の幅、高さ
graph_w = pn.widgets.IntInput(name="幅", value=1000, step=1, start=1, end=5000)
graph_h = pn.widgets.IntInput(name= "高さ", value=600, step=1, start=1, end=5000)

# グラフを描画するボタンの定義
display_graph_but = pn.widgets.Button(name= "グラフ描画", button_type= "primary", width=150, disabled= True)
graph_update_but = pn.widgets.Button(name= "グラフ更新", button_type= "primary", width=150, disabled= True)

# グラフ（HoloViews）描画パネルの定義
# データ未入力だとウィジェットエラー出るので仮のグラフデータ格納
blank_hv = fig1
graph_pane = pn.pane.Matplotlib(blank_hv, visible = False)

wb2_input = pn.Column()
col_name = []

# ファイル読み込みのイベント関数規定
def load_file(event):
    global df
    global col_name
    # csvファイルをデータフレームとして読み込み
    df = pd.read_csv(convert_to_wsl_path(filename_input.value))
    # 読み込んだCSVデータフレームの列名を取得
    col_name = list(df.columns)
    # 軸項目の選択肢を設定
    x_axis_sel.options = col_name
    y_axis_sel.options = col_name
    # グラフ描画ボタンの無効化を解除
    display_graph_but.disabled = False 
    # ボタンの色を変更
    load_file_but.button_type = "success"

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

# グラフ描画のイベント関数規定
def display_graph(event):
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
        else:
            if x_axis_not_use.value:
                ax1.plot(range(len(df[input_widget.value])), df[input_widget.value], graph_mark_sel.value + graph_line_sel.value,
                         markersize=graph_mark_size.value, linewidth=graph_line_width.value,
                         label=input_widget.value)            
            else:
                ax1.plot(df[x_col], df[input_widget.value], graph_mark_sel.value + graph_line_sel.value,
                         markersize=graph_mark_size.value, linewidth=graph_line_width.value,
                         label=input_widget.value)
    if x_label_sel.value != "":
        ax1.set_xlabel(x_label_sel.value)
    if y_label_sel.value != "":
        ax1.set_ylabel(y_label_sel.value)
    ax1.set_xlim(graph_x_l.value, graph_x_u.value)
    ax1.set_ylim(graph_y_l.value, graph_y_u.value)

    ax1.legend()
    # ウィジェットで描画するグラフデータの指定と表示
    graph_pane.object = fig1
    # ボタンの色を変更
    display_graph_but.button_type = "success"
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

# ボタンサイズの指定
load_file_but.width = display_graph_but.width = 150
# グラフパネルのサイズ指定
graph_pane.width = graph_w.value
graph_pane.height = graph_h.value

# ウィジェットボックスwb1へファイル読み込み関するウィジェットを格納
wb1 = pn.WidgetBox("# ファイル読み込み", filename_input, load_file_but)
# ウィジェットボックスwb2へグラフ読み込みに関するウィジェットを格納
wb2 = pn.WidgetBox("# グラフ出力", 
                   "### プロットするデータ", x_axis_not_use, 
                   wb2_input, pn.Row(add_button, del_button), 
                   "### プロット設定", pn.Row(graph_mark_sel, graph_line_sel), 
                   pn.Row(graph_mark_size, graph_line_width), 
                   x_label_sel, y_label_sel, pn.Row(graph_fig_w, graph_fig_h),
                   pn.Row(graph_x_l, graph_x_u),
                   pn.Row(graph_y_l, graph_y_u),
                   display_graph_but, visible= True)
wb2_input.extend([x_axis_sel, y_axis_sel])
wb3 = pn.WidgetBox("# グラフ表示更新", graph_w, graph_h, graph_update_but, visible= True)

# 出力
dashboard_layout = pn.Row(pn.Column(wb1, wb2, wb3), graph_pane)

dashboard_layout.servable()
