# chatbot.py constant
GPT_MODEL = 'gpt-4o'
GPT_ROLE = 'system'
MAX_TOKENS = 10
TEMPERATURE = 0.8
TTS_MODEL = 'tts-1-hd'
TTS_VOICE = 'alloy'
TTS_SPEED = 1
AUDIO_RESPONSE_FORMAT = 'wav'

# emotion_classification.py constant
EMOTION_MODEL = 'media/Speech-Emotion-Recognition-Model_FINAL.h5'
N_MFCC = 13
N_FFT = 2048
HOP_LENGTH = 512
SAMPLE_RATE = 22050
MAX_LENGTH = 100

# keyword_extraction.py constant
KEYWORD_MODEL = 'skt/kobert-base-v1'

# views.py constant
TEXT_PATH = 'media/text.txt'
TEXT_PATH_2 = 'text.txt'
AUDIO_INPUT_WAV_PATH = 'media/input.wav'
AUDIO_INPUT_WEBM_PATH = 'media/input.webm'
AUDIO_OUTPUT_PATH = 'media/output.wav'
ENCODING = 'utf-8'

CONVERSATION_START_MESSAGE = 'Conversation Started!!'
CONVERSATION_END_MESSAGE = 'Conversation Ended!!'
NONE_RESPONSE_MESSAGE = 'response message does not exist'
POST_REQUEST_ERROR_MESSAGE = 'POST request required'