#-*- coding: utf-8 -*-
from setup import *
from calcSim import *

import torch
from torch.utils.data import Dataset, DataLoader
from transformers import T5ForConditionalGeneration, T5Tokenizer
import asyncio



import warnings

async def predict(target, input):

    warnings.simplefilter('ignore')

    # target = "能登地方の地震活動「短くても数か月は続く」政府・地震調査委員会が臨時会合で評価"
    # input = "おとといときのう、震度6弱と震度5強が相次いだ石川県能登地方の地震活動について、政府の地震調査委員会の平田直委員長は、短くても数か月は続くとの見通しを示しました。 能登地方で震度6弱と5強を相次ぎ観測した地震について、政府の地震調査委員会はきのう臨時の会合を開き、気象庁と同様に、おととしの12月から活発な状態が続いている「一連の地震活動の一部」と評価しました。 そのうえで平田直委員長は今後の見通しについて次のような見解を示しました。 地震調査委員会 平田 直委員長 「（一連の地震活動の）始まりが2018年ぐらいだから相当長い間続いている現象なので、これがパタッと終わるとは考えにくい。この先1週間とか2週間ではなく、月単位でこういった活動が続く可能性が非常に高い」 地震調査委員会は来月の定例会合で、能登地方で続く地震活動の原因について国立大学などの研究成果なども交えて検討することにしています。"

    #モデルの読み込み
    tokenizer = T5Tokenizer.from_pretrained(MODEL_DIR, is_fast=True)
    trained_model = T5ForConditionalGeneration.from_pretrained(MODEL_DIR)

    #生成タイトルとオリジナルタイトルの類似度計算
    cs = CalcSim(trained_model,tokenizer,args.max_input_length,args.max_target_length)
    result = cs.make_output(input,target)

    for k in result:
      if k == "scores":
        print(f"{k} : ")
        scores = result[k][0]
        for i in scores:
          print(f"\t{i} : {scores[i]}")
      else:
          print(f"{k} : {result[k]}")
          #いただいたモデルで本番に近い動作を検証するため勝手ではありますが以下の値を返すようにしてあります。
    return result["scores"][0]["rouge-1"]["f"]
        
