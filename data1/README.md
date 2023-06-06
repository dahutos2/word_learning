# 目的
- 英単語と日本語訳の組み合わせを任意の数、csvに出力する
- 注意: 大量の英単語の作成を何度も行うとIPアドレスがブロックされることがあります
## 実施手順
- 設定ファイルに出力先のフォルダを設定する
  - `./execute/config.ini`
- 実行ファイルを実行する
  - `./execute/word_fetcher_mac`
- 注意：この実行ファイルは、MacOSでしか使用できないので、Windowsで実行したいときは、実行ファイルを作成して下さい
## 仮想環境構築(Anaconda)
### 名前
- get_word_env
### コマンド
- 作成
  - `conda create -n get_word_env python=3.8`
- 活性化
  - `conda activate get_word_env`
- 非活性化
  - `conda deactivate`
- 実行
  - `python ./get_words/word_fetcher.py`
### インストールパッケージ
#### ファイル名
- ./requirements.txt
#### インストールコマンド
- `pip install -r requirements.txt`
### 実行ファイルの作成
#### コマンド
- `pyinstaller` をインストールします
  - `conda install -c conda-forge pyinstaller`
- 実行ファイル作成
  - `pyinstaller --onefile --noconsole ./get_words/word_fetcher.py`
