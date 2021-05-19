#########################################################################################################################################
##Project name: UnderPressureBeta1.1
##Author: Shantel Willams
##Date: 09/25/2018
##
## This is the last beta release of my game Under Pressure. This game was a project for my intro to game programming course.
## This is a text base game witH mouse click. It has multple choice answers and only 2 outcomes. I used the pygame Library
## and gimp for simple graphics and transitions. This was my first coding project. I decided to go in and use what I learned
## to clean up alot of the code. Thank you!
###########################################################################################################################################


## Importing Packages that will be used to help code ##
import time
import os, sys, pygame, random
from pygame.locals import *
import glob


################
#Set the Screen#
###############################################################################
## This is the set up for my game screen/window. I am initializing the window #
## And setting up the size, title, clock and frames.                          #
###############################################################################

os.environ['SDL_VIDEO_CENTERED'] = "1"
pygame.init()
SCR_WID, SCR_HEI = 900, 650
screen = pygame.display.set_mode((SCR_WID, SCR_HEI))
pygame.display.set_caption("Under Pressure")
pygame.font.init()
TEXTCOLOR = (255,255,255)
BLACK = (0,0,0)
clock = pygame.time.Clock()
FPS = 60


###########################
## Set up group containers#
############################################################################
## I chose to use groups for this project. Groups are good if you decides  #
## to ever add multiple instances of an object. I only used one of each    #
## but it is here just in case.                                            #
############################################################################

Players = pygame.sprite.Group(())
Captains = pygame.sprite.Group(())


##########################
##Set up Game Backgrounds#
################################################################################
##These are some of my game backgrounds. I loaded them using the pygame method #
##load. Later in the code I called each image in the appropriate function.     #  
################################################################################

background2 = pygame.image.load("space/spaceship_quarters_bg.jpg")
Captain = pygame.image.load("space/CaptainOffice.jpg")
AirLock = pygame.image.load("space/Airlock.jpg")
StrangerPic = pygame.image.load("Mysterious/Stranger.jpg")


#################
##Set up sounds.#
#####################################################################
# These are preloaded sounds that will be called later in the code. #
# The sound helps to add more personality and mood to my game.      #
#####################################################################

creepyPhone = pygame.mixer.Sound('Sounds/creepyPhone.wav')
Outage = pygame.mixer.Sound('Sounds/powerDown.wav')
LisaDrag=  pygame.mixer.Sound('Sounds/Lisadrag.wav')
SpaceDoor =  pygame.mixer.Sound('Sounds/spaceDoorClose.wav')
 
###############
#Set up fonts #
#####################################################
# Fonts used in my game.                            #
#####################################################

font2 = pygame.font.Font('Fonts/TH3 MACHINE.ttf', 70)
font = pygame.font.Font('Fonts/TH3 MACHINE.ttf', 36)
font3 = pygame.font.Font('Fonts/BodoniFLF-Bold.ttf', 24)
font4 = pygame.font.Font('Fonts/BodoniFLF-Bold.ttf', 12)

##########################################################
# Function called to terminate the game and program.     #
# Called in the waitForPlayerToPressKey Funtion.         #
##########################################################

def terminate():
    pygame.quit()

##################################################################
# This function waits to see if player quits or presses escape.  #
# If this happens the terminate function is called.              #
##################################################################

def waitForPlayerToPressKey():
    while True:
        clock.tick(120)
        for event in pygame.event.get():
            
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return
            
#########################################################################################################################################
# Function I created to write the frames for scenes to the window. I decided to create this function to make it reusable in my code.
#######################################################################################################################################

def listDir(dir,images,title,path):
    images = []
    title = []
    

    fileNames = os.listdir(dir)
    for fileName in os.listdir(dir):## get files in path
        images.append(fileName)## loads each file in list images as a list of strings
    for image in images:
        title.append(pygame.image.load(path + image))## sets the string[] as surface objects in list title
    for pics in title:
        screen.blit(pics,(0,0))# Display list on screen
        pygame.display.update()
        time.sleep(1)

        
###########################################################################################################################################
# This function creates and displays my Title Screen. The graphic are ran per frame. I created the frames using Gimp. It loads
# and plays audio and displays the Title text. It waits for player to hit key to start.
#######################################################################################################################################
            
def titleScreen():
    # Variables to loop loading frames
    images = []
    title = []
    path = "TScreen/"
    
    #Music for titleScreen 
    music = pygame.mixer.music.load ("Music/Surprised.wav") ## Loads
    pygame.mixer.music.play(1)## Plays
    
    #Background is blitting each frame for the intro
    folderPath = r"D:\\Past Classes\\UnderPressure\\Project 3\\TScreen"
    

    ## Loop function for loading images
    listDir(folderPath,images,title,path)
    
    ## title text
    drawText('UNDER PRESSURE', font2, screen, (SCR_WID / 6), (SCR_HEI / 3))
    drawText('Press any key to start.', font, screen, (SCR_WID / 4), (SCR_HEI / 2) + 100)
    pygame.display.update()
    waitForPlayerToPressKey() ##Wait til player presses any key


#######################################################################################################################################
# Funtion I used to draw text to screen. It takes the Text, Font, Screen Surface and Location.
#######################################################################################################################################
    
def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

##########################################################################################################################################
# This funtction is to display my intro text or background story.
#######################################################################################################################################
 
def displayIntro():
     x = SCR_WID / 12
     y = SCR_HEI / 8
     i = 0

     screen.blit(background2,(0,0))
     pygame.display.update()

    #Display each item in list on screen from txt file. I decided to do this incase I wanted to add more dialogue in the future.
     introTxt = open("Text/intro.txt", "r")
     intro = introTxt.readlines()
     for ilines in intro:
          drawText(intro[i] ,font3 , screen, x , y)
          y = y + 30
          i +=1
     drawText('Press Any Key', font3, screen, (SCR_WID / 4), (SCR_HEI / 2) + 100)
     pygame.display.update()
     waitForPlayerToPressKey()
     pygame.mixer.music.stop()
     introTxt.close()

########################################################################################################################################
## Created a class for all my Characters because they share the same members.
#######################################################################################################################################    


