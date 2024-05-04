from common.path import *
import os
import shutil
import panel as pn
import traceback

pn.extension()

# テキスト入力用ウィジェット定義
input_dir = pn.widgets.TextInput(name="リネーム対象ファイル格納先", placeholder=r"C:\Users\user\Files")
output_dir = pn.widgets.TextInput(name="リネーム後ファイル格納先", placeholder=r"C:\Users\user\Files")
prefix_input = pn.widgets.TextInput(name="接頭語", placeholder="prefix_", width=80)
suffix_input = pn.widgets.TextInput(name="接尾語", placeholder="_suffix", width=80)
number_input = pn.widgets.IntInput(name="桁数", value=1, step=1, start=1, end=1000, width=80)

# ボタンウィジェット定義
load_button = pn.widgets.Button(name="ファイル読み込み", button_type="primary")
select_all_button = pn.widgets.Button(name="すべて選択", button_type="default")
deselect_all_button = pn.widgets.Button(name="すべて選択解除", button_type="default")
check_button = pn.widgets.Button(name="リネーム対象を確認", button_type="primary")
set_original_name_button = pn.widgets.Button(name="現在のファイル名を設定", button_type="default")
generate_names_button = pn.widgets.Button(name="ファイル名を生成", button_type="default")
rename_button = pn.widgets.Button(name="リネーム実行", button_type="primary", disabled=True, height=70, width=200)

# テキスト出力用ウィジェット定義
rename_result = pn.pane.Alert("実行結果", alert_type="dark", height=70, width=200)

# チェックボックスグループウィジェット
file_selector = pn.widgets.CheckBoxGroup()

# リネーム対象ファイル名の表示用コンテナ
rename_inputs_container = pn.Column()

# リネーム進捗表示
rename_tqdm = pn.widgets.Tqdm()

# ファイルとディレクトリのリスト管理用
file_list = []

def list_directory(path):
    """ 指定されたディレクトリ内のファイルとディレクトリをリストアップする """
    dirs = []
    files = []
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            dirs.append(entry)
        elif os.path.isfile(full_path):
            files.append(entry)
    return dirs, files

def load_files(event):
    """ ディレクトリからファイルをロードして選択肢を更新する """
    path = convert_to_wsl_path(input_dir.value)
    _, files = list_directory(path)
    file_list.extend(files)
    file_selector.options = files
    output_dir.value = convert_to_win_path(os.path.join(path, "renamed"))

def select_all_files(event):
    """ すべてのファイルを選択する """
    file_selector.value = file_list
    
def deselect_all_files(event):
    """ すべてのファイルを選択解除する """
    file_selector.value = []

def populate_rename_inputs(event):
    """ リネーム対象の入力フォームを生成する """
    rename_inputs_container.clear()
    for filename in file_selector.value:
        input_widget = pn.widgets.TextInput(name=filename, placeholder='リネーム後のファイル名 ※手動で編集可')
        rename_inputs_container.append(input_widget)
    rename_button.disabled = False

def set_original_names(event):
    """ 元のファイル名を入力フォームにセットする """
    for input_widget in rename_inputs_container:
        input_widget.value = input_widget.name

def generate_names(event):
    """ 新しいファイル名を生成して入力フォームにセットする """
    num = 0
    for input_widget in rename_inputs_container:
        new_name = f"{prefix_input.value}{num:0{number_input.value}}{suffix_input.value}{os.path.splitext(input_widget.name)[1]}"
        input_widget.value = new_name
        num += 1

def rename_files(event):
    """ ファイルをリネームして新しいディレクトリにコピーする """
    rename_result.object = "処理中..."
    rename_result.alert_type = "info"
    try:
        for input_widget in rename_inputs_container:
            if input_widget.value == "":
                rename_result.object = "リネーム後ファイル名が未設定"
                rename_result.alert_type = "warning"
                return
        target_dir = convert_to_wsl_path(output_dir.value)
        os.makedirs(target_dir, exist_ok=True)
        for input_widget in rename_tqdm(rename_inputs_container):
            original_path = os.path.join(convert_to_wsl_path(input_dir.value), input_widget.name)
            new_path = os.path.join(target_dir, input_widget.value)
            shutil.copy2(original_path, new_path)
        rename_result.object = "成功!!"
        rename_result.alert_type = "success"
    except Exception as e:
        rename_result.object = "リネーム失敗"
        rename_result.alert_type = "warning"
        print(traceback.format_exc())

# イベントハンドラの設定
load_button.on_click(load_files)
select_all_button.on_click(select_all_files)
deselect_all_button.on_click(deselect_all_files)
check_button.on_click(populate_rename_inputs)
set_original_name_button.on_click(set_original_names)
generate_names_button.on_click(generate_names)
rename_button.on_click(rename_files)

# ダッシュボードの構築
input_section = pn.WidgetBox("# 1. ファイル読み込み", input_dir, load_button,
                                "# 2. リネーム対象を選択", file_selector, pn.Row(select_all_button, deselect_all_button), check_button,
                                "# 3. リネーム後のファイル名を設定", set_original_name_button, pn.Row(prefix_input, number_input, suffix_input), generate_names_button,
                                "# 4. リネーム実行", output_dir, pn.Row(rename_button, rename_result), rename_tqdm)
dashboard_layout = pn.Row(input_section, pn.WidgetBox("# リネーム対象", rename_inputs_container))

dashboard_layout.servable()
