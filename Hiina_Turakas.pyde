import os, random
path = os.getcwd()

suits = ["clubs","diamonds,","hearts","spades"]
numbers = [2,3,4,5,6,7,8,9,10,"jack","queen","king","ace"]

class Card():
    def __init__(self,number,suit):
        self.number = number
        self.suit = suit
        self.img = loadImage(path+"/playing-cards-assets/png/"+str(self.number)+"_of_"+str(self.suit)+".png")
    
        print(self.img)
    
    def display(self):
        #self.x=x
        #self.y=y
        image(self.img,0,0)

        
class Deck():
    pass
class Hand():
    pass
    
card = Card(numbers[0],suits[0])
print(path+"/playing-cards-assets/png/"+str(card.number)+"_of_"+str(card.suit)+".png")
def setup():
    size(1280,720)
    background(0)
    
def draw():
    #background(0)
    card.display()