class Characters(pygame.sprite.Sprite):
    
    #Setting for the characters sprite Images.
    CaptainImage = pygame.image.load("Captain/SecurityOfficer.png")
    LisaImage = pygame.image.load("space/Lisa.png")
    
    
    def __init__(self,name,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        if self.name == "Captain": ## If objects is named Captain run these values else run the values below
            self.image = Characters.CaptainImage
            self.rect = self.CaptainImage.get_rect()
            self.image.set_colorkey(self.CaptainImage.get_at((0,0)))
        else:
            self.image = Characters.LisaImage
            self.rect = self.LisaImage.get_rect()
            self.image.set_colorkey(self.LisaImage.get_at((0,0)))
        self.rect.x = x
        self.rect.y = y

###########################################################################################################################
# Function to display the dialogue that takes play in the captains quaters. I used a loop to display each line and the    #
# corresponding object.                                                                                                   #
###########################################################################################################################


    def CaptainsScene(self):
        ##Sets the scene for the conversation between Lisa and the captain.
        x = SCR_WID / 10
        y = SCR_HEI / 6
        j = 0 ## Variable for Dialogue loop

        #Set up music for Captain Scene.
        music = pygame.mixer.music.load("Music/Convo2.wav")
        pygame.mixer.music.play(-1)


        ## Opening txt file and using a list to feed dialogue via a loop
        CaptainLines = open("Text/CaptainScene.txt", "r").readlines()
       
    
        for slines in CaptainLines:
            if(j %2) == 0:
                screen.blit(Captain,(0,0))
                pygame.draw.rect(screen,BLACK,[0,100,900,100],0)
                drawText(CaptainLines[j],font3 , screen, x , y)
                Players.draw(screen)## Displays lisa
                drawText('Press any key', font3, screen, (SCR_WID / 1.5), (SCR_HEI / 1.3) + 100)
                pygame.display.update()
                j +=1
                print(j);
            else:
                screen.blit(Captain,(0,0))
                pygame.draw.rect(screen,BLACK,[0,100,900,100],0)
                drawText(CaptainLines[j],font3 , screen, x , y)
                Captains.draw(screen)## Displays The Captain
                drawText('Press any key', font3, screen, (SCR_WID / 1.5), (SCR_HEI / 1.3) + 100)
                pygame.display.update()
                j += 1
                print(j);
            waitForPlayerToPressKey()

        
#########################################################################################################################################
# This function displays the video Call screen and audio
#######################################################################################################################################


def LisaPhone():

    ## variables
    x = SCR_WID / 12
    y = SCR_HEI / 8
    i = 2
    l = 0
    pathContact = "contact/"
    hallWayscenes = "hallWay/"

    ## Opening file to read lines for dialogue
    roomTxt = open("Text/roomScene.txt", "r")
    roomScene = roomTxt.readlines()

    # Variables to loop loading frames
    images = []
    title = []
    allWayImages = []
    hallWayscene = []
    
    #Finding the paths to images
    folderPath = r"D:\\Past Classes\\UnderPressure\\Project 3\\contact"
    dragfolderPath = r"D:\\Past Classes\\UnderPressure\\Project 3\\hallWay"

    ##power out image
    Powerout = pygame.image.load("Contact/Contact17.png")

    ## Drawing text to screen
    pygame.draw.rect(screen,BLACK,[0,50,900,100],0)
    drawText(roomScene[0] ,font3 , screen, x , y)
    drawText(roomScene[1] ,font3 , screen, x , y + 30)
    drawText('Press any key', font3, screen, (SCR_WID / 1.5), (SCR_HEI / 1.3) + 100)
    pygame.display.update()
    waitForPlayerToPressKey()
    pygame.display.update()

    ## Sound for the video call phone
    creepyPhone.set_volume(0.1)
    creepyPhone.play(-1,17300)

    ## Loop function for loading images
    listDir(folderPath,images,title,pathContact)
    
    pygame.mixer.music.stop()## Stops music currently playing
    Outage.play() ## Plays outage sound once

    ## Power outage scene
    while i <= 3:
        screen.blit(Powerout,(0,0))
        drawText(roomScene[i] ,font3 , screen, x , y)
        drawText('Press any key', font3, screen, (SCR_WID / 1.5), (SCR_HEI / 1.3) + 100)
        pygame.display.update()
        i = i + 1
        waitForPlayerToPressKey()
        
    ## Drag scene with array for frames and audio
    LisaDrag.play(1,10000)
    listDir(dragfolderPath,allWayImages, hallWayscene, hallWayscenes)
    SpaceDoor.play()
    time.sleep(2)


########################################################################################################################################
# This funtion Displays airlock dialogue. It Discribes the scene to the player 
#######################################################################################################################################

def Airlock():
    
    x = SCR_WID / 12
    y = SCR_HEI / 6
    i = 0
    
    ## Collect txt from file
    airLockTxt = open("Text/airLock.txt", "r").readlines()
   
    music = pygame.mixer.music.load ("Music/dragMusic2.wav")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.3)
    for lines in airLockTxt:
        screen.blit(AirLock,(0,0))
        drawText(airLockTxt[i] ,font3 , screen, x , y)
        drawText('Press any key', font3, screen, (SCR_WID / 1.5), (SCR_HEI / 1.3) + 100)
        pygame.display.update()
        waitForPlayerToPressKey()
        i += 1
    
        

#######################################################################################################################################
# The scene where you have dsicussion with a mysterious Stranger. Again I used frames and Text arrays to dsplay the graphics and
# text.
#######################################################################################################################################


def Stranger():
    
    x = 5
    y = SCR_HEI / 6
    i = 0

    ## Collect txt from file 
    StrangerTxt = open("Text/Stranger.txt", "r").readlines()
    for slines in StrangerTxt:
        screen.blit(StrangerPic,(0,0))
        pygame.draw.rect(screen,BLACK,[0,100,900,100],0)
        drawText(StrangerTxt[i] ,font3 , screen, x , y)
        drawText('Press any key', font3, screen, (SCR_WID / 1.5), (SCR_HEI / 1.3) + 100)
        waitForPlayerToPressKey()
        pygame.display.update()
        i += 1
        
########################################################################################################################################
# This funtion  also Displays the Dialogue between you and the Stranger. It displays the questions and draws the answer to a rectangle
# where the players choices are recognized.
#######################################################################################################################################


