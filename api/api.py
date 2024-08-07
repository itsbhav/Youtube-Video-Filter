# !pip install youtube_transcript_api
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
df=pd.read_csv("Video Filter Datasheet.csv")
from youtube_transcript_api import YouTubeTranscriptApi
import requests
import random
import os
def dataGatherer(videoId):
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet",
        "id": videoId,
        "key":os.getenv("YOUTUBE_KEY")
    }
    response = requests.get(url, params=params)
    videoId=videoId.replace(","," ")
    videoId=videoId.split()
    transcript=YouTubeTranscriptApi.get_transcripts(videoId,languages=('hi','en-US','en-IN','en-GB','en',))
    try:
        if response.status_code == 200:  
            response=response.json()
            for k in range(len(response['items'])):
                with open('Data.csv','a',encoding='utf-8') as f:
                    title=response['items'][k]['snippet']['title'].split()
                    for i in range(len(title)):
                        if ',' in title[i]:
                            title[i]=title[i].replace(",","")
                    title=' '.join(title)
                    f.write(f"{response['items'][k]['id']},{title},{response['items'][k]['snippet']['categoryId']},")
                    description=response['items'][k]['snippet'].get('description',"")
                    words = description.split()
                    for i in range(len(words)):
                        if ',' in words[i]:
                            words[i]=words[i].replace(",","")
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
                    f.write(f"{part1},{part2},{part3},")   
                    tags=response['items'][k]['snippet'].get('tags',"")
                    x=" ".join(tags)
                    f.write(f"{x},")
                    transcript[0][response['items'][k]['id']] = [x['text'] for x in transcript[0][response['items'][k]['id']] if ("[Music]" and "[संगीत]") not in x['text']]
                    if(len(transcript[0][response['items'][k]['id']])==0):
                        for i in range(30):
                            f.write(",")
                        f.write("\n")
                    for i in range(len(transcript[0][response['items'][k]['id']])):
                        if ',' in transcript[0][response['items'][k]['id']][i]:
                            transcript[0][response['items'][k]['id']][i]=transcript[0][response['items'][k]['id']][i].replace(',',' ')
                        if '\n' in transcript[0][response['items'][k]['id']][i]:
                            transcript[0][response['items'][k]['id']][i]=transcript[0][response['items'][k]['id']][i].replace('\n',' ')
                    total_sentences = len(transcript[0][response['items'][k]['id']])
                    part_size = total_sentences // 3

                    # Split the transcript into three parts
                    first_part = transcript[0][response['items'][k]['id']][:part_size]
                    middle_part = transcript[0][response['items'][k]['id']][part_size:2*part_size]
                    last_part = transcript[0][response['items'][k]['id']][2*part_size:]

                    random.shuffle(first_part)
                    random.shuffle(middle_part)
                    random.shuffle(last_part)

                    i=0
                    for x in first_part:
                        if(i==2):break
                        f.write(f"{x},")
                        i+=1
                    i=0
                    for x in middle_part:
                        if(i==2):break
                        f.write(f"{x},")
                        i+=1
                    i=0
                    for x in last_part:
                        if(i==1):break
                        f.write(f"{x},")
                        i+=1
                    f.write("\n")   
        else:
            print("frjn")
            print("Some Error occured")
            return
    except:
        print("jfvjn")
        print("Some error occured")

if __name__=="__main__":
    videoId= ""
    # videoId=",".join(df.iloc[80:,20])
    print(videoId)
    dataGatherer('AxRZJLeW5oc')