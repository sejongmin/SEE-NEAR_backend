import torch
from transformers import PreTrainedTokenizerFast
from transformers import BartForConditionalGeneration
from constant.conversation import *

tokenizer = PreTrainedTokenizerFast.from_pretrained('gogamza/kobart-summarization')
model = BartForConditionalGeneration.from_pretrained('gogamza/kobart-summarization')

# text = """
# 오늘은 아침 일찍 일어나서 창밖을 바라봤다. 아름다운 해가 떠오르고 있었다.
# 어제 꽃을 심은 정원을 살펴보니, 조금씩 자라고 있는 모습이 기쁘다.
# 창가에 앉아 일기를 쓰는 것이 오랜만에 느껴진다. 마음이 차분해진다.
# 지난 주에 방문한 도서관에서 빌린 책을 읽으며 시간을 보냈다.
# 가까운 친구들이 방문해 커피를 마시며 오랫동안 얘기를 나누었다.
# 밤에는 별들을 바라보며 하루를 돌아보았다. 작은 행복이 가득한 하루였다.
# 내일은 손자와 손녀들이 놀러오는 날이다. 미리 음식을 준비해야겠다.
# 마음이 머무는 곳이라면 내 가족들이 있는 곳이라고 생각한다.
# 노래를 부르면서 정원을 거닐며 오늘의 감사한 순간들을 되새기기로 했다.
# 내일의 일정을 생각하며 잠이 들었다. 오늘도 행복한 하루였다.
# """

def conversation_summary():
    with open(TEXT_PATH, "r", encoding=ENCODING) as f:
        sents = f.read()
    raw_input_ids = tokenizer.encode(sents)
    input_ids = [tokenizer.bos_token_id] + raw_input_ids + [tokenizer.eos_token_id]
    input_ids = torch.tensor([input_ids])

    summary_ids = model.generate(input_ids = input_ids,
                                    bos_token_id = model.config.bos_token_id,
                                    eos_token_id = model.config.eos_token_id,
                                    max_length = 50,
                                    length_penalty = 1.0,
                                    min_length = 32,
                                    num_beams = 10,
                                )

    flag = 0
    list = []

    for i in range(1, len(summary_ids[0])) :
        j = 0
        for j in range(0, i) :
            if tokenizer.decode(summary_ids[0][i]) == tokenizer.decode(summary_ids[0][j]) :
                flag = 1
                break
        if flag == 0 :
            list.append(tokenizer.decode(summary_ids[0][i]))
        flag = 0

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary