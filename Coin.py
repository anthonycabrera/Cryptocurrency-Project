class Coin:
    def __init__(self, coinName, price):
        self.coinName = coinName
        self.price = price

    def __str__(self):
        string = "The current price of " + self.getCoinName()
        string += " is " + str(self.getPrice())
        return string

    def getCoinName(self):
        return self.coinName 
    
    def getPrice(self):
        return self.price
