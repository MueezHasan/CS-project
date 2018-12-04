import os, random
path = os.getcwd()

suits = ["clubs","diamonds,","hearts","spades"]
values = {2:15,3:3,4:4,5:5,6:6,7:15,8:15,9:9,10:15,"jack":11,"queen":12,"king":13,"ace":14}
values7 = {2:1,3:3,4:4,5:5,6:6,7:1,8:1,9:9,10:1,"jack":11,"queen":12,"king":13,"ace":14}        # in case a 7 is played, special cards need to be always legal


class Card():
    def __init__(self,number,suit):
        self.number = number
        self.suit = suit
        self.img = loadImage(path+"/playing-cards-assets/png/"+str(self.number)+"_of_"+str(self.suit)+".png")
        self.value = values[self.number]
        self.value7 = values7[self.number]
    
    
    def display(self):
        #self.x=x
        #self.y=y
        image(self.img,0,0,100,145)

class Stack(list):      # the top card in the stack has a list index 0
    def __init__(self):
        pass

    # used for the active pile, covers discarding (move stack to discard pile) and picking up (move stack to hand) 
    def MoveStack(self,target):
        temp_list = self[::-1]   # moves the bottom cards first
        for card in temp_list:
            self.remove(card)
            target.insert(0,card)

    def MoveTo(self,card, target): 
        target.insert(0,card)
        self.remove(card)

    def DrawCard(self):
        deck.MoveTo(deck[0],self)
        
class TableCards(Stack):
    def __init__(self,covered):
        Stack.__init__(self)
        self.covered = covered
        for count in range(3):
            DrawCard()
        
class Hand(Stack):
    def __init__(self):
        Stack.__init__(self)
    
    def OrderCards(self):
        self.orderedcards=[] # makes a separate list in which  the sorted out values are added 
        for i in self: # goes through each of the cards in the original cards list, takes out their values and puts them inside the recently made list 
            a = i.value
            self.orderedcards.append(a)
        order = sort(self.orderedcards) # the list of values is now sorted according to their numeric value. 

        for v in order: # from the ordered list of values, you use each value to give you the key and the string from the dictionary that we created. 
            hello = []
            lol = values.get(v)
            hello.append(lol)
            
            # TODO: what if there are different cards with the same values?

    # moves a card to the active pile
    def PlayCard(self,card):
        self.MoveTo(card,active_pile)
    
    # checks if a selected card in a hand can be played on the active pile
    def Islegal(self,card):
        if  active_pile[0].number == 7:
            if (active_pile[0]).value7 >= card.value7:
                return True
        elif (active_pile[0]).value <= card.value:
            return True
        else:
            return False
            

class Deck(Stack):
    def __init__(self):
        Stack.__init__(self)
        for n in values.keys():
            for s in suits:
                self.append(Card(n,s))
        
    def ShuffleCards():
        self.cards.shuffle()



class HiinaTurakas:
    def __init___(self):
        pass

        
    
active_pile = Stack()
discard_pile = Stack()
    

deck = Deck()
#hand = Hand()

#print(path+"/playing-cards-assets/png/"+str(card.number)+"_of_"+str(card.suit)+".png")
def setup():
    size(1280,720)
    background(0)
    
def draw():
    #background(0)
    card.display()
