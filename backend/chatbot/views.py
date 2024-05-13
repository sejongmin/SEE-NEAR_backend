from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.http import FileResponse
from django.conf import settings
from .chatbotFunc.chatbotFunc import *
from .chatbotFunc.keyword_extraction import *
from .chatbotFunc.emotion_classification import *
from os import remove


import os

@api_view(['GET'])
def startConversation(request):
    print("대화 시작")
    
    return Response({'message': '대화가 시작되었습니다.'})

@api_view(['GET'])
def endConversation(request):
    print("대화 종료")
    
    with open('media/text.txt', "r", encoding='utf-8') as f:
        text = f.readlines()
        
    keyword = keyword_extraction(text)
    print("keyword:", keyword[0])
    emotion = emotion_classification('media/input.wav')
    print("Predicted emotion:", emotion)
    
    
    text_path = 'media/text.txt'
    audio_path = 'media/input.wav'
    audio_path2 = 'media/input.webm'
    audio_path3 = 'media/output.wav'

    remove(text_path)
    remove(audio_path)
    remove(audio_path2)
    remove(audio_path3)
    print('파일 삭제')
    
    return Response({'message': '대화가 종료되었습니다.'})

# @api_view(['GET'])
# def getSummary(request):
#     print("대화 요약")
#     with open('media/text.txt', "r", encoding='utf-8') as f:
#         conversation = f.read()
#     print(conversation)
    
#     command = ['다음 내용은 혼자 계신 시니어와 말동무 역할인 음성 챗봇간의 일상 생활',
#                 '관련 대화 답변 내용이야. 이를 참고해서 혼자 계신 시니어의 일상 활동을',
#                 '간략하게 한줄정도로 요약해줘']
    
#     prompt = create_prompt(conversation, command)
#     print(prompt)
#     response = client.chat.completions.create(
#     model="gpt-4",
#     messages = [
#     {
#         "role": "system",
#         "content": prompt
#     },
#     ],
#     max_tokens=100,
#     temperature=0.8,
#     stop=[' Human:', ' AI:']
#     )
#     print(response)
#     if response.choices:
#         bot_response = response.choices[0].message.content 
#     else:
#         bot_response = "No response from the model."
    
#     print(f'요약: {bot_response}')
#     summary_path = os.path.join(settings.MEDIA_ROOT, 'summary.txt')
#     with open(summary_path, 'a', encoding='utf-8') as f:
#             f.write(bot_response)
            
#     return Response({'message': '대화가 요약 완료.'})


name = '김숙자'
sex = 'female'
age = 60
interest = '임영웅', '봄', '강아지'
diasease = '당뇨'
prompt_list_default = [
                '너는 혼자계신 시니어분의 말동무 역할을 수행하게 될거야. 사용자의 정보를 알려줄게',
                f'시니어 분의 성별은 {sex}이고 나이는 {age}세 이시며 관심사로는 {interest}등이 있고 {diasease}와 같은 질병을 앓고 계셔',
                '위 정보를 참고해서 이 분이 심심하지 않으시게 일상생활의 간단한 질문이나 대답을 해주면 되',
                '너무 자세하게 질문과 대답을 하기보단 호응해주고 맞춰주는 식으로 대화를 해줘',
                '무조건 존댓말로 대답해줘',
                ]

@api_view(['POST'])
def chatbot(request):
    if request.method == 'POST':
        # GET speech-recognition user_input text from frontend and print
        user_input = request.POST.get('text', '')
        print(f'Input: {user_input}')

        # Append new user_input text data, if not exits, create new file and append
        text_path = os.path.join(settings.MEDIA_ROOT, 'text.txt')
        if not os.path.exists(text_path):
            open(text_path, 'w').close()

        with open(text_path, 'a') as f:
            f.write(user_input + '\n')
        
        # Create prompt & Get response
        prompt = create_prompt(user_input, prompt_list_default)
        response = get_ai_response(prompt)

        print(f'Response data: {response}')

        # If response exist update_list & Get response reply
        if response:
            update_list(response, prompt_list_default)
            pos = response.find("\nAI: ")
            response = response[pos + 4:]
        else:
            response = "response message not exist"
        print(f'Reply: {response}')
        
        # Create output.wav file with response reply through text_to_speech func
        text_to_speech(response)

        # Set output.wav to FileResponse format
        f = open('media/output.wav', "rb")
        audio_response = FileResponse(f)
        audio_response.set_headers(f)

        return audio_response
    else:
        return JsonResponse({'error': 'POST request required'})
    
# 설정시각 되면 알람 울림 -> 알람 종료하면 해당 알람 관련 내용 프론트에서 보냄
# 해당 알림 관련 내용으로 프롬프트 생성 -> 대화 시작

prompt_list_routine = [ '첫 문장의 내용은 시니어의 일상 루틴에 관한 알람 내용으로 아침, 점심, 저녁 안부나 시니어의 활동 수행 여부에 관한',
                        '내용으로 각 상황에 맞게 시니어에게 안부 인사나 수행에 관련 간단한 질문이나 대화를 한 두 문장으로 대화를 시작해줘' ]

@api_view(['POST'])
def routine(request):
    if request.method == 'POST':
        user_input = request.POST.get('text', '')
        print(f'Input: {user_input}')
        
        # Create prompt & Get response
        prompt = user_input.append(prompt_list_routine)
        response = get_ai_response(prompt)

        print(f'Response data: {response}')

        # If response exist update_list & Get response reply
        if response:
            update_list(response, prompt_list_routine)
            pos = response.find("\nAI: ")
            response = response[pos + 4:]
        else:
            response = "response message not exist"
        print(f'Reply: {response}')
        
        # Create output.wav file with response reply through text_to_speech func
        text_to_speech(response)

        # Set output.wav to FileResponse format
        f = open('media/output.wav', "rb")
        audio_response = FileResponse(f)
        audio_response.set_headers(f)

        return audio_response
    else:
        return JsonResponse({'error': 'POST request required'})
    
    prompt = [
        '1. 챗지피티 역할 지정하기 - 너의 역할은 일상생활에서 가벼운 대화를 나눠주는 말동무 역할이야'
        '2. 나의 상황, 문맥 알려주기 - 너는 혼자계셔서 외로우신 시니어들의 얘기를 들어주거나 간단한 질문들을 하면서 심심하시지 않으시도록 대화를 해주면 되'
        '3. 간결한 문장을 사용하기 - '
        '4. 구체적인 내용 작성하기'
        '5. 예시 들어주기'
        '6. 주제 선정'
        '7. 세부 내용 요청'
        '8. 포맷 지정 - 질문이나 답변은 너무 구체적이지 않도록 한문장에서 두문장 정도로 호응을 해주거나 대화 문맥에 맞게 대화를 이어나가면 되'
        '9. 스타일 지정 - 시니어 분과의 대화임으로 존댓말을 사용해줘'
        '0. 관련 질문 및 아이디어 생성'
        '1. 관련 키워드 및 문구 추가 - 다음은 시니어분의 정보 및 관심사 내용으로 대화에 간단하게 참고해도 좋아.'
    
    ]