def Questions1(wrongAnswer):
    x = 5
    y = SCR_HEI / 6
    i = 1
    location = 100
    
    screen.blit(StrangerPic,(0,0))
    drawText("Question number 1, Why did you want this job?",font3, screen, x, y)
    drawText("Click on a answer.",font4, screen, x, y + 50)
    
    #render text on rect to check for mouse collision.
    Answer = font3.render("A.) I was bored on earth.", 1, TEXTCOLOR,(0,0,0))
    rect = Answer.get_rect()
    rect.topleft = (x, y + 100)

    Answer2 = font3.render("B.) Seemed like a grand opportunity to explore.", 1, TEXTCOLOR,(0,0,0))
    rect2 = Answer2.get_rect()
    rect2.topleft = (x, y + 150)

    Answer3 = font3.render("C.) I enjoy cooking and plus the view is nice.", 1, TEXTCOLOR,(0,0,0))
    rect3 = Answer3.get_rect()
    rect3.topleft = (x, y + 200)

    screen.blit(Answer,rect)
    screen.blit(Answer2,rect2)
    screen.blit(Answer3,rect3)
    pygame.display.update()

   
    while i == 1 :
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                 pos = pygame.mouse.get_pos()
                 
                 if rect.collidepoint(pos):
                    print("down")
                    screen.blit(StrangerPic,(0,0))
                    drawText("Because you were bored? Wrong answer!",font3, screen, x, y)
                    wrongAnswer = wrongAnswer + 1
                    i = i + 1
                    print(wrongAnswer)
                         
                 elif rect2.collidepoint(pos):
                    screen.blit(StrangerPic,(0,0))
                    print("right answer")
                    drawText("Oh so your an explorer huh? I like that!",font3, screen, x, y)
                    i = i + 1
                    
                 elif rect3.collidepoint(pos):
                    screen.blit(StrangerPic,(0,0))
                    print("right answer")
                    drawText("I hear your quite the chef. Who wouldn't like this view?",font3, screen, x, y)
                    i = i + 1
                   
    pygame.display.update()
    time.sleep(3)
    Questions2(wrongAnswer)
                        
                    
def Questions2(wrongAnswer):
    x = 5
    y = SCR_HEI / 6
    i = 1
    
    print("------" + str(wrongAnswer))
    screen.blit(StrangerPic,(0,0))
    drawText("Question number 2. What is your best quality?",font3, screen, x, y)
    drawText("Click on a answer.",font4, screen, x, y + 50)
    
    #render text on rect to check for mouse collision.
    Answer = font3.render("A.) Teamwork.", 1, TEXTCOLOR,(0,0,0))
    rect = Answer.get_rect()
    rect.topleft = (x, y + 100)

    Answer2 = font3.render("B.) Courage.", 1, TEXTCOLOR,(0,0,0))
    rect2 = Answer2.get_rect()
    rect2.topleft = (x, y + 150)

    Answer3 = font3.render("C.) Patience.", 1, TEXTCOLOR,(0,0,0))
    rect3 = Answer3.get_rect()
    rect3.topleft = (x, y + 200)

    Answer4 = font3.render("D.) what kind of bull crap is this?", 1, TEXTCOLOR,(0,0,0))
    rect4 = Answer4.get_rect()
    rect4.topleft = (x, y + 250)

    screen.blit(Answer,rect)
    screen.blit(Answer2,rect2)
    screen.blit(Answer3,rect3)
    screen.blit(Answer4,rect4)
    pygame.display.update()

    while i == 1:
        for event in pygame.event.get():
             if event.type == QUIT:
                terminate()
             if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                    
             if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                 pos = pygame.mouse.get_pos()
                 if rect.collidepoint(pos):
                    print("right answer")
                    screen.blit(StrangerPic,(0,0))
                    drawText("We are working as a team to downsize the crew.",font3, screen, x, y)
                    i = i +1
                    
                 elif rect2.collidepoint(pos):
                    screen.blit(StrangerPic,(0,0))
                    print("right answer")
                    drawText("Courage you say? Yea how many people volunteer to come outer space?",font3, screen, x, y)
                    i = i +1
                    
                 elif rect3.collidepoint(pos):
                    screen.blit(StrangerPic,(0,0))
                    print("right answer")
                    drawText("Patience! You need patience with these spoiled residents on freedom-858",font3, screen, x, y)
                    i = i + 1

                 elif rect4.collidepoint(pos):
                    print("down")
                    screen.blit(StrangerPic,(0,0))
                    drawText("You are really testing my patience!",font3, screen, x, y)
                    wrongAnswer = wrongAnswer + 1
                    i = i +1
                    print(wrongAnswer)

    pygame.display.update()
    time.sleep(3)
    Questions3(wrongAnswer)

