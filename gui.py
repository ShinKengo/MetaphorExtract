import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, Scrollbar
import os
from answer_generater import gpt4o_mini_response
import sys

# gpt4o_mini_response関数の呼び出し

def on_extract():
    if (text_box.get("1.0", tk.END).strip() == placeholder_text or not text_box.get("1.0", tk.END).strip()) and not selected_files:
        error_label.config(text="文章を入力してください", fg="red")
        return
    error_label.config(text="")
    extract_button.config(state="disabled")
    clear_button.config(state="disabled")
    select_button.config(state="disabled")
    if text_box.get("1.0", tk.END).strip() and not selected_files:
        user_input = text_box.get("1.0", tk.END).strip()
    elif selected_files:
        user_input = ""
        for file in selected_files:
            with open(file, 'r', encoding='utf-8') as f:
                user_input += f.read() + "\n"
    else:
        user_input = ""
    loading_label = tk.Label(root, text="処理中...しばらくお待ちください", font=("Helvetica", 20), bg="#ccffcc", fg="blue")
    loading_label.pack(pady=20)
    root.update()
    response = gpt4o_mini_response(user_input)
    loading_label.destroy()
    root.withdraw()  # 入力画面を消す
    display_output(response)

# 抽出結果画面の表示

def display_output(response):
    output_window = tk.Toplevel()
    output_window.title("抽出結果")
    output_window.geometry("1400x700")
    output_window.grid_columnconfigure(0, weight=1)
    output_window.grid_columnconfigure(1, weight=2)
    output_window.configure(bg="#ccffcc")

    output_frame = tk.Frame(output_window, bg="#ccffcc")
    output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    canvas = tk.Canvas(output_frame, bg="#ccffcc")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = Scrollbar(output_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    scrollable_frame = tk.Frame(canvas, bg="#ccffcc")
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    for i, pair in enumerate(response):
        row_frame = tk.Frame(scrollable_frame, bg="#ccffcc")
        row_frame.pack(fill=tk.X, pady=5)
        local_height = max((len(pair[0])-1) // 22 + 1, (len(pair[1])-1) // 44 + 1)

        label1 = tk.Text(row_frame, wrap=tk.WORD, bg="#ffeecc", font=("Helvetica", 14), height=local_height, width=40)
        label1.insert("1.0", pair[0])
        label1.config(state=tk.DISABLED)
        label1.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        label2 = tk.Text(row_frame, wrap=tk.WORD, bg="#ffeecc", font=("Helvetica", 14), height=local_height, width=80)
        label2.insert("1.0", pair[1])
        label2.config(state=tk.DISABLED)
        label2.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)

    next_button = tk.Button(output_window, text="次の文章", command=lambda: return_to_input(output_window), bg="#ffcc99", font=("Helvetica", 12))
    next_button.pack(side=tk.BOTTOM, pady=10)
    exit_button = tk.Button(output_window, text="終了", command=safe_exit, bg="#ff6666", font=("Helvetica", 12))
    exit_button.pack(side=tk.TOP, anchor='ne', padx=10, pady=10)

# 入力画面に戻る

def return_to_input(output_window):
    output_window.destroy()
    root.deiconify()
    on_reset()

# ファイル選択ボタンのクリックイベント
selected_files = []
def on_select_files():
    files = filedialog.askopenfilenames(filetypes=[("Text files", "*.txt")])
    for file in files:
        if file not in selected_files:
            selected_files.append(file)
            show_selected_files()

def show_selected_files():
    for widget in file_frame.winfo_children():
        widget.destroy()
    for file in selected_files:
        label = tk.Label(file_frame, text=os.path.basename(file), bg="#66bb66")
        label.pack(side=tk.LEFT, padx=5)
        remove_button = tk.Button(file_frame, text="×", command=lambda f=file: remove_file(f), bg="#ffcc99")
        remove_button.pack(side=tk.LEFT, padx=2)

def remove_file(file):
    selected_files.remove(file)
    show_selected_files()

# クリアとボタンの再有効化

def on_reset():
    on_clear()
    text_box.insert("1.0", placeholder_text)
    text_box.config(fg="gray")
    extract_button.config(state="normal")
    clear_button.config(state="normal")
    select_button.config(state="normal")

# 入力をクリア

def on_clear():
    text_box.delete("1.0", tk.END)
    selected_files.clear()
    show_selected_files()

# プログラムを安全に終了

def safe_exit():
    root.destroy()
    sys.exit()

# メインウィンドウの作成
root = tk.Tk()
root.title("テキスト抽出アプリケーション")

# エラーメッセージラベルの作成
error_label = tk.Label(root, text="", bg="#ccffcc", font=("Helvetica", 24))
error_label.pack()
root.geometry("1400x700")
root.configure(bg="#ccffcc")

# テキストボックスの作成
text_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10, bg="#ffeecc")
text_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10, anchor='center')
placeholder_text = "ここにテキストをペーストしてください"
text_box.insert("1.0", placeholder_text)

def on_text_change(event):
    if text_box.get("1.0", tk.END).strip() == placeholder_text:
        text_box.delete("1.0", tk.END)
        text_box.config(fg="black")
    elif not text_box.get("1.0", tk.END).strip():
        text_box.insert("1.0", placeholder_text)
        text_box.config(fg="gray")

text_box.bind("<FocusIn>", on_text_change)
text_box.bind("<FocusOut>", on_text_change)
text_box.config(fg="gray")
text_box.pack(pady=10)

# ボタンの作成
button_frame = tk.Frame(root, bg="#ccffcc")
button_frame.pack(pady=10)

select_button = tk.Button(button_frame, text="フォルダー選択", command=on_select_files, bg="#ffcc99", width=12, height=2, font=("Helvetica", 12))
select_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(button_frame, text="クリア", command=on_clear, bg="#ffcc99", width=12, height=2, font=("Helvetica", 12))
clear_button.pack(side=tk.LEFT, padx=5)

extract_button = tk.Button(button_frame, text="抽出", command=on_extract, bg="#ffcc99", width=12, height=2, font=("Helvetica", 12))
extract_button.pack(side=tk.LEFT, padx=5)

exit_button = tk.Button(root, text="終了", command=safe_exit, bg="#ff6666", font=("Helvetica", 12))
exit_button.pack(side=tk.TOP, anchor='ne', padx=10, pady=10)

# ファイル名の表示フレーム
file_frame = tk.Frame(root, bg="#ccffcc")
file_frame.pack(pady=5)

# メインループの開始
root.mainloop()
