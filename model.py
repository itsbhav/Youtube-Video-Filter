from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

import numpy as np
import tensorflow as tf
from dotenv import load_dotenv
load_dotenv()

import string
import re
import nltk
import requests
import random
import joblib
import os

nltk.data.path.append('./nltk_data')

def dataGatherer(videoId):
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet",
        "id": videoId,
        "key":os.getenv("YOUTUBE_KEY")
    }
    response = requests.get(url, params=params)
    videoId = [videoId]
    transcript=dict()
    try:
        transcript = YouTubeTranscriptApi.get_transcripts(videoId, languages=('hi', 'en-US', 'en-IN', 'en-GB', 'en',))
    except:
        transcript='not available'
    if response.status_code == 200:
        response = response.json()
        for k in range(len(response['items'])):
            Title = response['items'][k]['snippet']['title']
            CategoryId = int(response['items'][k]['snippet']['categoryId'])
            Description = response['items'][k]['snippet'].get('description', "")
            words = Description.split()
            for i in range(len(words)):
                if ',' in words[i]:
                    words[i] = words[i].replace(",", "")
                if 'http' in words[i] or 'www' in words[i]:
                    words[i] = ''
                total_words = len(words)
                if total_words <= 75:
                    # If the total number of words is less than or equal to 75, split into three equal parts
                    part1 = ' '.join(words[:total_words//3])
                    part2 = ' '.join(words[total_words//3:2*(total_words//3)])
                    part3 = ' '.join(words[2*(total_words//3):])
                else:
                    # Otherwise, limit each part to 25 words
                    part1 = ' '.join(words[:25])
                    part2 = ' '.join(words[(total_words//2)-12:(total_words//2)+13])
                    part3 = ' '.join(words[-25:])
            Tags = response['items'][k]['snippet'].get('tags', "")
            Tags = " ".join(Tags)
            if(transcript=='not available'):
                first_part=''
                middle_part=''
                last_part=''  
            else:
                transcript[0][videoId[0]] = [x['text'] for x in transcript[0][videoId[0]] if "[Music]" not in x['text'] and "[संगीत]" not in x['text']]
                if len(transcript[0][videoId[0]]) == 0:
                    continue

                for i in range(len(transcript[0][videoId[0]])):
                    if ',' in transcript[0][videoId[0]][i]:
                        transcript[0][videoId[0]][i] = transcript[0][videoId[0]][i].replace(',', ' ')
                    if '\n' in transcript[0][videoId[0]][i]:
                        transcript[0][videoId[0]][i] = transcript[0][videoId[0]][i].replace('\n', ' ')
                total_sentences = len(transcript[0][videoId[0]])
                part_size = total_sentences // 3

                # Split the transcript into three parts
                first_part = transcript[0][videoId[0]][:part_size]
                middle_part = transcript[0][videoId[0]][part_size:2*part_size]
                last_part = transcript[0][videoId[0]][2*part_size:]

            random.shuffle(first_part)
            random.shuffle(middle_part)
            random.shuffle(last_part)
            
            dataset=[[Title,CategoryId,part1,part2,part3,Tags]]
            i = 0
            for x in first_part:
                if i == 2:
                    break
                dataset[0].append(x)
                i += 1
            i = 0
            for x in middle_part:
                if i == 2:
                    break
                dataset[0].append(x)
                i += 1
            i = 0
            for x in last_part:
                if i == 1:
                    break
                dataset[0].append(x)
                i += 1
            if(len(dataset[0])==6):
                dataset[0].append("")
                dataset[0].append("")
                dataset[0].append("")
                dataset[0].append("")
                dataset[0].append("")
    else:
        print("Some error occurred")
        return
    transformer_=joblib.load('column_transformer.pkl')
    # print(transformer_)
    dataset=transformer_.transform(dataset)
    # print(dataset)
    vectorizer=joblib.load('count_vectorizer.pkl')
    x=(
    '''पर
    इन
    वह
    यिह
    वुह
    जिन्हें
    जिन्हों
    किन्हों
    किन्हें
    इत्यादि
    द्वारा
    इन्हें
    इन्हों
    उन्हों
    बिलकुल
    इन्हीं
    उन्हीं
    उन्हें
    इसमें
    जितना
    दुसरा
    कितना
    कितने
    कितनो
    वग़ैरह
    दूसरे
    कौनसा
    लेकिन
    होता
    करने
    किया
    लिये
    अपने
    नहीं
    दिया
    इसका
    करना
    वाले
    सकते
    इसके
    सबसे
    होने
    करते
    बहुत
    करें
    होती
    अपनी
    उनके
    कहते
    होते
    करता
    उनकी
    इसकी
    सकता
    रखें
    अपना
    उसके
    जिसे
    किसे
    किसी
    काफ़ी
    पहले
    नीचे
    यहाँ
    जैसा
    जैसे
    मानो
    अंदर
    भीतर
    पूरा
    सारा
    होना
    उनको
    वहाँ
    वहीं
    जहाँ
    जीधर
    उनका
    इनका
    के
    हैं
    गया
    बनी
    एवं
    हुआ
    साथ
    बाद
    लिए
    कुछ
    कहा
    यदि
    हुई
    इसे
    हुए
    अभी
    सभी
    कुल
    रहा
    रहे
    इसी
    उसे
    जिस
    जिन
    कौन
    किस
    कोई
    ऐसे
    तरह
    संग
    यही
    उसी
    फिर
    मगर
    का
    एक
    यह
    से
    को
    इस
    कि
    जो
    कर
    मे
    ने
    तो
    ही
    या
    हो
    था
    तक
    आप
    ये
    थे
    दो
    वे
    थी
    जा
    ना
    उस
    पे
    उन
    भी
    और
    घर
    तब
    जब
    व
    न''').split('\n')
    stopwords_hinglish = set(stopwords.words('hinglish')).union(set(stopwords.words('english'))).union(set(x))
    stopwords_hinglish.add('subscribe')
    stopwords_hinglish.add('telegram')
    stopwords_hinglish.add('channel')
    stopwords_hinglish.add('link')
    stopwords_hinglish.add('follow')
    stopwords_hinglish.add('instagram')
    stopwords_hinglish.add('whatsapp')
    stopwords_hinglish.add('facebook')
    stopwords_hinglish.add('twitter')
    stopwords_hinglish.add('youtube')
    stopwords_hinglish.add('linkedin')
    stopwords_hinglish.add('pinterest')
    stopwords_hinglish.add('snapchat')
    stopwords_hinglish.add('tiktok')
    stopwords_hinglish.add('medium')
    stopwords_hinglish.add('reddit')
#     print(stopwords_hinglish)
    corpus=[]
    for i in range(len(dataset)):
      word_lists=''
      for j in range(14,len(dataset[0])):
        text=str(dataset[i,j])
#         print(text)
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = re.sub(r'\d+', '', text)
        symbol_pattern = re.compile(
            "["
            u"\U0001F600-\U0001F64F"  # Emoticons
            u"\U0001F300-\U0001F5FF"  # Symbols & Pictographs
            u"\U0001F680-\U0001F6FF"  # Transport & Map Symbols
            u"\U0001F1E0-\U0001F1FF"  # Flags (iOS)
            u"\U00002702-\U000027B0"  # Dingbats
            u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
            u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
            u"\U00002600-\U000026FF"  # Miscellaneous Symbols
            u"\U0001F700-\U0001F77F"  # Alchemical Symbols
            u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
            u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
            u"\U0001FA00-\U0001FA6F"  # Chess Symbols
            u"\U00002500-\U00002BEF"  # Various symbols (including arrows and more)
            u"\U00002300-\U000023FF"  # Miscellaneous Technical
            u"\U00002000-\U000020FF"  # General Punctuation
            u"\U0001F1E6-\U0001F1FF"  # Regional Indicator Symbols
            "]+", flags=re.UNICODE
        )
        text=symbol_pattern.sub(r'',text)
        ps=PorterStemmer()
    #     text=normalizer.normalize(text)
        text=word_tokenize(text)
        text=[ps.stem(word) for word in text if word not in stopwords_hinglish]
        suffixes = {
        1: [u"ो",u"े",u"ू",u"ु",u"ी",u"ि",u"ा"],
        2: [u"कर",u"ाओ",u"िए",u"ाई",u"ाए",u"ने",u"नी",u"ना",u"ते",u"ीं",u"ती",u"ता",u"ाँ",u"ां",u"ों",u"ें"],
        3: [u"ाकर",u"ाइए",u"ाईं",u"ाया",u"ेगी",u"ेगा",u"ोगी",u"ोगे",u"ाने",u"ाना",u"ाते",u"ाती",u"ाता",u"तीं",u"ाओं",u"ाएं",u"ुओं",u"ुएं",u"ुआं"],
        4: [u"ाएगी",u"ाएगा",u"ाओगी",u"ाओगे",u"एंगी",u"ेंगी",u"एंगे",u"ेंगे",u"ूंगी",u"ूंगा",u"ातीं",u"नाओं",u"नाएं",u"ताओं",u"ताएं",u"ियाँ",u"ियों",u"ियां"],
        5: [u"ाएंगी",u"ाएंगे",u"ाऊंगी",u"ाऊंगा",u"ाइयाँ",u"ाइयों",u"ाइयां"],
        }
        stems=[]
        for word in text:
          for L in range(1,5):
            if len(word) >= L + 1:
                for suffix in suffixes[L]:
                    if word.endswith(suffix):
                        word=word[:-L] #stripping the suffix from the word
          if word:
            stems.append(word)
        text=stems
        text=' '.join(text)
        word_lists+=text+' '
      corpus.append(word_lists)
#     print(corpus)
    X_text=vectorizer.transform(corpus).toarray()
#     print(type(np.array(X_text)))
    X_text=np.array(X_text)
#     print(X_text.shape)
#     print(dataset)
    dataset=np.concatenate((dataset[:,:14],X_text),axis=1)
#     print(dataset)
    ann_model=tf.keras.models.load_model('video_filter.keras')
    result=ann_model.predict(np.array(dataset).astype('float64'))
    if(result>0.5):
        print(f'The video {videoId[0]} is an Educational content')
        return f'The video {videoId[0]} is an Educational content'
    else:
        print(f'Video {videoId[0]} does not seem to be an educational content.')
        return f'Video {videoId[0]} does not seem to be an educational content.'
    
import streamlit as st
def main():
    st.title("YouTube Video Content Classifier")
    video_id = st.text_input("Enter YouTube Video ID:", "")
    if st.button("Classify"):
        if video_id:
           x=dataGatherer(video_id)
           st.subheader(x)
        else:
            st.warning("Please enter a valid YouTube Video ID")
if __name__ == "__main__":
    main()
