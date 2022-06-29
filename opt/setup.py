#-*- coding: utf-8 -*-
import torch
import argparse


PRETRAINED_MODEL_NAME = "sonoisa/t5-base-japanese"
MODEL_DIR = "./model"

# GPU利用有無
USE_GPU = torch.cuda.is_available()

# 各種ハイパーパラメータ
args_dict = dict(
    data_dir=".",  # データセットのディレクトリ
    model_name_or_path=PRETRAINED_MODEL_NAME,
    tokenizer_name_or_path=PRETRAINED_MODEL_NAME,

    learning_rate=3e-4,
    weight_decay=0.0,
    adam_epsilon=1e-8,
    warmup_steps=0,
    gradient_accumulation_steps=1,

    n_gpu=1 if USE_GPU else 0,
    early_stop_callback=False,
    fp_16=False,
    opt_level='O1',
    max_grad_norm=1.0,
    seed=42,
)

# 学習に用いるハイパーパラメータを設定する
args_dict.update({
    "max_input_length":  512,  # 入力文の最大トークン数
    "max_target_length": 64,  # 出力文の最大トークン数
    "train_batch_size":  8,  # 訓練時のバッチサイズ
    "eval_batch_size":   8,  # テスト時のバッチサイズ
    "num_train_epochs":  8,  # 訓練するエポック数
    })

args = argparse.Namespace(**args_dict)

