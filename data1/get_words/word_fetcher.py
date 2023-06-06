import os
import sys
import re
import csv
import configparser
import random
import tkinter as tk
from tkinter import simpledialog, ttk
from nltk.corpus import wordnet as wn
from googletrans import Translator


def get_current_path(file):
    # 実行ファイルの絶対パスを取得
    executable_path = os.path.abspath(sys.argv[0])

    # 実行ファイルのディレクトリを取得
    executable_dir = os.path.dirname(executable_path)

    return os.path.join(executable_dir, file)


def check_condition(s):
    """アルファベットが含まれるまたは全てがカタカナであるかを確認する"""
    return bool(re.search("[a-zA-Z]|^[ァ-ヶー]+$", s))


def get_random_synset():
    """WordNetからランダムな単語を取得する"""
    synsets = list(wn.all_synsets())
    return random.choice(synsets)


def get_translation(word):
    """Google Translate APIで英語を翻訳する"""
    translator = Translator(service_urls=["translate.google.com"])
    translated_word = translator.translate(word, src="en", dest="ja")
    return translated_word.text


def save_words_to_csv(word_list, file_name="en_and_ja.csv"):
    """英単語のリストを、CSVに追記する"""
    # ファイルの存在を確認し、存在しない場合は作成
    if not os.path.exists(file_name):
        open(file_name, "w").close()

    # ファイルのサイズを確認
    if os.path.getsize(file_name) == 0:
        # ヘッダー行を書き込む
        with open(file_name, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["English", "Japanese"])

    # データ行を追記する
    with open(file_name, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        for word in word_list:
            writer.writerow(word)


def read_config():
    """設定ファイルのCSV出力先を取得する"""
    config = configparser.ConfigParser()
    config_path = get_current_path("config.ini")
    config.read(config_path)
    return config["output"]["csv_file_path"]


def get_num_words_from_user():
    """単語数入力のダイアログを表示"""
    root = tk.Tk()
    root.withdraw()
    num_words = simpledialog.askinteger(
        "英単語と日本語訳の取得", "取得する英単語の数を入力して下さい。", minvalue=1, maxvalue=5000
    )
    return num_words


def cancel_loop():
    """ループを中断する"""
    global cancel_requested
    cancel_requested = True
    print("「現状で出力する」で処理が中断されました。")


def csv_to_set(file_path):
    """csvファイルをセットに変換する

    #ファイルパスが存在しないときは、空のデータを返す
    """
    if not os.path.exists(file_path):
        return set()
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        return set(tuple(row) for row in reader)


# Download WordNet data
import nltk

nltk.download("wordnet")

csv_file_path = read_config()
num_words = get_num_words_from_user()
words = set()
exist_words = csv_to_set(csv_file_path)

# キャンセルボタンが押下されたときは、中断する
if num_words == None:
    print("キャンセルされました。")
    sys.exit()

# 進捗率を表示
progressbar_root = tk.Tk()
progressbar_root.title("取得中")

progressbar = ttk.Progressbar(progressbar_root, length=300, mode="determinate")
progressbar["maximum"] = num_words
progressbar.grid(column=0, row=0, padx=10, pady=10)

# 中断ボタン
cancel_button = tk.Button(progressbar_root, text="現状で出力する", command=cancel_loop)
cancel_button.grid(column=0, row=2, padx=10, pady=10)

cancel_requested = False

print(f"{num_words}セットの英単語の取得を開始します。")
# 単語数が指定の数を超えるまで、ループを繰り返す
while len(words) < num_words and not cancel_requested:
    synset = get_random_synset()
    english_word = synset.lemmas()[0].name()

    japanese_translation = get_translation(english_word)
    if check_condition(japanese_translation):
        continue

    word_pair = (english_word, japanese_translation)

    # すでに登録済みの時は、何もしない
    if exist_words in word_pair:
        continue

    words.add(word_pair)

    # プログレスバーを更新
    progressbar["value"] = len(words)
    progressbar_root.update()

# プログレスバーを閉じる
progressbar_root.destroy()

# ディレクトリが存在しない場合は作成
directory_path = os.path.dirname(csv_file_path)
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

# csvファイルに出力
print(f"{csv_file_path}に{len(words)}セットの英単語を出力します")
save_words_to_csv(words, csv_file_path)
