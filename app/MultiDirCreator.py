import os
import shutil
import panel as pn
import traceback

pn.extension()

# テキスト入力用ウィジェット定義
template_dir = pn.widgets.TextInput(name="テンプレートディレクトリ指定", placeholder=r"C:\Users\user\Files")
output_dir = pn.widgets.TextInput(name="ディレクトリ生成先", placeholder=r"C:\Users\user\Files")
prefix_input = pn.widgets.TextInput(name="接頭語", placeholder="prefix_", width=80)
suffix_input = pn.widgets.TextInput(name="接尾語", placeholder="_suffix", width=80)
number_input = pn.widgets.IntInput(name="桁数", value=1, step=1, start=1, end=1000, width=80)
create_number_input = pn.widgets.IntInput(name="生成する個数", value=1, step=1, start=1, end=1000, width=80)

# ボタンウィジェット定義
load_button = pn.widgets.Button(name="テンプレート読み込み", button_type="primary")
add_button = pn.widgets.Button(name="追加", button_type="default")
del_button = pn.widgets.Button(name="削除", button_type="default")
auto_add_button = pn.widgets.Button(name="ディレクトリ名自動生成", button_type="default")
dir_create_button = pn.widgets.Button(name="ディレクトリ生成実行", button_type="primary", height=70, width=200)

use_template = pn.widgets.Checkbox(name= "テンプレートを使用")

# テキスト出力用ウィジェット定義
load_result = pn.pane.Str("", styles={'font-size': '12pt'})
dir_create_result = pn.pane.Alert("実行結果", alert_type="dark", height=70, width=200)
dir_tree = pn.pane.Str("")

# 生成ディレクトリ表示用コンテナ
create_dir_container = pn.Column()

# ディレクトリ生成進捗表示
create_tqdm = pn.widgets.Tqdm()

def get_directory_tree(dir_path, prefix=""):
    """
    指定したディレクトリのツリー構造を文字列で返す。

    :param dir_path: ツリー構造を取得したいディレクトリのパス。
    :param prefix: 現在のフォルダの深さを示すプレフィックス。
    :return: ディレクトリのツリー構造を表す文字列。
    """
    dir_tree = prefix + "|-- " + os.path.basename(dir_path) + "\n"
    prefix += "    "
    try:
        for item in sorted(os.listdir(dir_path)):
            path = os.path.join(dir_path, item)
            if os.path.isdir(path):
                dir_tree += get_directory_tree(path, prefix)
            else:
                dir_tree += prefix + "|-- " + item + "\n"
    except PermissionError:
        dir_tree += prefix + "|-- [Permission Denied]\n"
    return dir_tree


def create_directories_from_list(template_path, output_base_path, directory_names):
    """
    既存のディレクトリ構造をコピーしてリストに基づいたディレクトリを作成する。

    :param template_path: テンプレートとして使用するディレクトリのパス。
    :param output_base_path: 出力するディレクトリのベースパス。
    :param directory_names: 作成するディレクトリ名のリスト。
    """
    # 指定されたディレクトリ名に基づいてディレクトリを作成
    os.makedirs(output_base_path, exist_ok=True)
    for dir_name in create_tqdm(directory_names):
        if dir_name != "":
            output_dir = os.path.join(output_base_path, dir_name)
            if use_template.value:
                shutil.copytree(template_path, output_dir)
            else:
                os.makedirs(output_dir)

def load_template(event):
    """ テンプレートをロードする """
    dir_tree.object = get_directory_tree(convert_to_wsl_path(template_dir.value))

def add_dirs(event):
    """ ディレクトリ名入力フォーム追加 """
    input_widget = pn.widgets.TextInput(placeholder='ディレクトリ名')
    create_dir_container.append(input_widget)
    
def del_dir(event):
    """ ディレクトリ名入力フォーム削除 """
    if 0 < len(create_dir_container):
        create_dir_container.pop(-1)

def auto_add_dirs(event):
    """ ディレクトリ名自動追加 """
    for num in range(create_number_input.value):
        new_name = f"{prefix_input.value}{num:0{number_input.value}}{suffix_input.value}"
        input_widget = pn.widgets.TextInput(value=new_name, placeholder='ディレクトリ名')
        create_dir_container.append(input_widget)

def create_dir(event):
    """ ディレクトリ生成 """
    dir_create_result.object = "生成中..."
    dir_create_result.alert_type = "info"
    try:
        tmp = [t.value for t in create_dir_container]
        create_directories_from_list(convert_to_wsl_path(template_dir.value),
                                    convert_to_wsl_path(output_dir.value),
                                    tmp)
        dir_create_result.object = "成功!!"
        dir_create_result.alert_type = "success"
    except Exception as e:
        dir_create_result.object = "失敗!!"
        dir_create_result.alert_type = "warning"
        print(traceback.format_exc())

# イベントハンドラの設定
load_button.on_click(load_template)
add_button.on_click(add_dirs)
del_button.on_click(del_dir)
auto_add_button.on_click(auto_add_dirs)
dir_create_button.on_click(create_dir)

# ダッシュボードの構築
input_section = pn.WidgetBox("# 1. テンプレート指定", use_template, template_dir, load_button,
                             "# 2. 生成するディレクトリ名指定", create_dir_container, pn.Row(add_button, del_button),
                             pn.Row(prefix_input, number_input, suffix_input, create_number_input), auto_add_button,
                             "# 3. ディレクトリ生成実行", output_dir, pn.Row(dir_create_button, dir_create_result), create_tqdm)
dashboard_layout = pn.Row(input_section, dir_tree)

dashboard_layout.servable()
