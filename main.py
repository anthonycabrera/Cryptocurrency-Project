from Coin import Coin
import requests
import json
import pyttsx3
import speech_recognition as sr
import re

API_KEY = "tp8yP9ssfNZa"
PROJECT_TOKEN = "tWSq7W7NXSjg"
RUN_TOKEN = "t0fRuqswy_zU"

class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key": self.api_key
        }
        self.getData()

    def getData(self):
        response = requests.get(f'http://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data', params=self.params)
        self.data = json.loads(response.text)

    def getCoinData(self, coin):
        data = self.data["coin"]

        for content in data:
            if content['name'].lower() == coin.lower():
                return content

        return "0"

    def getListOfCoins(self):
        coins = []
        for coin in self.data['coin']:
            coins.append(coin['name'])

        return coins

    def getListOfPrices(self):
        prices = []
        for price in self.data['coin']:
            prices.append(price['price'])
        return prices

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def getAudio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
        except Exception as e:
            print("Exception: ", str(e))

    return said.lower()

def buildCoin():
    array = []
    i = 0
    while (i < 100):
        array.append(Coin(cryptoNames[i], cryptoPrices[i]))
        i += 1
    return array

def searchCoin(coinName, list, engine):
    coinFound = False
    for coin in list:
        if (coin.getCoinName().lower() == coinName.lower()):
            print(coin)
            engine.say(coin)
            engine.runAndWait()
            coinFound = True
        
    if (not coinFound):
        print("Cryptocurrency " + coinName + " not found")

def listCoins(list):
    print("Top 100 Crytocurrency")
    for coins in list:
        print(coins)


def dashboard(coinL, engine):
    print("""Enter 1 to list top 100 Cryptocurrencies
Enter 2 to search for a coin using text
Enter 3 to search for a coin using speach recognition""")
    inpt = input()

    if (inpt == "1"):
        listCoins(coinL)
    elif (inpt == "2"):
        print("Enter coin")
        sCoin = input()
        searchCoin(sCoin, coinL, engine)
    elif (inpt == "3"):
        print("Listening...")
        sCoin = getAudio()
        searchCoin(sCoin, coinL, engine)
    else:
        print("Did not recognize input")

def main(coinL):
    gameOn = True
    engine = pyttsx3.init()
    print("Welcome")
    while (gameOn):
        dashboard(coinL, engine)
        print("Would you like to try again?")
        inpt = ""
        while (inpt != "yes" and inpt != "no"):
            print("Enter yes or no")
            inpt = input()
        if (inpt == "no"):
            gameOn = False
            print("Ok goodbye...")
        inpt = ""

data = Data(API_KEY, PROJECT_TOKEN)
cryptoNames = data.getListOfCoins()
cryptoPrices = data.getListOfPrices()
coinL = buildCoin()
main(coinL)