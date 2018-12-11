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
    def __init__(self,number,suit,state="uncovered"): #, playability = False):
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

    def moveTo(self,card, target):
        card.uncover()
        target.insert(0,card)
        self.remove(card)
    
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
        stroke(120,147,83)
        fill (120,147,83)
        rect(self.x,self.y+170,25,-20)
        fill (255)
        text (len(self),self.x,self.y+170)

        # adds number of cards as text below it
            
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
        else:
#            stroke(120,147,83)
#            fill(120,147,83)
#            rect(self.x + 760,self.y,25,145)
#            rect(self.x - 35,self.y,25,145)
            pass
            
    
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
#            self.playability = True
            return True
        elif  game.active_pile[cnt].number == 7 and 7 >= card.value7:
#            self.playability = True
            return True
        elif game.active_pile[cnt].number == 8:
            return self.isLegal(card,cnt+1) 
        elif game.active_pile[cnt].number == 2:
#            self.playability = True
            return True
        elif (game.active_pile[cnt]).value <= card.value:
#            self.playability = True
            return True
        else:
#            self.playability = False
            return False    
   
   # used for hands and tablecards, cpu player finds what card in stack to play
    def playLowestLegal(self):
        canPlay = False
        if len(self) == 0:
            for c in reversed(self):
                if self.isLegal(c):
                    card = c
                    canPlay = True
                    break
            if canPlay == True:
                self.moveTo(card,self.active_pile)
                # checks for more of the same number
                for c in self:
                    if c.number == card.number:
                        self.moveTo(c,self.active_pile)
        # if there is no move possible, has to pick up active deck
            else:
                self.active_pile.moveStack(game.handTop)



class TableCards(Stack):
    def __init__(self,state = "uncovered"):
        Stack.__init__(self)
        self.state = state
        # self.state = "uncovered"
        
        
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
#        stroke(120,147,83)
#        fill(120,147,83)
#        rect(self.x-20,self.y,360,160)
        


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
#            for x in reversed(self):
            for x in self[self.last_visible:self.first_visible:-1]:
    
                if self.isLegal(x) == False:
                    self.whitecard = loadImage(path+"/greycard.png")
                    image(self.whitecard,self.x+cnt,self.y)
                cnt += 130
            while(cnt < 760):
#                stroke(120,147,83)
#                fill(120,147,83)
#                rect(self.x+cnt,self.y,100,145)
                cnt += 130
            if len(self)>5:
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
            else:
#                stroke(120,147,83)
#                fill(120,147,83)
#                rect(self.x + 760,self.y,25,145)
#                rect(self.x - 35,self.y,25,145)
                pass
        
        # rect(self.x-30,self.y+70,20,20)
        # rect(self.x+780,self.y+70,20,20)

                
    # moves a card to the active pile
    def playCard(self,card):
        self.moveTo(card,game.active_pile)
        if self.last_visible == len(self) and len(self)>5:
            self.change_last_visible(increase="False")

#        if len(self) < 6 or self.last_visible > 6:
#            self.change_last_visible(increase="False")
    

        
    def clicked(self,card):
        
        if self.isLegal(card):
            self.playCard(card)



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
        if len(self)>0:
            image(self.img,self.x,self.y,100,145)
#            fill(120,147,83)
#            rect(self.x,self.y+170,25,-20)
            fill (255)
            text (len(self),self.x,self.y+170)
        # adds number of cards as text below it
        else:
#            fill(120,147,83)
#            rect(self.x,self.y,100,145)
#            fill (120,147,83)
#            rect(self.x,self.y+170,20,-20)
            pass
    


class HiinaTurakas:
    def __init__(self):
#        self.players = ["Player 1", "Player 2"] #, "Player 3", "Player 4"]
        self.turn = 0
        self.active_pile = Stack(arrows=True)
        self.discard_pile = Stack(arrows=True)
        self.deck = Deck()
        random.shuffle(self.deck)
        self.Game_New = False
        self.instructions = False
        self.death = Rebirth()