def Questions3(wrongAnswer):
    x = 5
    y = SCR_HEI / 6
    i = 1
    print("------" + str(wrongAnswer))
    screen.blit(StrangerPic,(0,0))
    drawText("Question number 3. Do you enjoy your job?",font3, screen, x, y)
    drawText("Click on a answer.",font4, screen, x, y + 50)
    
    #render text on rect to check for mouse collision.
    Answer = font3.render("A.) Yes! I enjoy my job.", 1, TEXTCOLOR,(0,0,0))
    rect = Answer.get_rect()
    rect.topleft = (x, y + 100)

    Answer2 = font3.render("B.) Just something to do.", 1, TEXTCOLOR,(0,0,0))
    rect2 = Answer2.get_rect()
    rect2.topleft = (x, y + 150)

    Answer3 = font3.render("C.) Whats it to you?", 1, TEXTCOLOR,(0,0,0))
    rect3 = Answer3.get_rect()
    rect3.topleft = (x, y + 200)

    screen.blit(Answer,rect)
    screen.blit(Answer2,rect2)
    screen.blit(Answer3,rect3)
    pygame.display.update()

    while i == 1:
        for event in pygame.event.get():
             if event.type == QUIT:
                terminate()
             if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
             if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                 pos = pygame.mouse.get_pos()
                 if rect.collidepoint(pos):
                    print("right answer")
                    screen.blit(StrangerPic,(0,0))
                    drawText("Glad you like it here! Let's see if you will continue to work.",font3, screen, x, y)
                    i = i +1
                    
                 elif rect2.collidepoint(pos):
                    screen.blit(StrangerPic,(0,0))
                    print("right answer")
                    drawText("Just something to do huh ?",font3, screen, x, y)
                    i = i +1 
                    
                 elif rect3.collidepoint(pos):
                    screen.blit(StrangerPic,(0,0))
                    print("down")
                    drawText("You still think this is a joke!",font3, screen, x, y)
                    i = i +1
                    wrongAnswer = wrongAnswer + 1
                    print(wrongAnswer)

    pygame.display.update()
    time.sleep(3)
    Questions4(wrongAnswer)

def Questions4(wrongAnswer):
    x = 5
    y = SCR_HEI / 6
    i = 1
    print("------" + str(wrongAnswer))
    screen.blit(StrangerPic,(0,0))
    drawText("Question number 4. Would you sacrifice yourself for your crew?",font3, screen, x, y)
    drawText("Click on a answer.",font4, screen, x, y + 50)
    
    #render text on rect to check for mouse collision.
    Answer = font3.render("A.) NO.", 1, TEXTCOLOR,(0,0,0))
    rect = Answer.get_rect()
    rect.topleft = (x, y + 100)

    Answer2 = font3.render("B.) YES.", 1, TEXTCOLOR,(0,0,0))
    rect2 = Answer2.get_rect()
    rect2.topleft = (x, y + 150)


    screen.blit(Answer,rect)
    screen.blit(Answer2,rect2)
    pygame.display.update()

    while i == 1:
        for event in pygame.event.get():
             if event.type == QUIT:
                terminate()
             if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
             if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                 pos = pygame.mouse.get_pos()
                 if rect.collidepoint(pos):
                    print("right answer")
                    screen.blit(StrangerPic,(0,0))
                    drawText("Well Someone has to Go!",font3, screen, x, y)
                    i = i + 1
                    
                    
                 elif rect2.collidepoint(pos):
                    screen.blit(StrangerPic,(0,0))
                    print("down")
                    drawText("Good because we need you now!",font3, screen, x, y)
                    wrongAnswer = wrongAnswer + 1
                    i = i + 1
                    print(wrongAnswer)

    pygame.display.update()
    time.sleep(3)
    
    if wrongAnswer < 4:
          Questions5(wrongAnswer)
    else:
          badEnd()


