import os, random, time
path = os.getcwd()


suits = ["clubs","diamonds","hearts","spades"]
values = {2:15,3:3,4:4,5:5,6:6,7:15,8:15,9:9,10:15,"jack":11,"queen":12,"king":13,"ace":14}
values7 = {2:1,3:3,4:4,5:5,6:6,7:1,8:1,9:9,10:1,"jack":11,"queen":12,"king":13,"ace":14}        # in case a 7 is played, special cards need to be always legal


class Card():
    def __init__(self,number,suit,state="uncovered"):
        self.number = number
        self.suit = suit
        self.value = values[self.number]
        self.value7 = values7[self.number]
        self.state = state
        self.x = None
        self.y = None

    def __str__(self):
        return (str(self.number)+" of "+str(self.suit))
    
    def display(self,x,y):
        self.x = x
        self.y = y

        if self.state == "covered":
            self.img = loadImage(path+"/playing-cards-assets/png/back@2x.png")
            image(self.img,self.x,self.y,100,145)
        elif self.state == "uncovered":
            self.img = loadImage(path+"/playing-cards-assets/png/"+str(self.number)+"_of_"+str(self.suit)+".png")
            image(self.img,self.x,self.y,100,145)
        
        stroke(0)
        strokeWeight(0.5)
        noFill()
        rect(self.x,self.y,100,145)

    def uncover(self):
        self.state = "uncovered"


# A stack is any collection of cards, it is based on a list
class Stack(list):      # the top card in the stack has a list index 0
    def __init__(self, arrows = False):
        self.arrows = arrows
        self.last_visible = 3   # index of the last visible displayed card defaulted to top card
        self.cnt = 0            # default x-length at start
        self.rightclick = loadImage(path+"/rightclick.png")
        self.leftclick = loadImage(path+"/leftclick.png")
        self.noleft = loadImage(path+"/noleft.png")
        self.noright = loadImage(path+"/noright.png")
        self.canleft = False       # Booleans that decide whether stack can be scrolled
        self.canright = False
        
    # used for the active pile, covers discarding (move stack to discard pile) and picking up (move stack to hand) 
    def moveStack(self,target):
        temp_list = self[::-1]   # moves the bottom cards first
        for card in temp_list:
            self.remove(card)
            target.insert(0,card)

    # uncovers and moves a single card
    def moveTo(self,card, target):
        card.uncover()
        target.insert(0,card)
        self.remove(card)
    
# orders the cards in the stack from highest (index 0) to lowest (max index)    
    def order(self):
        #print "for the order"
        for count in range(len(self)):
            for a in range(count):
                if self[count].value > self[a].value:
                    card = self.pop(count)
                    self.insert(a,card)
    
    def drawCard(self):
        game.deck.moveTo(game.deck[0],self)
    
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
            
        # adds number of cards as text below it
        fill (255)
        text (len(self),self.x,self.y+170)

        # adds scrolling arrows if necessary            
        if self.arrows == True and len(self) > 3:
            if self.first_visible == None:         # can not scroll further to the right
                image(self.noright,self.x + 200,self.y,25,145)
                self.canright = False
            else:
                image(self.rightclick, self.x + 200, self.y,25,145)
                self.canright = True
            if self.last_visible == len(self)-1:   # can not scroll further to the left
                image(self.noleft,self.x - 35,self.y,25,145)
                self.canleft = False
            else:
                image(self.leftclick, self.x - 35, self.y,25,145)
                self.canleft = True
            
    
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
        
# checks if a selected card can be played on the active pile
    def isLegal(self,card,cnt=0):
        if len(game.active_pile) == cnt:
            return True
        elif game.userPlayed != False:
            if card.number == game.userPlayed:
                return True
            else:
                return False
        else:
            if  game.active_pile[cnt].number == 7 and 7 >= card.value7:
                return True
            elif game.active_pile[cnt].number == 8:
                return self.isLegal(card,cnt+1) 
            elif game.active_pile[cnt].number == 2:
                return True
            elif (game.active_pile[cnt]).value <= card.value:
                return True
            else:
                return False    

