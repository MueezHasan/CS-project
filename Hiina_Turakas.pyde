import os, random
path = os.getcwd()

suits = ["clubs","diamonds","hearts","spades"]
values = {2:15,3:3,4:4,5:5,6:6,7:15,8:15,9:9,10:15,"jack":11,"queen":12,"king":13,"ace":14}
values7 = {2:1,3:3,4:4,5:5,6:6,7:1,8:1,9:9,10:1,"jack":11,"queen":12,"king":13,"ace":14}        # in case a 7 is played, special cards need to be always legal

#size_x = 1400
#size_y = 1050
#size_x = 1600
#size_y = 900


class Card():
    def __init__(self,number,suit,state="uncovered"):
        self.number = number
        self.suit = suit
        self.value = values[self.number]
        self.value7 = values7[self.number]
        self.state = state
        
    
    def display(self,x,y):
        self.x = x
        self.y = y
        self.img = loadImage(path+"/playing-cards-assets/png/"+str(self.number)+"_of_"+str(self.suit)+".png")
        image(self.img,self.x,self.y,100,145)
        stroke(0)
        strokeWeight(0.5)
        noFill()
        rect(self.x,self.y,100,145)


        if self.state == "covered":
            self.img = loadImage(path+"/playing-cards-assets/png/back@2x.png")
            image(self.img,self.x,self.y,100,145)
            






class Stack(list):      # the top card in the stack has a list index 0
    def __init__(self):
        self.last_visible = 3   # index of the last visible displayed card defaulted to top card
        self.cnt = 0            # default x-length at start
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
        game.deck.MoveTo(game.deck[0],self)
    
    def display(self,x,y):
        self.x = x
        self.y = y
        self.cnt = 0   
        if self.last_visible <= 3:
            self.first_visible = None
        else:
            self.first_visible = self.last_visible - 4
        for v in self[self.last_visible:self.first_visible:-1]:
            v.display(self.x+self.cnt,self.y)
            self.cnt += 30
        text (len(self),self.x,self.y+170)
        
    
    # gets called by mouseclick function
    def change_last_visible(self,increase):
        if increase == True:
            self.last_visible += 1
        else:
            self.last_visible -= 1

        if self.last_visible > len(self):
            self.last_visible = len(self)-1
        elif self.last_visible < 0:
            self.last_visible = 0
                    
        return self.last_visible
        
        




class TableCards(Stack):
    def __init__(self,covered):
        Stack.__init__(self)
        self.covered = covered
        for count in range(3):
            DrawCard()
        




class Hand(Stack):
    def __init__(self):
        Stack.__init__(self)
        self.last_visible = 5
        self.cnt = 780     # starts with 6 cards, that means length 780
        
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
    
    def display(self,x,y):
        self.x = x
        self.y = y
        self.cnt = 0   
        if self.last_visible <= 7:
            self.first_visible = None
        else:
            self.first_visible = self.last_visible - 8
        for v in self[self.last_visible:self.first_visible:-1]:
            v.display(self.x+self.cnt,self.y)
            self.cnt += 130
        rect(self.x-30,self.y+70,20,20)
        rect(self.x+780,self.y+70,20,20)
            
    # moves a card to the active pile
    def PlayCard(self,card):
        self.MoveTo(card,game.active_pile)
    
    # checks if a selected card in a hand can be played on the active pile
    def Islegal(self,card):
        if  game.active_pile[0].number == 7:
            if (game.active_pile[0]).value7 >= card.value7:
                return True
        elif (game.active_pile[0]).value <= card.value:
            return True
        else:
            return False





# A deck is a stack that starts with 52 cards instead of being empty upton creation
class Deck(Stack):
    def __init__(self):
        Stack.__init__(self)
        self.cnt = 190
        for n in values.keys():
            for s in suits:
                self.append(Card(n,s))
        
    def display(self,x,y):
        self.x=x
        self.y=y 
        self.img = loadImage(path+"/playing-cards-assets/png/back@2x.png")
        if len(self)!=0:
            image(self.img,self.x,self.y,100,145)
            stroke(0)
            strokeWeight(0.5)
            noFill()
            rect(self.x,self.y,100,145)
            text (len(self),self.x,self.y+170)
        # add number of cards as text below it
    





class HiinaTurakas:
    def __init__(self):
        self.players = ["Player 1", "Player 2", "Player 3", "Player 4"]
        self.turn = 0
        self.active_pile = Stack()
        self.discard_pile = Stack()
        self.deck = Deck()
        print("deck initialized")
        random.shuffle(self.deck)
    
    def display(self):
        self.active_pile.display((1325)//2,(755)//2)
        self.deck.display(400,(755)//2)
        self.discard_pile.display(1000,(755)//2)
        
    def addPlayer(num):
        name = "Player "+ str(num)
        if name not in self.players:
            self.players.append(name)
        self.players.sort()
    
    def removePlayer(num):
        name = "Player "+ str(num)
        if name in self.players:
            self.players.remove(name)

        
# initializing

game = HiinaTurakas()
hand1 = Hand() 
hand2 = Hand()

   
for count in range(6):
    hand1.DrawCard()
    game.deck.MoveTo(game.deck[count],game.active_pile)
    hand2.DrawCard()
game.active_pile.MoveStack(game.discard_pile)
for count in range(5):
    game.deck.MoveTo(game.deck[count],game.active_pile)
    

#print(path+"/playing-cards-assets/png/"+str(card.number)+"_of_"+str(card.suit)+".png")
def setup():
     
    #size(1280,720)
    #size(1280,960)
    #size(1400,1050)
    #size(size_x,size_y)
    size(1600,900)
    background(120,147,83)
    
def draw():
    textSize(20)
    fill(0,0,0)

    #hand1.display((size_x//2)-hand1.cnt//2,20)
    #hand2.display((size_x-hand2.cnt)//2,size_y-145-20)
    #game.active_pile.display((size_x-275)//2,(size_y-145)//2)
    #game.deck.display(size_x//4,(size_y-145)//2)
    #game.discard_pile.display((3*size_x)//4-200,(size_y-145)//2)

    hand1.display(800-hand1.cnt//2,20)
    hand2.display((1600-hand2.cnt)//2,735)
    game.display()
    pass
