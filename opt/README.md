# HackU07-ml

## 環境構築
- Mecab
  - インストール方法参考 >> https://qiita.com/Sak1361/items/47e9ec464ccc770cd65c

- ライブラリ
  - 下記コマンドでインストール  
  - `pip install -r requirements.txt`  

- 事前学習済みモデル
  - [ここ](https://drive.google.com/drive/folders/1VngpilapaaN-jH3x1KPfzmYkHUItaR8j?usp=sharing )からダウンロードしてください
  - トップディレクトリで解凍、`model`というディレクトリが生成されればok

## 実行方法
- トップディレクトリで`python main.py`

## モデルの読み込みテスト
- 必要なライブラリが揃っている状態でトップディレクトリで下記コードが動けば読み込みはできています
- モデルディレクトリパスを変更するときは`setup.py`の`MODEL_DIR`を変更してください
```python
from setup import *
from calcSim import *

import torch
from torch.utils.data import Dataset, DataLoader
from transformers import T5ForConditionalGeneration, T5Tokenizer

#　モデルの読み込み部分
tokenizer = T5Tokenizer.from_pretrained(MODEL_DIR, is_fast=True)
trained_model = T5ForConditionalGeneration.from_pretrained(MODEL_DIR)
```

## その他
- スコアが複数出てくるがこれは今後絞っていく予定
- generate_title.ipynbを見てもらえれば大体何をやっているかわかるかも？
- 疑問点があったら山根まで
