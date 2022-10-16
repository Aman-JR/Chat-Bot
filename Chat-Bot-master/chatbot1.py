#This is a corona disease helpline/information chat box
#pip install newspaper3k
#or pip install newspaper
from newspaper import Article
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
#eg: "I am a student of graphic era university, I am in 6th sem. I live in Kanpur......" for questions like : "Who are you"
from sklearn.metrics.pairwise import cosine_similarity
#1.0 -> 100% match 0-> 0% match
import numpy as np
import warnings
# warneings.filterwarnings('ignore') to ignore warinings

#Download the punkt package
nltk.download('punkt',quiet=True)

#get the article
article= Article('https://en.wikipedia.org/wiki/Coronavirus')
article.download()
article.parse()
article.nlp()
corpu = article.text
article= Article('https://en.wikipedia.org/wiki/BTS')
article.download()
article.parse()
article.nlp()
corpu = corpu+' '+(article.text)
#print the article text
#print(corpu)

#tokennisation
test= corpu
sentence_list=nltk.sent_tokenize(test)
#A list of sentences will be produced
#print(sentence_list)

#A function to return a randon greeting message to a user
def greet_response(text):
    text= text.lower() #hello, HELLO, Hello
    bot_greet=['hello','hi','hey','wassup']
    user_greet=['hi','hello','helo','hiii','wassup','hey']
    #try using as many words as possible
    
    for word in text.split():
        if word in user_greet:
            return random.choice(bot_greet)

#index sort function
def index_sort(list_var):
    length=len(list_var)
    list_index=list(range(0,length))
    x=list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]]>x[list_index[j]]:
                #swap
                temp=list_index[i]
                list_index[i]=list_index[j]
                list_index[j]=temp
    
    return list_index

#Bot response to actual queries
def bot_response(user_input):
    #main function to response queries
    user_input=user_input.lower()
    sentence_list.append(user_input)
    bot_res=''
    cm = CountVectorizer().fit_transform(sentence_list)
    similarity_score=cosine_similarity(cm[-1],cm)
    similarity_score_list=similarity_score.flatten()
    #0.0, 0.4, 0.6, 0.2, 1.0, 0.9
    index=index_sort(similarity_score_list)
    index=index[1:]
    response_flag=0
    j=0
    for i in range(len(index)):
        if similarity_score_list[index[i]]>0.001:
            bot_res=bot_res+' '+sentence_list[index[i]]
            response_flag=1
            j=j+1
        if j>2:
            break
    if response_flag==0:
        bot_res= bot_res + 'I apologise, that I have not understood you meaning.'
    sentence_list.remove(user_input)
    return bot_res

#start the chat
print("Covid Helpline: I am here to help you with the inofomation regarding Covid virus. If you want to exit type bye or exit.")
exit_list=['bye','exit','byee','break','quit']
while(True):
    user_input=input()
    if user_input.lower() in exit_list:
        print("Bot: Thank you for connecting with us. See you later.")
        break
    else:
        if greet_response(user_input) != None:
            print('Bot: '+greet_response(user_input))
        else:
            print('Bot: '+bot_response(user_input))
