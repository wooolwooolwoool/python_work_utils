import panel as pn
import yaml
import os

yaml_file = 'data/textcopy.yaml'
save_flg = True

# Panelの拡張を有効にする
pn.extension()

# テキスト入力ウィジェットを作成
text_input = pn.widgets.TextInput(placeholder='Enter text...', width=300)

# JavaScriptコードを実行するHTMLパネルを作成
html_pane = pn.pane.HTML("", width=0, height=0, sizing_mode='fixed')

# 動的に生成されるボタンを格納するコンテナ
button_container = pn.Column()

yaml_input = pn.widgets.TextAreaInput(name='yaml Input', placeholder='Enter text here...', width=600, height=600)
yaml_load_button = pn.widgets.Button(name='load', button_type='primary')
yaml_save_button = pn.widgets.Button(name='save', button_type='primary')

# JavaScriptを使用してクリップボードにコピーする関数
def copy_to_clipboard(text):
    return f"""
    <script>
    function copyToClipboard() {{
        navigator.clipboard.writeText("{text}").then(function() {{
            console.log('Copied to clipboard successfully!');
        }}, function(err) {{
            console.error('Could not copy text: ', err);
        }});
    }}
    copyToClipboard();
    </script>
    """

# Addボタンのコールバック関数
def add_copy_button(event):
    # 入力されたテキストを取得
    text = text_input.value
    if text:
        # 新しいボタンを作成
        new_button = pn.widgets.Button(name=f'Copy "{text}"', button_type='primary', button_style="outline")
        
        # ボタンのコールバック関数を定義
        def copy_callback(event, text=text):
            js_code = copy_to_clipboard(text)
            html_pane.object = js_code
        
        # 新しいボタンにコールバック関数を追加
        new_button.on_click(copy_callback)
        
        # コンテナに新しいボタンを追加
        button_container.append(new_button)

        # テキストを保存
        if save_flg:
            with open(yaml_file, 'r') as f:
                data = yaml.safe_load(f)
            with open(yaml_file, 'w') as f:
                if data is None:
                    data = []
                data.append(text)
                yaml.dump(data, f)

# テキストデータの読み込み
def load_data():
    global save_flg
    save_flg = False
    button_container.clear()
    try:
        if os.path.exists(yaml_file):
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
                if data is not None:
                    for s in data:
                        text_input.value = s
                        add_copy_button(None)    
                    text_input.value = ""
        else:
            with open(yaml_file, 'w') as f:
                pass
    except:
        pass
    save_flg = True

def load_yaml(event):
    with open(yaml_file) as f:
        data = yaml.safe_load(f)
        yaml_input.value = "\n".join(data)

def save_yaml(event):
    with open(yaml_file, "w") as f:
        data = yaml_input.value.split("\n")
        if data is not None:
            with open(yaml_file, 'w') as f:
                yaml.dump(data, f)
    load_data()

# Addボタンを作成
add_button = pn.widgets.Button(name='Add', button_type='primary')
# ボタンのCallbackを登録
add_button.on_click(add_copy_button)
yaml_load_button.on_click(load_yaml)
yaml_save_button.on_click(save_yaml)

# レイアウトを作成
layout = pn.Tabs(("main", pn.Column(
    pn.Row(text_input, add_button),
    button_container,
    html_pane
)), ("edit", pn.Column(yaml_input, pn.Row(yaml_load_button, yaml_save_button))))

load_data()

# ダッシュボードとして表示
layout.servable()
