# 目的
- 英単語を入力として受け取り、その単語の正しい日本語訳とは異なる、しかし合理的な日本語訳を返す「意味的類義語生成モデル」を作成する
## 生成
- 生成処理
  - `./learning_word.ipynb`
- 参考文献フォルダ
  - `./references/`
## 生成処理の内部
- 英単語と誤った日本語訳を学習する
- ハイパーパラメータを設定し学習する
- 正しい日本語訳にどれだけ近いかで、結果を評価する
## 仮想環境構築(Anaconda)
### 名前
- leanrning_word_env
### コマンド
- 作成
  - `conda create -n leanrning_word_env  python=3.8`
- 活性化
  - `conda activate leanrning_word_env`
- 非活性化
  - `conda deactivate`
- JupyterLabのカーネルに仮想環境を追加
  - `python -m ipykernel install --user --name=leanrning_word_env`
### インストールパッケージ
#### ファイル名
- ./requirements.txt
#### インストールコマンド
- `pip install -r requirements.txt`