def Questions5(wrongAnswer):
    x = 5
    y = SCR_HEI / 6
    i = 1
    print("------" + str(wrongAnswer))
    screen.blit(StrangerPic,(0,0))
    drawText("Question number 5. Have you told anyone about the shortage of supplies?",font3, screen, x, y)
    drawText("Click on a answer.",font4, screen, x, y + 50)
    
    #render text on rect to check for mouse collision.
    Answer = font3.render("A.) NO.", 1, TEXTCOLOR,(0,0,0))
    rect = Answer.get_rect()
    rect.topleft = (x, y + 100)

    Answer2 = font3.render("B.) Yes.", 1, TEXTCOLOR,(0,0,0))
    rect2 = Answer2.get_rect()
    rect2.topleft = (x, y + 150)

    Answer3 = font3.render("C.) Whats shortage?", 1, TEXTCOLOR,(0,0,0))
    rect3 = Answer3.get_rect()
    rect3.topleft = (x, y + 200)

    screen.blit(Answer,rect)
    screen.blit(Answer2,rect2)
    screen.blit(Answer3,rect3)
    pygame.display.update()

    while i == 1:
        for event in pygame.event.get():
             if event.type == QUIT:
                terminate()
             if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
             if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                 pos = pygame.mouse.get_pos()
                 if rect.collidepoint(pos):
                    print("right answer")
                    screen.blit(StrangerPic,(0,0))
                    drawText("Good! Then you will keep your mouth shut.",font3, screen, x, y)
                    i = i + 1
                    
                 elif rect2.collidepoint(pos):
                    screen.blit(StrangerPic,(0,0))
                    print("down")
                    drawText("Not the right answer!",font3, screen, x, y)
                    wrongAnswer = wrongAnswer + 1
                    print(wrongAnswer)
                    i = i + 1
                    
                 elif rect3.collidepoint(pos):
                    screen.blit(StrangerPic,(0,0))
                    print("right answer")
                    drawText("Nice!",font3, screen, x, y)
                    i = i + 1
                    
    pygame.display.update()
    time.sleep(3)
    
    if wrongAnswer < 4:
          Questions6(wrongAnswer)
    else:
          badEnd()

    

def Questions6(wrongAnswer):
    x = 5
    y = SCR_HEI / 6
    i = 1
    print("------" + str(wrongAnswer))
    screen.blit(StrangerPic,(0,0))
    drawText("Question number 6. What are your strengths?",font3, screen, x, y)
    drawText("Click on a answer.",font4, screen, x, y + 50)
    
    #render text on rect to check for mouse collision.
    Answer = font3.render("A.) I will demonstrate once Im out!", 1, TEXTCOLOR,(0,0,0))
    rect = Answer.get_rect()
    rect.topleft = (x, y + 100)

    Answer2 = font3.render("B.)I can adjust to any changes.", 1, TEXTCOLOR,(0,0,0))
    rect2 = Answer2.get_rect()
    rect2.topleft = (x, y + 150)

    Answer3 = font3.render("C.)I can make a great pizza!", 1, TEXTCOLOR,(0,0,0))
    rect3 = Answer3.get_rect()
    rect3.topleft = (x, y + 200)

    screen.blit(Answer,rect)
    screen.blit(Answer2,rect2)
    screen.blit(Answer3,rect3)
    pygame.display.update()

    while i == 1:
        for event in pygame.event.get():
             if event.type == QUIT:
                terminate()
             if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
             if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                 pos = pygame.mouse.get_pos()
                 if rect.collidepoint(pos):
                    print("down")
                    screen.blit(StrangerPic,(0,0))
                    drawText("Sadly its me with all the power.",font3, screen, x, y)
                    wrongAnswer = wrongAnswer + 1
                    print(wrongAnswer)
                    i = i + 1
                
                 elif rect2.collidepoint(pos):
                    screen.blit(StrangerPic,(0,0))
                    print("right answer")
                    drawText("yup alot of adjusting going on.",font3, screen, x, y)
                    i = 1 + 1
                    
                    
                 elif rect3.collidepoint(pos):
                    screen.blit(StrangerPic,(0,0))
                    print("right answer")
                    drawText("pizza! I am dying for some.",font3, screen, x, y)
                    i = i + 1
                    
    pygame.display.update()
    time.sleep(3)
    if wrongAnswer < 4:
          Questions7(wrongAnswer)
    else:
          badEnd()


def Questions7(wrongAnswer):
    x = 5
    y = SCR_HEI / 6
    i = 1
    print("------" + str(wrongAnswer))
    screen.blit(StrangerPic,(0,0))
    drawText("Question number 7. which do you prefer? Planet earth or Freedom-858?",font3, screen, x, y)
    drawText("Click on a answer.",font4, screen, x, y + 50)
    
    #render text on rect to check for mouse collision.
    Answer = font3.render("A.)Planet earth. I just love nature.", 1, TEXTCOLOR,(0,0,0))
    rect = Answer.get_rect()
    rect.topleft = (x, y + 100)

    Answer2 = font3.render("B.)I am a space Cowgirl!", 1, TEXTCOLOR,(0,0,0))
    rect2 = Answer2.get_rect()
    rect2.topleft = (x, y + 150)


    screen.blit(Answer,rect)
    screen.blit(Answer2,rect2)
    pygame.display.update()

    while i == 1:
        for event in pygame.event.get():
             if event.type == QUIT:
                terminate()
             if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
             if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                 pos = pygame.mouse.get_pos()
                 if rect.collidepoint(pos):
                    print("down")
                    screen.blit(StrangerPic,(0,0))
                    drawText("To bad we can't ship you back.",font3, screen, x, y)
                    wrongAnswer = wrongAnswer + 1
                    i = i + 1
                    print(wrongAnswer)
                    
                    
                 elif rect2.collidepoint(pos):
                    screen.blit(StrangerPic,(0,0))
                    print("right answer")
                    drawText("giddy up Cowgirl!",font3, screen, x, y)
                    i = i + 1

    pygame.display.update()
    time.sleep(3)
    if wrongAnswer < 4:
          Questions8(wrongAnswer)
    else:
          badEnd()

