# モジュールを読み込む。
import tkinter  # Tcl/Tk の Python インタフェース
import time

# 関数を読み込む。
from tkinter import messagebox  # メッセージボックス作成
from joblib import Parallel, delayed
from youtube import get_video_id, get_video_data, get_chat_id, get_page_token, get_chat_data  # YouTube
from youtube import get_message_list, get_user_name_list  # YouTube
from translator import deepl_translate  # DeepL翻訳

# ======================================================================================================================
# チャット読み込みの間隔を設定する。(短くし過ぎるとエラーになるので注意)
UPDATE_TIME = 3000  # ミリ秒
# ======================================================================================================================


# ボタンをクリックしたときの処理をする。
def click_button():
    # GUIから情報を取得する。
    youtube_live_url = edit_box1.get()  # YouTubeLiveのURL
    youtube_api_key = edit_box2.get()  # YouTube APIキー

    # YouTubeLiveの情報を取得する。
    video_id = get_video_id(youtube_live_url)  # ビデオID
    video_data = get_video_data(video_id, youtube_api_key)  # ビデオデータ
    chat_id, error_message = get_chat_id(video_data)  # チャットID
    if chat_id is None:  # YouTubeLive以外の場合
        messagebox.showerror('URL Error', error_message)
        return  # 処理を中断する。
    chat_data = get_chat_data(chat_id, None, youtube_api_key)  # チャットデータ(ページトークン初期値=None)
    page_token = get_page_token(chat_data)  # ページトークン

    # テキストボックスにメッセージを追加する。
    root.after(UPDATE_TIME, add_message, chat_id, page_token)


# テキストボックスにメッセージを追加する。
def add_message(chat_id, page_token):
    # GUIから情報を取得する。
    youtube_api_key = edit_box2.get()  # YouTube APIキー
    deepl_api_key = edit_box3.get()  # DeepL APIキー
    target_lang = variable.get()  # 翻訳先の言語

    # YouTubeLiveの情報を取得する。
    chat_data = get_chat_data(chat_id, page_token, youtube_api_key)  # チャットデータ
    page_token = get_page_token(chat_data)  # ページトークン
    message_list = get_message_list(chat_data)  # メッセージリスト
    user_name_list = get_user_name_list(chat_data)  # ユーザー名リスト

    # DeepLで翻訳する。
    start_time = time.time()  # 処理開始時刻
    trans_message_list = Parallel(n_jobs=-1)(
        [delayed(deepl_translate)(message, target_lang, deepl_api_key) for message in message_list]
    )
    end_time = time.time()  # 処理終了時刻
    elapsed_time_s = end_time - start_time  # 処理時間 秒
    elapsed_time_ms = round(elapsed_time_s * 1000)  # 処理時間 ミリ秒

    # テキストボックスに表示するメッセージを設定する。
    display_message_list = []
    for index, trans_message in enumerate(trans_message_list):  # メッセージの数だけ繰り返す。
        text = '[' + user_name_list[index] + '] ' + trans_message  # [ユーザー名]＋翻訳メッセージ
        display_message_list.append(text)

    # テキストボックスにメッセージを追加する。
    for display_message in display_message_list:
        txt_box.insert(tkinter.END, display_message)
        txt_box.insert(tkinter.END, '\n')
        txt_box.insert(tkinter.END, '\n')

    # スクロールバーを一番下にする。
    txt_box.see('end')

    # ウィンドウ表示を更新する。
    root.update()

    # 指定した時間待機する。
    wait_time = max({0, UPDATE_TIME - elapsed_time_ms})
    root.after(wait_time, add_message, chat_id, page_token)


# ======================================================================================================================


# ウィンドウを作成する。
root = tkinter.Tk()
root.title('YouTube Live Chat DeepL Translator')
root.geometry('600x650')
root.resizable(False, False)

# フレームを作成する。
frame = tkinter.Frame(root)
frame.pack()
frame.place(x=0, y=70)

# テキストボックスを作成する。
txt_box = tkinter.Text(frame, font=('Arial', 10), width=82, height=29)
y_scroll = tkinter.Scrollbar(frame, orient=tkinter.VERTICAL, command=txt_box.yview)  # 縦方向スクロールバー
y_scroll.pack(side=tkinter.RIGHT, fill='y')  # 縦方向スクロールバー
txt_box['yscrollcommand'] = y_scroll.set  # 縦方向スクロールバー
txt_box.pack()

# ボタンを作成する。
button = tkinter.Button(root, text='Start', font=('Arial', 15), command=click_button)
button.pack()
button.place(x=500, y=20)

# ラベルを作成する。
label1 = tkinter.Label(root, text='YouTube Live URL', font=('Arial', 12))
label1.pack()
label1.place(x=20, y=5)

# ラベルを作成する。
label2 = tkinter.Label(root, text='YouTube API Key', font=('Arial', 10))
label2.pack()
label2.place(x=140, y=590)

# ラベルを作成する。
label3 = tkinter.Label(root, text='DeepL API Key', font=('Arial', 10))
label3.pack()
label3.place(x=370, y=590)

# ラベルを作成する。
label4 = tkinter.Label(root, text='Target Language', font=('Arial', 10))
label4.pack()
label4.place(x=10, y=590)

# YouTubeLiveのURLを入力するエディットボックスを作成する。
edit_box1 = tkinter.Entry(root, font=('Arial', 12), width=50)
edit_box1.pack()
edit_box1.place(x=20, y=30)

# YouTube APIキーを入力するエディットボックスを作成する。
edit_box2 = tkinter.Entry(root, font=('Arial', 10), width=30, show='*')
edit_box2.pack()
edit_box2.place(x=140, y=610)

# DeepL APIキーを入力するエディットボックスを作成する。
edit_box3 = tkinter.Entry(root, font=('Arial', 10), width=30, show='*')
edit_box3.pack()
edit_box3.place(x=370, y=610)

# 翻訳言語を選択するプルダウンメニューを作成する。
option_list = [
    'German',      # DE
    'English',     # EN
    'French',      # FR
    'Italian',     # IT
    'Japanese',    # JA
    'Spanish',     # ES
    'Dutch',       # NL
    'Polish',      # PL
    'Portuguese',  # PT
    'Russian',     # RU
    'Chinese'      # ZH
]
variable = tkinter.StringVar(root)
variable.set(option_list[4])  # JA
pull_down_menu = tkinter.OptionMenu(root, variable, *option_list)
pull_down_menu.config(width=10, font=('Arial', 10))
pull_down_menu.pack()
pull_down_menu.place(x=10, y=610)

# ウインドウを描画する。
root.mainloop()