# The table cards are stacks containing the cards that get played when the deck is emptied
class TableCards(Stack):
    def __init__(self,state = "uncovered"):
        Stack.__init__(self)
        self.state = state
        
        
    def display(self,x,y):
        self.x = x
        self.y = y
        self.cnt = 0
        if self.state == "uncovered":
            for v in self:
                v.display(self.x+ self.cnt, self.y)
                self.cnt += 110
    
        elif self.state == "covered":
            for card in self:
                card.state = "covered"
            for v in self:
                v.display(self.x+ self.cnt, self.y)
                self.cnt += 110
        
    def clicked(self,card):
        self.moveTo(card,game.handBottom)

# A hand is a stack consisting of the cards that a player has at the moment.
class Hand(Stack):
    def __init__(self,state="uncovered"):
        Stack.__init__(self)
        self.last_visible = 5
        self.cnt = 780     # starts with 6 cards, that means length 780
        self.state = state
    
            
    def display(self,x,y):
        self.x = x
        self.y = y
        self.cnt = 0   

        if self.last_visible <=5:
            self.first_visible = None
        else:
            self.first_visible = self.last_visible - 6            
        if self.state == "covered":
            for card in self:
                card.state = "covered"
        else:
            for card in self:
                card.state = "uncovered"

        for v in self[self.last_visible:self.first_visible:-1]:
            v.display(self.x+self.cnt,self.y)
            self.cnt += 130
        
        if self.state == "uncovered":
            cnt = 0 
            for card in self[self.last_visible:self.first_visible:-1]:
    
                if self.isLegal(card) == False:    # greys out the cards that can't be played
                    self.greycard = loadImage(path+"/greycard.png")
                    image(self.greycard,self.x+cnt,self.y)
                cnt += 130
            while(cnt < 760):
                cnt += 130
            if len(self)>5:   # displays arrows only if the hand has at least 6 cards
                if self.first_visible == None:         # can not scroll further to the right
                    image(self.noright,self.x + 760,self.y,25,145)
                    self.canright = False
                else:
                    image(self.rightclick, self.x + 760, self.y,25,145)
                    self.canright = True
                if self.last_visible == len(self)-1:   # can not scroll further to the left
                    image(self.noleft,self.x - 35,self.y,25,145)
                    self.canleft = False
                else:
                    image(self.leftclick, self.x - 35, self.y,25,145)
                    self.canleft = True

                
    # moves a card to the active pile
    def playCard(self,card):
        self.moveTo(card,game.active_pile)
        if self.last_visible == len(self) and len(self)>5:
            self.change_last_visible(increase="False")
    
        
    def clicked(self,card):        
        if self.isLegal(card):
            self.playCard(card)


# A deck is a stack that starts with 52 cards instead of being empty upon creation
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
        if len(self)>0:
            image(self.img,self.x,self.y,100,145)
            fill (255)
            text (len(self),self.x,self.y+170)
        # adds number of cards as text below it

    