def Questions8(wrongAnswer):
    x = 5
    y = SCR_HEI / 6
    i = 1
    print("------" + str(wrongAnswer))
    screen.blit(StrangerPic,(0,0))
    drawText("Question number 8. Do you have loved ones on Earth?",font3, screen, x, y)
    drawText("Click on a answer.",font4, screen, x, y + 50)
    
    #render text on rect to check for mouse collision.
    Answer = font3.render(" A.) Yes! My parents. Have you heard from earth?", 1, TEXTCOLOR,(0,0,0))
    rect = Answer.get_rect()
    rect.topleft = (x, y + 100)

    Answer2 = font3.render("B.) Not anyone I care about.", 1, TEXTCOLOR,(0,0,0))
    rect2 = Answer2.get_rect()
    rect2.topleft = (x, y + 150)


    screen.blit(Answer,rect)
    screen.blit(Answer2,rect2)
    pygame.display.update()

    while i == 1:
        for event in pygame.event.get():
             if event.type == QUIT:
                terminate()
             if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
             if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                 pos = pygame.mouse.get_pos()
                 if rect.collidepoint(pos):
                    print("right answer")
                    screen.blit(StrangerPic,(0,0))
                    drawText("We have not had contact from earth in a week.",font3, screen, x, y)
                    i = i + 1
                    
                 elif rect2.collidepoint(pos):
                    screen.blit(StrangerPic,(0,0))
                    print("down")
                    drawText("But your file states otherwise.",font3, screen, x, y)
                    i = i + 1
                    wrongAnswer = wrongAnswer + 1
                    print(wrongAnswer)

    pygame.display.update()
    time.sleep(3)
    if wrongAnswer < 4:
          Questions9(wrongAnswer)
    else:
          badEnd()

def Questions9(wrongAnswer):
    x = 5
    y = SCR_HEI / 6
    i = 1
    print("------" + str(wrongAnswer))
    screen.blit(StrangerPic,(0,0))
    drawText("Question number 9. Do you know why supplies are low?",font3, screen, x, y)
    drawText("Click on a answer.",font4, screen, x, y + 50)
    
    #render text on rect to check for mouse collision.
    Answer = font3.render("A.) Yea, You probably took them for yourself.", 1, TEXTCOLOR,(0,0,0))
    rect = Answer.get_rect()
    rect.topleft = (x, y + 100)

    Answer2 = font3.render("B.) Because of  the lack of communication with Earth.", 1, TEXTCOLOR,(0,0,0))
    rect2 = Answer2.get_rect()
    rect2.topleft = (x, y + 150)

    Answer3 = font3.render("C.) How would I know? ", 1, TEXTCOLOR,(0,0,0))
    rect3 = Answer3.get_rect()
    rect3.topleft = (x, y + 200)

    screen.blit(Answer,rect)
    screen.blit(Answer2,rect2)
    screen.blit(Answer3,rect3)
    pygame.display.update()

    while i == 1:
        for event in pygame.event.get():
             if event.type == QUIT:
                terminate()
             if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
             if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                 pos = pygame.mouse.get_pos()
                 if rect.collidepoint(pos):
                    print("down")
                    screen.blit(StrangerPic,(0,0))
                    drawText("Haha That smart mouth will get you no where.",font3, screen, x, y)
                    i = i + 1
                    wrongAnswer = wrongAnswer + 1
                    print(wrongAnswer)
                    
                 elif rect2.collidepoint(pos):
                    screen.blit(StrangerPic,(0,0))
                    print("right answer")
                    drawText("yup we have requested multiple shipments with no answer.",font3, screen, x, y)
                    i = i + 1
                    
                    
                 elif rect3.collidepoint(pos):
                    screen.blit(StrangerPic,(0,0))
                    print("right answer")
                    drawText("No communication. No shipments.",font3, screen, x, y)
                    i = i + 1
                    
    pygame.display.update()
    time.sleep(3)
    if wrongAnswer < 4:
          Questions10(wrongAnswer)
    else:
          badEnd()


