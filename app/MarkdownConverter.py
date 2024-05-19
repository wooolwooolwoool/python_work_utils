import panel as pn

# Panelの拡張を有効にする
pn.extension()

# テキストエリアウィジェットを作成
markdown_input = pn.widgets.TextAreaInput(name='Markdown Input', placeholder='Enter Markdown text here...', width=600, height=600)

# Markdown表示用のウィジェットを作成
markdown_display = pn.pane.Markdown('Your formatted Markdown will appear here.', width=600, height=600)

# ボタンを作成
update_button = pn.widgets.Button(name='Convert', button_type='primary')

# ボタンのクリックイベントに対するコールバック関数を定義
def update_markdown(event):
    markdown_display.object = markdown_input.value

# ボタンにコールバック関数を追加
update_button.on_click(update_markdown)

# レイアウトを作成
layout = pn.Row(pn.Column(
    markdown_input,
    update_button),
    pn.WidgetBox(markdown_display)
)

# ダッシュボードとして表示
layout.servable()
