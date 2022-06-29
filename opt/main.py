#-*- coding: utf-8 -*-
from setup import *
from calcSim import *

import torch
from torch.utils.data import Dataset, DataLoader
from transformers import T5ForConditionalGeneration, T5Tokenizer


import warnings
warnings.simplefilter('ignore')

tokenizer = T5Tokenizer.from_pretrained(MODEL_DIR, is_fast=True,model_max_length=args.max_input_length)
trained_model = T5ForConditionalGeneration.from_pretrained(MODEL_DIR)
cs = CalcSim(trained_model,tokenizer,args.max_input_length,args.max_target_length)


async def predict(target, input):
  #前処理の追加
  result = cs.make_output(input,target)
  #スコアをr-lに限定
  return result