def Questions10(wrongAnswer):
    x = 5
    y = SCR_HEI / 6
    i = 1
    print("------" + str(wrongAnswer))
    screen.blit(StrangerPic,(0,0))
    drawText("Question number 10. You made it! Can we save everyone?",font3, screen, x, y)
    drawText("Click on a answer.",font4, screen, x, y + 50)
    
    #render text on rect to check for mouse collision.
    Answer = font3.render("A.) Yes, If we just work together. I am sure there is another solution.", 1, TEXTCOLOR,(0,0,0))
    rect = Answer.get_rect()
    rect.topleft = (x, y + 100)

    Answer2 = font3.render("B.)  No, just let me out!", 1, TEXTCOLOR,(0,0,0))
    rect2 = Answer2.get_rect()
    rect2.topleft = (x, y + 150)

    Answer3 = font3.render("C.) I sure hope so.", 1, TEXTCOLOR,(0,0,0))
    rect3 = Answer3.get_rect()
    rect3.topleft = (x, y + 200)

    screen.blit(Answer,rect)
    screen.blit(Answer2,rect2)
    screen.blit(Answer3,rect3)
    pygame.display.update()

    while i == 1:
        for event in pygame.event.get():
             if event.type == QUIT:
                terminate()
             if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
             if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                 pos = pygame.mouse.get_pos()
                 if rect.collidepoint(pos):
                    print("down")
                    screen.blit(StrangerPic,(0,0))
                    drawText("We have thought of different solutions.",font3, screen, x, y)
                    i = i + 1
                    
                 elif rect2.collidepoint(pos):
                    screen.blit(StrangerPic,(0,0))
                    print("right answer")
                    drawText("Sure! you didnt say which door.",font3, screen, x, y)
                    i = i + 1
                    wrongAnswer = wrongAnswer + 1
                    print(wrongAnswer)
                    
                    
                 elif rect3.collidepoint(pos):
                    screen.blit(StrangerPic,(0,0))
                    print("right answer")
                    drawText("Good to see you have not lost hope in there.",font3, screen, x, y)
                    i = i + 1
                    

    pygame.display.update()
    time.sleep(3)
    if wrongAnswer < 4:
          goodEnd()
    else:
          badEnd()


#######################################################################################################################################
# This is the good Ending for my text game.
#######################################################################################################################################

def goodEnd():
    x = 5
    y = SCR_HEI / 6

    lines = ["Congrats Lisa! You made it through.","Some of your other co-workers were not so lucky.","We will be watching you! Speak of this to no one."]

    for slines in lines:
        screen.blit(StrangerPic,(0,0))
        pygame.draw.rect(screen,BLACK,[0,100,900,100],0)
        drawText(slines ,font3 , screen, x , y)
        pygame.display.update()
        time.sleep(3)


#######################################################################################################################################
# This is the Bad ending for my game.
#######################################################################################################################################

def badEnd():
    x = 5
    y = SCR_HEI / 6

    screen.blit(StrangerPic,(0,0))
    pygame.draw.rect(screen,BLACK,[0,100,900,100],0)
    drawText("Sorry Lisa! We are no longer interested in your employment here." ,font3 , screen, x , y)
    pygame.display.update()
    time.sleep(3)

#########################################  Main Function, Where I put it all togther###################################################
def main():
     wrongAnswer = 0 ## sets player wrong answers to zero
     Lisa = Characters("Lisa",400,50) ## Creating lisa Which is an object of Character
     captainTalk = Characters("Captain",10,150) ## Creating captainTalk Which is an object of Character
     Players.add(Lisa) ## Adding object to group
     Captains.add(captainTalk)## adding object to group
     

    ## Make the game loop
     while True:
                #process to check if user quits anytime during game
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print ("Game exited by user")
                        pygame.quit()
                        
            
                    ## Calling each function needed to complete the game.
                    titleScreen()
                    displayIntro()
                    captainTalk.CaptainsScene()
                    LisaPhone()
                    Airlock()
                    Stranger()
                    Questions1(wrongAnswer)
                    pygame.display.flip()
                    

main()
