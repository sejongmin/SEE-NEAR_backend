import os
import datetime
from django.db.models import Q
from django.http import JsonResponse, FileResponse
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Post, DayReport
from .serializers import PostSerializer, DayReportSerializer, WeekReportSerializer
from .functions.chatbot import *
from .functions.keyword_extraction import *
from .functions.emotion_classification import *
from constant.conversation import *

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_post(request):
    try:
        serializer = PostSerializer()
        post = serializer.create(request.user.family_id)

        response_data = {"id": post.id}
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        response_data = {'error': e}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_post(request, pk):
    try:
        postSerializer = PostSerializer()
        post = Post.objects.get(pk=pk)

        keyword = keyword_extraction(TEXT_PATH)
        emotion = emotion_classification(AUDIO_INPUT_WAV_PATH)
        os.remove(TEXT_PATH)
        os.remove(AUDIO_INPUT_WAV_PATH)
        os.remove(AUDIO_INPUT_WEBM_PATH)
        os.remove(AUDIO_OUTPUT_PATH)

        data = {
            "content": "content",
            "emotion": 0,
            "keyword": "keyword"
        }

        postSerializer.update(post=post, data=data)

        reportSerializer = DayReportSerializer()
        report = reportSerializer.get_or_create(family=request.user.family_id, date=post.date)
        report = reportSerializer.update(report=report, data=data)

        response_data = {"message": UPDATE_POST_MESSAGE}
        return Response(response_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        response_data = {'error': e}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_posts(request, date):
    try:
        queryset = Post.objects.filter(
            Q(family_id=request.user.family_id) &
            Q(date=date)
        )

        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        response_data = {'error': e}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_report(request, date):
    try:
        queryset = DayReport.objects.get(
            Q(family_id=request.user.family_id) &
            Q(date=date)
        )

        serializer = DayReportSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        response_data = {'error': e}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_reports(request, date):
    try:
        queryset = DayReport.objects.filter(
            Q(family_id=request.user.family_id) &
            Q(date__year=date.year) &
            Q(date__month=date.month)
        )

        serializer = DayReportSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        response_data = {'error': e}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_week_report(request, start):
    try:
        start_day = start
        end_day = start_day + datetime.timedelta(days=6)

        queryset = DayReport.objects.filter(
            Q(family_id=request.user.family_id) &
            Q(date__range=[start_day, end_day])
        )

        serializer = WeekReportSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        response_data = {'error': e}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

prompt_list_default = [
    '너는 혼자계신 시니어분의 말동무 역할을 수행하게 될거야. 사용자의 정보를 알려줄게',
    f'시니어 분의 성별은 {sex}, 나이는 {age}세, 관심사는 {interest}, 질병은 {diasease}',
    '위 정보를 참고해서 이 분이 심심하지 않으시게 일상생활의 간단한 질문이나 대답을 해주면 되',
    '너무 자세하게 질문과 대답을 하기보단 호응해주고 맞춰주는 식으로 대화를 해줘',
    '무조건 존댓말로 대답해줘',
]

@api_view(['POST'])
def chatbot(request):
    if request.method == 'POST':
        user_input = request.POST.get('text', '')

        text_path = os.path.join(settings.MEDIA_ROOT, 'text.txt')
        if not os.path.exists(text_path):
            open(text_path, 'w').close()

        with open(text_path, 'a') as f:
            f.write(user_input + '\n')
        
        prompt = create_prompt(user_input, prompt_list_default)
        response = get_ai_response(prompt)

        if response:
            update_list(response, prompt_list_default)
            pos = response.find("\nAI: ")
            response = response[pos + 4:]
        else:
            response = "response message not exist"
        
        text_to_speech(response)

        f = open('media/output.wav', "rb")
        audio_response = FileResponse(f)
        audio_response.set_headers(f)

        return audio_response
    else:
        return JsonResponse({'error': 'POST request required'})