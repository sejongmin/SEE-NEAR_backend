import torch
from transformers import PreTrainedTokenizerFast
from transformers import BartForConditionalGeneration
from constant.conversation import *

tokenizer = PreTrainedTokenizerFast.from_pretrained('digit82/kobart-summarization')
model = BartForConditionalGeneration.from_pretrained('digit82/kobart-summarization')

# sents = """
# 오늘도 허리가 아파서 아침에 일어나기가 참 힘들더라. 기지개를 켜고 겨우겨우 일어나서 차 한 잔 마셨지. 날씨는 참 좋은데, 허리가 계속 쑤시니까 움직이는 게 쉽지가 않네.
# 점심에는 그냥 간단히 국밥을 끓였어. 서서 오래 있는 게 힘들어서 말이야. 그래도 손녀가 와서 도와주니 고맙더라고. 밥 먹으면서 손녀랑 이런저런 얘기를 나누었어.
# 오후에는 허리 좀 펴보려고 동네 공원에 갔지. 친구들이랑 천천히 걷는데, 걸음이 느려져서 좀 답답하긴 하더라. 그래도 같이 얘기 나누면서 걷다 보니 한결 낫더군.
# 저녁에는 허리가 더 아파서 누워서 TV 좀 보다가 책 몇 장 읽었어. 그런데 책도 오래 읽다 보니 허리가 더 아프네. 그냥 일찍 누웠어.
# 오늘 하루도 이렇게 지나가니, 허리가 아프지만 그래도 감사한 마음이 든다.
# """

def conversation_summary(sents):
    with open(TEXT_PATH, "r", encoding=ENCODING) as f:
        sents = f.read()
    raw_input_ids = tokenizer.encode(sents)
    input_ids = [tokenizer.bos_token_id] + raw_input_ids + [tokenizer.eos_token_id]
    summary_ids = model.generate(torch.tensor([input_ids]),  num_beams=4,  max_length=512,  eos_token_id=1)

    text = tokenizer.decode(summary_ids.squeeze().tolist(), skip_special_tokens=True)
    words = text.split()
    seen_words = set()
    result_words = []

    for word in words:
        if word not in seen_words:
            seen_words.add(word)
            result_words.append(word)

    unique_text = " ".join(result_words)

    return unique_text

    # flag = 0
    # list = []

    # for i in range(1, len(summary_ids[0])) :
    #     j = 0
    #     for j in range(0, i) :
    #         if tokenizer.decode(summary_ids[0][i]) == tokenizer.decode(summary_ids[0][j]) :
    #             flag = 1
    #             break
    #     if flag == 0 :
    #         list.append(tokenizer.decode(summary_ids[0][i]))
    #     flag = 0
    # return ''.join(list)

# print(conversation_summary(sents))