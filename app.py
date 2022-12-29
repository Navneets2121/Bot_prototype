# !pip install wikipedia

# !pip install newsapi-python

# !pip install pyjokes

# !pip install keras

import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer=WordNetLemmatizer()
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
import json
import pickle
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import keras
import numpy as np
from keras.models import Sequential
from keras.layers import Dense,Activation, Dropout
from keras.optimizers import SGD
import random


# nltk.download('popular')
import datetime # library for date and time
from pytz import timezone # to select timezone of INDIA (or any other country)
import smtplib # library used to send mails
from email.message import EmailMessage
#import pyautogui
import webbrowser as wb
from time import sleep
import wikipedia
#import pywhatkit
import requests
from newsapi import NewsApiClient
import pyjokes
import string 
import random
import psutil
lemmer=nltk.stem.WordNetLemmatizer()
from keras.models import load_model
model = load_model('model.h5')
import json
import random
intents = json.loads(open('data.json').read())
words = pickle.load(open('texts.pkl','rb'))
classes = pickle.load(open('labels.pkl','rb'))

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] +=1
                # print("word",w)
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res1 = model.predict(np.array([p]))
    res = res1[0]
    ERROR_THRESHOLD = 0.45
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    List=[]
    if not ints:
      tag="noanswer"
    else:
      tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            # print("tags are : " + tag)
            result = List.append(random.choice(i['responses']))
    return List,tag

def LemTokens(tokens):
  return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict=dict((ord(punct),None) for punct in string.punctuation)

def LemNormalize(text):
  return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

def time():
  Time = datetime.datetime.now(timezone('Asia/Calcutta')).strftime("%H:%M:%S") # H-> Hour, M-> Minutes, S-> Seconds
  ans = ("The current time is : " + Time)
  return Time

def day():
  Day = datetime.datetime.now().strftime("%A")
  ans = ("The current day is : " + Day)
  return Day

def date():
  Year = int(datetime.datetime.now().year)
  Month = int(datetime.datetime.now().month)
  Date = int(datetime.datetime.now().day)
  ans = (str(Date) + " " + str(Month) + " " + str(Year))
  return ans

def takeInput():
  var = input("\nPlease tell me how can i help you? : ")
  return str(var)

def sendEmail(receiver, subject, content):
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls() #tls -> transport layer security(used to make email secure)
  server.login("efahi56189@gmail.com", "56189efahi") #sender mail and mail id password required
  email = EmailMessage()
  email['From'] = "efahi56189@gmail.com"
  email['To'] = receiver
  email['Subject'] = subject
  email.set_content(content)
  server.send_message(email)
  server.close() 

  # enable less secure apps in gmail account to run this function

def sendWhatsMsg(phone_no, message):
  Message = message
  wb.open('https://web.whatsapp.com/send?phone='+phone_no+'&text='+Message)
  sleep(10)
  puautogui.press('enter')

def searchGoogle(query):
  wb.open('https://www.google.com/search?q='+query)

def news():
  newsapi = NewsApiClient(api_key = '99ccfefa3dfe4abc824d337eaa9e4a8a')
  # topic=input("Enter a topic:")
  topic = request.args.get('topic')
  data = newsapi.get_top_headlines(q=topic, language='en', page_size=5)
  newsdata = data['articles']
  newlist = [" "]
  # print(newsdata)
  for x,y in enumerate(newsdata):
    newlist.append(f'{x+1}'+ '.' + f'{y["description"]}')
    
  result='\n'.join([str(item) for item in newlist])
  return result

def passwordGen():
  s1 = string.ascii_uppercase
  s2 = string.ascii_lowercase
  s3 = string.digits
  s4 = string.punctuation

  passlength = 10
  s = []
  s.extend(list(s1))
  s.extend(list(s2))
  s.extend(list(s3))
  s.extend(list(s4))
  random.shuffle(s)

  newpass = ("".join(s[0:passlength]))
  ans =  newpass
  return ans

def flip():
  coin = ['head', 'tail']
  toss = []
  toss.extend(coin)
  random.shuffle(toss)
  toss = ("".join(toss[0]))
  
  return toss

def roll():
  die = ['1', '2', '3', '4', '5', '6']
  roll = []
  roll.extend(die)
  random.shuffle(roll)
  roll = ("".join(roll[0]))
  ans = ("output of the die rolled is "+roll)
  return roll

def cpu():
  usage = str(psutil.cpu_percent())
  ans = ("CPU is at "+ usage)
  return usage

def bot(msg):
  inp = msg.lower()
  # query = LemNormalize(inp)
  ints = predict_class(inp, model)
  List = getResponse(ints, intents)[0]
  tag=getResponse(ints, intents)[1]
  flag = True
  # operations
  if 'goodbye' in tag:
    return (List)

  if 'time' in tag:
    flag = False
    List.append(time())

  if 'day' in tag:
    flag = False
    List.append(day())

  if 'date' in tag:
    flag = False
    List.append(date())

  if 'email' in tag:
    flag = False
    try:
      receiver = request.args.get('receiver')
      subject = request.args.get('subject')
      content = request.args.get('content')
      sendEmail(receiver, subject, content)
      return ("email has been sent")
    except Exception as e:
      return ("404")

  if 'message' in tag:
    flag = False
    user_name = {
        'Navneet' : '+91 9814876595'
    }
    try:
      receiver = input("Please enter receiver's name : ")
      name = receiver.lower()
      phone_no = user_name[name]
      message = input("Please enter content of the msg : ")
      sendWhatsMsg(phone_no, message)
      return ("message has been sent")
    except Exception as e:
      return (e)

  if 'wikipedia' in tag:
    flag = False
    inp = inp.replace("wikipedia", "")
    result = wikipedia.summary(inp, sentences = 3)
    List.append(" " + result)

  if 'google' in tag:
    flag = False
    inp = inp.replace("google", "")
    result = wikipedia.summary(inp, sentences = 2)
    List.append(" " + result)

  if 'weather' in tag:
    flag = False
    # city=input("Enter city :")
    city = request.args.get('city')
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid=24a0a5534a7ced33763b94acb9e7d058'

    res = requests.get(url)
    data = res.json()

    weather = data['weather'] [0] ['main']
    temp = data['main']['temp']
    temp = round((temp - 32)*5/9)
    desp = data['weather'] [0] ['description']
    List.append(weather)
    List.append("The current temperature is : " + str(temp))

  if 'news' in tag:
    flag = False
    List.append(news())

  if 'joke' in tag:
    flag = False
    List.append(" " + pyjokes.get_joke())

  if 'password' in tag:
    flag = False
    List.append(passwordGen())

  if 'flip' in tag:
    flag = False
    List.append(flip())

  if 'roll' in tag:
    flag = False
    List.append(roll())

  if 'cpu' in tag:
    flag = False
    List.append(cpu())

  return (List)

# if __name__ == '__main__':
#   while(True):
#     msg=takeInput()
#     result= bot(msg)
#     reply=' '.join([str(item) for item in result])
#     print(reply)
#     if(msg== 'quit'):
#       break

from flask import Flask, render_template,request,jsonify
import numpy as np
app= Flask(__name__)

@app.route('/')
def home():
    return ("!! Welcome !!")

@app.route('/get', methods=['GET'])
def get_bot_response():
    userText = request.args.get('msg')
    result=bot(userText)
    reply=' '.join([str(item) for item in result])
    return (reply)

if __name__ == '__main__':
    # import socket
    # socket.setdefaulttimeout(10)
    app.run(host="0.0.0.0",)

# !pip freeze > requirements.text
