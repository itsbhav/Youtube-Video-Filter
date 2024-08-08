# Idea Behind... 
YouTube has a lot of distraction for students, particularly during study time.  
As youtube has a vast domain of contents, students during study time switch to other videos for entertainment leading to loss of study time and concentration.  
So, a lot of institutions restrict youtube for employees and students in their premises.  
Instead, a model can be developed based on Natural Language Processing to classify the videos into two categories and the routers at institutions may allow only educational content.

# Tech Stack
This model based on Subtitles, Description, Tags, Category ID of Video, classifies the video into educational and non-educational.  
The model has used Two Linear Sequential Dense Layers and an output layer for processing the texts.  
The model uses nltk, a Natural Language Processing library. It also supports hindi as well as English texts for classification.  

# Metrics  
The model has 2301 videos , with 1200 educational videos and 1101 non-deucational videos.  
We have taken all tags used in the video, the category id of the video, three lines of description- from initial, middle and last part, five lines of subtitles from initial, middle and last parts of the video.  
80% data was used for training after stemming, filtration and cleaning. The other 20% was used as test data.
This resulted in a accuracy of 99.56%, with only two misclassifications.  
Some other models were also tried, like Logistic regression and XGBoost with accuracies of 99.33% and 98% accuracies.  
The ANN model being more accurate was used as a classifier.


# To run on local-host
1. Run "pip install -r requirements.txt"
2. Run "streamlit run model.py"
3. Type youtube video's id, videoid is of form https://www.youtube.com/watch?v=videoId
4. Click Classify

## It is deployed on https://youtube-video-filter.onrender.com