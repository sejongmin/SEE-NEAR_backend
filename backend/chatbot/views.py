from django.shortcuts import render

from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.http import FileResponse
from django.conf import settings
from .chatbotFunc.chatbotFunc import *

import os

name = '김숙자'
sex = 'female'
age = 60
interest = '임영웅', '봄', '강아지'
diasease = '당뇨'
prompt_list = [
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
        prompt = create_prompt(user_input, prompt_list)
        response = get_ai_response(prompt)

        print(f'Response data: {response}')

        # If response exist update_list & Get response reply
        if response:
            update_list(response, prompt_list)
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