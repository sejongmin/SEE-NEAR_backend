from wordcloud import WordCloud
from constant.conversation import *

def createWordCloud(text):
    wordcloud = WordCloud(
            background_color=BACKGROUND_COLOR,
            max_words=MAX_WORDS,
            width=WIDTH,
            height=HEIGHT,
            font_path=BASE_PATH + FONT_PATH
        ).generate(text)
    wordcloud.to_file(filename=BASE_PATH+WORDCLOUD_PATH)