#        self.handTop = Hand("covered")
        self.handTop = Hand() 
        self.handBottom = Hand()
        self.gameend = False
        
        self.tableB1 = TableCards()
        self.tableB2 = TableCards("covered")
        self.tableT1 = TableCards()
        self.tableT2 = TableCards("covered")
        
    def display(self):
        
        background(120,147,83)
        
        
        self.active_pile.display((1325)//2,(755)//2)
        self.deck.display(400,(755)//2)
        self.discard_pile.display(1000,(755)//2)
#        self.handTop.display(800-self.handTop.cnt//2,20)
#        self.handBottom.display((1600-self.handBottom.cnt)//2,735)
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
        
        fill (255)
        rect(150,735,150,120)
        fill (0)
        text ("End Turn", 170,795)
        
        if self.instructions == False:
            fill (255)
            rect(1300,60,200,500)
            fill (0)
            text ("Instructions", 1350,280)
        elif self.instructions == True:
            fill (255)
            rect(1300,60,200,500)
            fill (0)
            text ("Nothing", 1320,100)
            text ("in here",1320,120)
            text ("yet",1320,140)
            fill (0)
            rect(1420,510,70,30)
            fill (255)
            text("return",1425,530)
        
        if self.gameend != True:
            self.gameplay()
            
    def startHands(self):
        for count in range(6):
            self.handTop.drawCard()
            self.handBottom.drawCard()
        self.handBottom.order()
        for count in range(3):
            self.tableB1.drawCard()
            self.tableB2.drawCard()
            self.tableT1.drawCard()
            self.tableT2.drawCard()
        self.tableB1.order()
        self.tableB2.order()
   
# checks whether to discard the active pile
# discards when 10 is played or when there are 4 same numbers in a row         
    def activeCount(self):
        self.sequential = 0
        num = self.active_pile[0].number
        if len(self.active_pile)>=4:
            for cnt in range(4):
                if self.active_pile[cnt].number == num:
                    self.sequential += 1
        if self.sequential == 4 or num == 10:
            self.active_pile.moveStack(self.discard_pile)
#            stroke(120,147,83)
#            fill(120,147,83)
#            rect((1325)//2-35, (755)//2,270,146)
    
        
                                 
#    def addPlayer(num):
#        name = "Player "+ str(num)
#        if name not in self.players:
#            self.players.append(name)
#        self.players.sort()
    
#    def removePlayer(num):
#        name = "Player "+ str(num)
#        if name in self.players:
#            self.players.remove(name)
            
    def click(self):
        r = mouseX
        c = mouseY
        
        if  80 <= mouseX <=230 and 60 <= mouseY <=130:
            self.Game_New = True
        if 1300 <= mouseX <= 1500 and 60<= mouseY <= 560:
            self.instructions = True
        if 1420<= mouseX <= 1490 and 520 <= mouseY <= 540:
            self.instructions = False
            
    # finds whether a card in the hand was clicked
        if self.gameend != True:
            for card in self.handBottom[self.handBottom.last_visible:self.handBottom.first_visible:-1]:
                if card.x != None and card.y != None and card.x < mouseX < card.x+100 and card.y < mouseY < card.y+145:
                    self.handBottom.clicked(card)
        
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
        if self.gameend != True and len(self.deck) > 0 and 400 < mouseX < 500 and (755)//2 < mouseY < (755)//2 + 145:
            self.handBottom.drawCard() 
            self.handBottom.order()
            
    # clicking the active pile moves content to hand
        if self.gameend != True and self.active_pile.x <= mouseX < self.active_pile.x+200 and self.active_pile.y <= mouseY <= self.active_pile.y+100:
            self.active_pile.moveStack(self.handBottom)
            stroke(120,147,83)
#            fill(120,147,83)
#            rect(self.active_pile.x-35, self.active_pile.y,270,146)
            self.handBottom.order()
    
                           
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
            
#     discard pile's left button
        if self.discard_pile.x-35 <= mouseX < self.discard_pile.x and self.discard_pile.y <= mouseY <= self.discard_pile.y+100 and self.discard_pile.canleft == True:
            self.discard_pile.change_last_visible(increase = True)
#     discard pile's right button
        if self.discard_pile.x+200 < mouseX <= self.discard_pile.x+235 and self.discard_pile.y <= mouseY <= self.discard_pile.y+100 and self.discard_pile.canright == True:
            self.discard_pile.change_last_visible(increase = False)
            
    # end turn button makes the cpu play
        if self.gameend != True and 150 < mouseX < 300 and 735 < mouseY < 855:
            # TODO: add conditions
            self.cpuPlays()

                    
    def cpuPlays(self):
         pickedUp = False
         canPlay = False
         if len(self.deck) == 0 and len(self.handTop) == 0:
    # plays the lowest legal card in covered table cards
#            self.tableT1.playLowestLegal()
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
                        print "computer wins"
                        self.gameend = True
                 else:
                    self.active_pile.moveStack(self.handTop)
                    pickedUp = True                 

                       
            else:
    # plays the lowest legal card in uncovered table cards
 #           self.tableT2.playLowestLegal()
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
                 else:
                    self.active_pile.moveStack(self.handTop)
                    pickedUp = True      
         else:
    # plays the lowest legal card in hand
            self.handTop.order()
#            self.handTop.playLowestLegal()
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
                            self.cpuPlays()
            else:
                self.active_pile.moveStack(self.handTop)
                pickedUp = True
        # checks if it can play instantly again
         if len(self.active_pile) > 0 and self.active_pile[0].number == 2:
             self.cpuPlays()
         if len(self.active_pile) > 0:
            self.activeCount()
         if pickedUp == False and len(self.active_pile) == 0:
              self.cpuPlays()
         
# gameplay loop
    def gameplay(self):
        if len(self.active_pile) > 0:
            self.activeCount()
#    self.cpuPlays()       # enable this for making cpu algorithm unload all at once 
        
    # checking player win
        if len(self.handBottom) == 0 and len(self.tableB2) == 0:
            self.gameend = True
            print "player wins"  
                
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
        
# initializing

game = HiinaTurakas()
game.startHands()

   

    
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

    #game.handTop.display((size_x//2)-handTop.cnt//2,20)
    #game.handBottom.display((size_x-handBottom.cnt)//2,size_y-145-20)
    #game.active_pile.display((size_x-275)//2,(size_y-145)//2)
    #game.deck.display(size_x//4,(size_y-145)//2)
    #game.discard_pile.display((3*size_x)//4-200,(size_y-145)//2)



    game.display()


    
def mouseClicked():
    game.click()