# the main game class
class HiinaTurakas:
    def __init__(self):
        
        # initialising boolean variables
        self.prepRound = True          # the first round is the preparation round
        self.cpuStarts = None          # who starts the game?
        self.userPlayed = False        # has the user played a card on his turn?
        self.blockEnd = True           # blocks the 'end turn' button
        self.blockDeck = True          # blocks the player from drawing cards from the deck
        self.gameend = False           # win/lose condition
        self.won = None                # the winner of the game
        self.specialcards = loadImage(path+"/specialcard.png") #the image for the special card information box
        self.instrucimg = loadImage(path+"/Imageofinstructions.png") #the image for the instructions box
        
        self.greycard = loadImage(path+"/greycard.png")    # the image to grey out cards
        
        # starting the stacks
        self.active_pile = Stack(arrows=True)
        self.discard_pile = Stack(arrows=True)
        self.handTop = Hand("covered")
        self.handBottom = Hand()
        self.tableB1 = TableCards()
        self.tableB2 = TableCards("covered")
        self.tableT1 = TableCards()
        self.tableT2 = TableCards("covered")
        self.deck = Deck()
        random.shuffle(self.deck)
        
        # for starting a new game
        self.Game_New = False
        self.death = Rebirth()
        

    def display(self):
        
        background(120,147,83)
        
        self.active_pile.display((1325)//2,(755)//2)
        self.deck.display(400,(755)//2)
        self.discard_pile.display(1000,(755)//2)
        self.handTop.display(440,20)
        self.handBottom.display(440,735)
            
        self.tableB2.display(600,580)
        self.tableB1.display(612,570)
        self.tableT2.display(622,175)    
        self.tableT1.display(610,185)
        
        fill (255)
        if self.Game_New == False:
            rect(80,60,150,70)
            fill (0)
            text ("New Game", 100,100)
        else:
            self.death.commit()
        
        if self.blockEnd:
            fill (200)
        else:
            fill (255)
        rect(150,735,150,120)
        if self.blockEnd:
            fill(70)
        else:
            fill (0)
        text ("End Turn", 170,795)
        
        if self.blockDeck and len(self.deck) > 0:
            image(self.greycard,self.deck.x,self.deck.y)
        
        if len(self.deck) > 0 or len(self.handBottom):
            for cnt in range(len(self.tableB1)): 
                image(self.greycard,self.tableB1.x+cnt*110,self.tableB1.y)

        image(self.instrucimg,1250,60)
        self.specialcards = loadImage(path+"/specialcard.png")
        image(self.specialcards,80,200,250,400)

        
        if self.gameend != True:
            self.gameplay()
        elif self.won == "The computer has won!":
            rect(self.handTop.x,self.handTop.y,300,100)
            fill(255)
            text(self.won, self.handTop.x+20, self.handTop.y+60)
        else:
            rect(self.handBottom.x,self.handBottom.y,300,100)
            fill(255)
            text(self.won, self.handBottom.x+20, self.handBottom.y+60)

# initializer function that fills the stacks from cards from the deck
# called after everything is instantiated                    
    def startHands(self):
        for count in range(6):
            self.handTop.drawCard()
            self.handBottom.drawCard()
        self.handBottom.order()
        self.handTop.order()
        for count in range(3):
            self.tableB2.drawCard()
            self.handTop.moveTo(self.handTop[0],self.tableT1)
            self.tableT2.drawCard()
        self.tableT1.order()
        self.tableT2.order()

# decides who starts first based on lower card
    def whoBegins(self):
        if self.handTop[2].value < self.handBottom [2].value:
            self.cpuStarts = True
        elif self.handTop[2].value == self.handBottom [2].value:   
    # same value --> chooses randomly
            choice = random.randint(0,1)
            if choice == 0:
                self.cpuStarts = True
        else:
            self.cpuStarts = False
   
# checks whether to discard the active pile
# discards when 10 is played or when there are 4 of the same numbers played in a row         
    def activeCount(self):
        self.sequential = 0
        num = self.active_pile[0].number
        if len(self.active_pile)>=4:
            for cnt in range(4):
                if self.active_pile[cnt].number == num:
                    self.sequential += 1
        if self.sequential == 4 or num == 10:
            time.sleep(0.5)
            self.active_pile.moveStack(self.discard_pile)
            self.userPlayed = False
            self.blockEnd = True
            
            
    def click(self):
        r = mouseX
        c = mouseY

    # finds whether the new game button was clicked        
        if  80 <= mouseX <=230 and 60 <= mouseY <=130:
            self.Game_New = True
            
    # finds whether a card in the hand was clicked
        if self.gameend != True:
            for card in self.handBottom[self.handBottom.last_visible:self.handBottom.first_visible:-1]:
                if card.x != None and card.y != None and card.x < mouseX < card.x+100 and card.y < mouseY < card.y+145:
                    if self.prepRound == True:  # during the initial round, add cards in front of the hand
                        self.tableB1.append(card)
                        self.handBottom.remove(card)
                    else:
                        if len(self.deck) !=0 and len(self.handBottom) < 3:
                            self.blockEnd = True
                        self.handBottom.clicked(card)   # otherwise add them to the active pile
                        if self.handBottom.isLegal(card):
                            if len(self.handBottom) >= 3 and card.number !=2:
                                self.blockEnd = False     # if player does not need to pick up and is not forced to play, enable turn end
                            if card.number != 2 and self.userPlayed == False:
                                self.userPlayed = card.number
                                if len(self.deck) == 0:
                                    self.blockEnd = False
    
        
    # finds whether a tablecard was clicked
        if self.gameend != True and len(self.handBottom) == 0 and len(self.deck) == 0:
            if len(self.tableB1) == 0:
                for card in self.tableB2:
                    if card.x < mouseX < card.x+100 and card.y < mouseY < card.y+145:
                        self.tableB2.clicked(card)
            else:
                for card in self.tableB1:
                    if card.x < mouseX < card.x+100 and card.y < mouseY < card.y+145:
                        self.tableB1.clicked(card)
                        
        
    # clicking the deck picks up a card
        if self.blockDeck == False and 400 < mouseX < 500 and (755)//2 < mouseY < (755)//2 + 145:
            self.handBottom.drawCard() 
            self.handBottom.order()
            if len(self.handBottom) == 3 or len(self.deck) == 0:
                if len(self.active_pile) != 0 and self.active_pile[0].number != 2:
                    self.blockEnd = False

            
    # clicking the active pile moves content to hand
        if self.gameend != True and self.prepRound != True and len(self.active_pile) > 0 and self.userPlayed == False and self.active_pile.x <= mouseX < self.active_pile.x+200 and self.active_pile.y <= mouseY <= self.active_pile.y+145:
            self.active_pile.moveStack(self.handBottom)
            self.handBottom.order()
        # and skips your turn    
            self.cpuPlays()
            
                           
    # hand's left button
        if self.handBottom.x-35 <= mouseX < self.handBottom.x and self.handBottom.y <= mouseY <= self.handBottom.y+100 and self.handBottom.canleft == True:
            self.handBottom.change_last_visible(increase = True)
    # hand's right button
        if self.handBottom.x + 760 < mouseX <= self.handBottom.x + 795 and self.handBottom.y <= mouseY <= self.handBottom.y+100 and self.handBottom.canright == True:
            self.handBottom.change_last_visible(increase = False)

    # active pile's left button
        if self.active_pile.x-35 <= mouseX < self.active_pile.x and self.active_pile.y <= mouseY <= self.active_pile.y+100 and self.active_pile.canleft == True:
            self.active_pile.change_last_visible(increase = True)
    # active pile's right button
        if self.active_pile.x+200 < mouseX <= self.active_pile.x+235 and self.active_pile.y <= mouseY <= self.active_pile.y+100 and self.active_pile.canright == True:
            self.active_pile.change_last_visible(increase = False)
            
    # discard pile's left button
        if self.discard_pile.x-35 <= mouseX < self.discard_pile.x and self.discard_pile.y <= mouseY <= self.discard_pile.y+100 and self.discard_pile.canleft == True:
            self.discard_pile.change_last_visible(increase = True)
    # discard pile's right button
        if self.discard_pile.x+200 < mouseX <= self.discard_pile.x+235 and self.discard_pile.y <= mouseY <= self.discard_pile.y+100 and self.discard_pile.canright == True:
            self.discard_pile.change_last_visible(increase = False)
            
    # end turn button makes the cpu play
        if self.gameend != True and self.blockEnd == False and 150 < mouseX < 300 and 735 < mouseY < 855:
            self.cpuPlays()

# the decision-making for the computer player                    
    def cpuPlays(self):       
        # local variables, resets computer turn states
         pickedUp = False    # computer has picked up cards from the active pile
         canPlay = False     # becomes true when there is a legal card the computer can play
         
         self.blockEnd = True        
         self.userPlayed = False   # resets player turn states
         
         
         if len(self.deck) == 0 and len(self.handTop) == 0:
    # plays the lowest legal card in covered table cards
            if len(self.tableT1) == 0:
                 for c in reversed(self.tableT2):
                     if self.tableT2.isLegal(c):
                         card = c
                         canPlay = True
                         break
                 if canPlay == True: 
                    self.tableT2.moveTo(card,self.active_pile)
                # checks for more of the same number
                    if len(self.tableT2) > 0:
                        for c in self.tableT2:
                            if c.number == card.number:
                                self.tableT2.moveTo(c,self.active_pile)
                    else:
                        self.gameend = True
                        self.won = "The computer has won!"
                 else:   # if no move is possible, picks up the active pile
                    self.active_pile.moveStack(self.handTop)
                    pickedUp = True                                        
            else:
    # plays the lowest legal card in uncovered table cards
                 for c in reversed(self.tableT1):
                     if self.tableT1.isLegal(c):
                         card = c
                         canPlay = True
                         break
                 if canPlay == True:
                    self.tableT1.moveTo(card,self.active_pile)
            # checks for more of the same number
                    if len(self.tableT1) > 0:
                        for c in self.tableT1:
                            if c.number == card.number:
                                self.tableT1.moveTo(c,self.active_pile)
                 else:   # if no move is possible, picks up the active pile
                    self.active_pile.moveStack(self.handTop)
                    pickedUp = True      
         else:
    # plays the lowest legal card in hand
            self.handTop.order()
            for c in reversed(self.handTop):
                if self.handTop.isLegal(c):
                    card = c
                    canPlay = True
                    break
            if canPlay == True:                
                self.handTop.playCard(card)
                if len(self.deck) > 0 and len(self.handTop)<3:
                    self.handTop.drawCard()
            # checks for more of the same number
                if len(self.handTop) > 0:
                    for c in self.handTop:
                        if c.number == card.number:
                            self.display()   # refreshes screen to show state between moves
                            time.sleep(0.5)
                            self.cpuPlays()
            else:   # if no move is possible, picks up the active pile
                self.active_pile.moveStack(self.handTop)
                pickedUp = True
        # checks if it can play instantly again
         if len(self.active_pile) > 0 and self.active_pile[0].number == 2:
            self.display()   # refreshes screen to show state between moves
            time.sleep(0.5)
            self.cpuPlays()
         if len(self.active_pile) > 0:    # checks for discarding active pile
            self.activeCount()
         if pickedUp == False and len(self.active_pile) == 0:
            self.display()   # refreshes screen to show state between moves
            time.sleep(0.5)
            self.cpuPlays()             # if it discarded, play again
         
# gameplay loop
    def gameplay(self):
        
        if len(self.active_pile) > 0:   # keeps track of the same type of cards in the active pile
            self.activeCount()          # if 4 similar cards are placed in a row, discards the pile 
        if len(self.tableB1) == 3:
            self.prepRound = False      # ends the preparation round
        # these two if statements will only happen during the first loop
            if self.cpuStarts == None:
                self.whoBegins()
            if self.cpuStarts == True:
                self.cpuPlays()
                self.cpuStarts = False
                
        if self.gameend != True and self.prepRound != True and len(self.deck) > 0 and len(self.handBottom) < 3:
            self.blockDeck = False
        else:
            self.blockDeck = True
    # checking player win
        if len(self.handBottom) == 0 and len(self.tableB2) == 0:
            self.gameend = True
            self.won = "The player has won!"
                
# this class serves as an object separate from the game
# it gets called to restart it when the 'new game' button is clicked
class Rebirth():
    def __init__(self):
        pass
    def commit(self):
        global game
        del game
        background(120,147,83)
        game = HiinaTurakas()
        game.startHands()
        
        
# initializing the game

game = HiinaTurakas()
game.startHands()

   
def setup():    
    size(1600,900)
    background(120,147,83)
    
def draw():
    textSize(20)
    fill(0,0,0)
    game.display()


def mouseClicked():
    game.click()
