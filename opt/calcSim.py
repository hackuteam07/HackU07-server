
from rouge import Rouge
import MeCab as mc


class CalcSim():
  def __init__(self,model,tokenizer,max_input_length,max_target_length):
    self.tokenizer = tokenizer
    self.max_length = max_input_length
    self.trained_model = model
    self.max_target_length = max_target_length
    #スコア計算用インスタンス
    self.tagger = mc.Tagger()
    self.rouge = Rouge()


  def generate_summary(self,input):
    tokenized_inputs = self.tokenizer.batch_encode_plus(
                        [input], self.max_length, truncation=True,
                        padding="max_length", return_tensors="pt"
                    )
    input_ids  = tokenized_inputs["input_ids"]
    input_mask = tokenized_inputs["attention_mask"]

    output = self.trained_model.generate(input_ids=input_ids,
            attention_mask=input_mask,
            max_length=self.max_target_length,
            temperature=1.0,
            repetition_penalty=1.5,
            )

    output_text = [self.tokenizer.decode(ids, skip_special_tokens=True, clean_up_tokenization_spaces=False) for ids in output]

    return output_text[0]

  def calc_score(self,output,target):
    summery = self.tagger.parse(output)[:-1]
    title = self.tagger.parse(target)[:-1]
    scores = self.rouge.get_scores(summery,title)
    return scores

  def make_output(self,input,target):
    """
    input : 記事本文
    target : オリジナルタイトル
    """
    output_text = self.generate_summary(input)
    socres = self.calc_score(output_text,target)

    return {"original_title" : target,"generated_title": output_text,"scores" : socres}

