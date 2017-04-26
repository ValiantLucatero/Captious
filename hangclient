from socket import*
import threading
import time , sys
from tkinter import*
from tkinter import messagebox

global name         #-name of the thread being used
global quit         #-keeps track of the quit variable, set to true once a player decides to quit the game
global actualwrd    #-keeps track of the word currently set
global word_set     #-keeps track if the a word is currently set (True or False)
global used_bar     #-keeps track of the bar where the used letters go (deletes the words once set to False)
global counter      #-keeps track of the current tries in the game until game is over.

##--------------------------------------------------------------------------------
# Initialization of global variables
##--------------------------------------------------------------------------------

counter = 0
word_set = 'False'
used_bar = 'False'
actualwrd = '*'
name = ''
quit = False

servername = '127.0.0.1'
port = 0
serverport = 12000

##--------------------------------------------------------------------------------
##---FUNCTION DECLARATIONS---

#---------------------------------------------------------------------------------
# This function will handle the receiving of messages from the server.
# Will also display them in the current running window.
# This function is threaded and will recv the name of the window to display on (chat)
# a socket (sock) and a blank parameter (name).
# It decodes the commands recvd from the server and execs accordingly.
#---------------------------------------------------------------------------------
def recieveMsg( name , sock , chat ):

    print("started")

    global quit , block , word_set , usedletter

    text = Text(chat , width = 50 , height = 20 , yscrollcommand = s.set )
    s.config( command = text.yview)
    text.pack(side = LEFT)

    while quit == False:

        try:
            msg , addr = sock.recvfrom( 1024 )
            message = msg.decode()
            tokens = message.split()
            #print(message + " FROM SERVER") #this is to track the msgs from the server

        except ConnectionResetError:

            print("thread sorry")

            message = messagebox.showerror("Connection Error!" , "No connection ws made...")
            break

        if tokens[0] == 'CNTR' :

            counter = tokens[1]

            if counter == '6':
                canvas.delete("all")
                canvas.create_image(175,125, image = img1 )  
                          
            if counter == '5':
                canvas.create_image(175,125, image = img2 )

            if counter == '4':
                canvas.create_image(175,125, image = img3 )

            if counter == '3':
                canvas.create_image(175,125, image = img4 )

            if counter == '2':
                canvas.create_image(175,125, image = img5 )

            if counter == '1':
                canvas.create_image(175,125, image = img6 )

            if counter == '0':
                canvas.create_image(175,125, image = img7 )

            if counter == 'W':
                canvas.create_image(175,125, image = img8 )

        elif  tokens[0] == 'SETWRD':

            #print("I ENTERED SETWORD") #-trace statement
            block.delete(1.0 , 'end')
            block.insert(INSERT , tokens[1])

        elif  tokens[0] == 'SETWRD2':

            check_set(tokens[2])

            #print("I ENTERED SETWORD2") #-trace statement

            block.delete(1.0 , 'end')
            block.insert(INSERT , tokens[1])

        elif tokens[0] == 'UPDATEWRD':
            
            check_set(tokens[2])

            #print("I ENTERED UDPATE") #-trace statement
            actualwrd = tokens[1]

        elif tokens[0] == 'RLET':

            global used_bar
            
            if(used_bar == 'False'):
                
                usedletter.delete(1.0 , 'end')
                used_bar = 'True'

            #print("I ENTERED RLET") #-trace statement
            letter = tokens[1].upper()
            usedletter.insert(INSERT , letter )


        elif message != "QUITCOMM":

            #This will print out aything else to the chat screen
            text.insert(INSERT , message)
            text.see(END)

        else:
            quit = True

    print("I am done wih thread")

#---------------------------------------------------------------------------------
# This is the function that will be executed whe the button 'Enter' is pressed once the username is entered.
# It connects the client to the game server.
#---------------------------------------------------------------------------------
def submit():

    global name

    userName = user.get()
    name = userName
    
    if len(userName) > 0:  
        try:

            clientsock.sendto( userName.encode() , (servername , serverport) )

        except ConnectionResetError:

           print("sorry")
       
        root.destroy()
        menu_w.destroy()

    else:

        disp_name_error()

#---------------------------------------------------------------------------------
# This is the function that will be executed whe the 'Enter' key is pressed once the username is entered.
# It connects the client to the game server.
#---------------------------------------------------------------------------------
def submitenter(event):

    global name
    userName = user.get()
    name = userName
    
    if len(userName) > 0:  

        try:

            clientsock.sendto( userName.encode() , (servername , serverport) )

        except ConnectionResetError:
           print("sorry")

        root.destroy()
        menu_w.destroy()
    else:

        disp_name_error()

#---------------------------------------------------------------------------------
# This function will send the messages written in the chat window once the button
# 'send' is pressed.
# These messages will be the ones sent to other players.
# Messages are sent in the from [player]: 'message' 
# If nothing is inputed in the entry bar, nothing is sent.
#---------------------------------------------------------------------------------
def chatsend():
    
    global name 

    message = msg.get()

    tokens = message.split()

    if len(message) > 0: 

        line = "[" + name + "]: " + message + "\n"
        clientsock.sendto( line.encode() , (servername , serverport) )
        msg.delete(0 , 'end')

#---------------------------------------------------------------------------------
# This function will send the messages written in the chat window once the 'enter'
# key is pressed.
# These messages will be the ones sent to other players.
# Messages are sent in the from [player]: 'message' 
# If nothing is inputed in the entry bar, nothing is sent.
#---------------------------------------------------------------------------------
def enter(event):

    global name 

    message = msg.get()

    tokens = message.split()

    if len(message) > 0: 

        line = "[" + name + "]: " + message + "\n"
        clientsock.sendto( line.encode() , (servername , serverport) )
        msg.delete(0 , 'end')

#---------------------------------------------------------------------------------
# This funtion will pop a window displaying an error when nothing was entered as
# input in the entry bar from the username screen.
#---------------------------------------------------------------------------------
def disp_name_error():

    message = messagebox.showerror("No name!" , "Please enter a user name\n")

#---------------------------------------------------------------------------------
# This funtion, once a player decided to quit the game, send a code to the server
# in the form of '[player]: ^q'
# The code '^q' is the one read and executed from the server 
#---------------------------------------------------------------------------------
def quitchat():

    line = "[" + name + "]: ^q \n"
    clientsock.sendto( line.encode() , (servername , serverport) )
    chat.destroy()

#---------------------------------------------------------------------------------
# This function pops a window up prompting the user to input a word to set
# in the game. 
#---------------------------------------------------------------------------------
def set_word():

    global wordwindow 
    global input

    wordwindow = Tk()

    wordwindow.title("Choose a difficult word!")
    wordwindow.minsize(width = 200, height =50)


    wordlabel = Label( wordwindow, text = "Enter your word: ")
    wordlabel.pack(side = LEFT)

    input = Entry( wordwindow )
    input.pack(side = LEFT)

    button = Button( wordwindow , text = "Set", width = 20 , command = wordsend )
    button.pack(side = LEFT)

    wordwindow.mainloop()

#---------------------------------------------------------------------------------
# This function is executed once the 'Set' button from the 'wordwindow' window referenced
# above. It sends the command to set the word in the form on '[player]: SETWRD word'
# Here, the indicator 'word_set' is modified. If 'word_set' is false (word not set)
# then procede, otherwise display an error message saying so.
#---------------------------------------------------------------------------------
def wordsend():

    global block , word_set

    word = input.get()
    tokens = word.split()
    
    if (len(tokens[0]) > 0):

        if word_set == 'False':  
                  
            print( "button entered" )
            block.delete(1.0 , 'end')
            block.insert(INSERT , tokens[0])
            command = "[" + name + "]: SETWRD " + tokens[0] 
            clientsock.sendto( command.encode() , (servername , serverport))

        else:

            message = messagebox.showerror("Word set!!" , "Not your turn to set a word, please wait!")

        wordwindow.destroy()

#---------------------------------------------------------------------------------
# This function pops a window up prompting the user to input a word to guess
# the word in the game. 
#---------------------------------------------------------------------------------

def guess_word():

    global guess 
    global guessinput

    guess = Tk()
    guess.title("Give it a try...")

    guesslabel = Label(guess , text = "Guess: " ).pack(side = LEFT)
    guessinput = Entry( guess )
    guessinput.pack( side = LEFT)
    guessb = Button(guess , text = "Good Luck!" , command = send_guess).pack(side = LEFT)
   
    guess.mainloop()

#---------------------------------------------------------------------------------
# This function is executed once the 'Good Luck' button from the 'guess' window referenced
# above. It sends the command to set the word in the form on '[player]: GUESSWRD word'
#---------------------------------------------------------------------------------
def send_guess():
    
    gword = guessinput.get()
    tokens = gword.split()
    
    if( len(tokens[0]) > 0 ):

        command = "[" + name + "]: GUESSWRD " + tokens[0] 
        clientsock.sendto( command.encode() , (servername , serverport) )
        guess.destroy()

#---------------------------------------------------------------------------------
# This function pops a window up prompting the user to input a letter to guess
# that could be in the word that is currently set. 
#---------------------------------------------------------------------------------
def guess_letter():

    global letter 
    global letterinput

    letter = Tk()
    letter.title("Give me a letter...")

    letterlabel = Label(letter , text = "letter: " ).pack(side = LEFT)
    letterinput = Entry( letter , width = 20 )
    letterinput.pack( side = LEFT)
    letterb = Button(letter , text = "Good Luck!" , command = send_letter).pack(side = LEFT)
   
    letter.mainloop()

#---------------------------------------------------------------------------------
# This function is executed once the 'Letter' button from the 'letter' window referenced
# above. It sends the command to set the word in the form on '[player]: RLET letter'
# Prior to sending the command, this also checks that the input is only one character
# to avoid errors in the server or the game.
# Currently does not check if input is an alphabetical character.
#---------------------------------------------------------------------------------
def send_letter():
    
    gletter = letterinput.get()
    tokens = gletter.split()
    
    if( len(tokens[0]) == 1 ):

        command = "[" + name + "]: RLET " + tokens[0] 
        clientsock.sendto( command.encode() , (servername , serverport) )
        letterinput.delete(0 , 'end')

#---------------------------------------------------------------------------------
# This function is in charge of cheching an setting the indicators for a word
# being set in the game and if the bar of used letters is to be cleared or not
#---------------------------------------------------------------------------------
def check_set( word ):

    global word_set
    global used_bar

    word_set =  word

    if (word == 'False'):
        used_bar = 'False'

def randomwrd():


        if word_set == 'False':  

            command = "[" + name + "]: RANDOMWRD" 
            clientsock.sendto( command.encode() , (servername , serverport) )                  

        else:

            message = messagebox.showerror("Word set!!" , "Not your turn to set a word, please wait!")

def connect():
    # //this is for the welcome window. It prompts the user for a 'name'
    global root , user

    root = Tk()

    root.title("Welcome!")
    root.maxsize(width = 270 , height = 48)
    root.geometry("270x48+%d+%d" % ((150) , (250)) )

    welcomelabel = Label(root , text = "Welcome to the chat room!!")
    welcomelabel.grid(row = 1 , columnspan = 2)

    userlabel = Label(root , text = "Enter Player Name")
    userlabel.grid(row = 3)

    user = Entry(root)
    user.bind("<Return>" , submitenter)
    user.grid(row = 3 , column = 1)

    submit_button = Button(root , text = "Enter" , command = submit)
    submit_button.grid(row = 3 , column = 2)

    root.mainloop()

def menu():

    global menu_w

    

    menu_w = Tk()

    menu_w.title("Welcome to Hang'em!")
    menu_w.maxsize(width = 305 , height = 230)
    menu_w.geometry("305x230+%d+%d" % ((500) , (250)) )

    img = PhotoImage( file = "images/welcome.png")
    imgb = PhotoImage( file = "images/play.png")
    imgr = PhotoImage( file = "images/rules.png")
    imgq = PhotoImage( file = "images/quit.png")

    welcome_canvas = Canvas(menu_w , bg = 'blue' , width = 300 , height = 200 )
    welcome_canvas.pack(side = TOP)
    welcome_canvas.create_image( 152 , 102 , image = img)

    play = Button(menu_w , command = connect)
    play.pack(side = LEFT)
    play.config(image = imgb , height = 20 , width = 94)
  
    help = Button(menu_w , command =  disp_help )
    help.pack(side = LEFT)
    help.config(image = imgr , height = 20 , width = 94)

    esc = Button(menu_w  , command = quit_game)
    esc.pack(side = LEFT)
    esc.config(image = imgq , height = 20 , width = 94)

    menu_w.mainloop()

def disp_help():
    
    message = messagebox.showinfo("Help" , "Rules of the game:\n\n" +
                                  "-The point of the game is to guess the word set by a player" +
                                  " before you run our of tries.\n\n" +
                                  "-One player will have the option to set a word of their own " +
                                  "or to pick a random word from the database.\n\n" +
                                  "-If its your turn to guess, you can either hit 'Letter Request'  to guess a specific" + 
                                  " letter or you can hit 'Guess word' if you think you know the" +
                                  " hidden word.\n\n" +
                                  "-If you guess the word, you win the round and a new word can be set.\n\n" +
                                  "-If you run out of tries you will be HANGED and the game is over.\n\n" +
                                  "-PENALTIES:\t-1 for an incorrect letter guess.\n\t\t-2 for an incorrect word guess. ")


def quit_game():
        sys.exit(0)  
    

#---------------------------------------------------------------------
clientsock = socket(AF_INET , SOCK_DGRAM)
clientsock.bind( (servername , port) )

menu()   

userlength = len( name )  

if userlength > 0:

    global msg
    global canvas
    global img1 , img2 , img3 , img4 , img5 , img6 , img7

    chat = Tk()
    
    img1 = PhotoImage(file = 'images/hng1.png') 
    img2 = PhotoImage(file = 'images/hng2.png') 
    img3 = PhotoImage(file = 'images/hng3.png') 
    img4 = PhotoImage(file = 'images/hng4.png') 
    img5 = PhotoImage(file = 'images/hng5.png')
    img6 = PhotoImage(file = 'images/hng6.png')      
    img7 = PhotoImage(file = 'images/hng7.png') 
    img8 = PhotoImage(file = 'images/hng8.png') 
    imgsend = PhotoImage(file = 'images/send.png')
    imgquit = PhotoImage(file = 'images/quits.png')
    imgsetw = PhotoImage(file = 'images/setw.png')
    imgsetl = PhotoImage(file = 'images/setl.png')
    imgrand = PhotoImage(file = 'images/rndm.png')
    imgguess = PhotoImage(file = 'images/guess.png')


    chat.title("Hang 'em. Chat ")
    chat.minsize( width = 735 , height = 330 )
    chat.geometry("740x450+%d+%d" % ((300) , (250)) )

    hangman = Label(chat , text = "Welcome to Hang'em, " + name + "!!\n" , font = ("Arial" , 15) )
    hangman.pack(side = TOP)
    #hangman.place(x = 0 , y = 0 , relwidth = 1 , relheight = 1)

    topframe = Frame(chat , bg = "green" )
    topframe.pack( side = TOP)

    bottomframe = Frame(chat , height = 30)
    bottomframe.pack( side = BOTTOM )

    sideframe = Frame(topframe , bg = "green" , bd = 6 , width = 80 , height = 40)
    sideframe.pack(side = RIGHT)

    s = Scrollbar(topframe)
    s.pack(side = RIGHT , fill = Y)

    chatlabel = Label(bottomframe , text = "You: ")
    chatlabel.pack( side = LEFT)
    
    msg = Entry(bottomframe , width = 50)
    msg.bind("<Return>" , enter)
    msg.pack(side = LEFT)

    chatbutton = Button(bottomframe , text = "Send"  ,  command = chatsend , height = 20 , width = 150)
    chatbutton.pack(side = LEFT)
    chatbutton.config( image = imgsend)

    quitbutton = Button(bottomframe , text = "Quit" , command = quitchat , height = 20 , width = 150)
    quitbutton.pack(side = BOTTOM)
    quitbutton.config( image = imgquit)

    rt = threading.Thread( target = recieveMsg , args = ("Thread" , clientsock , topframe) )
    rt.start()

    block = Text( sideframe , width = 24 , height = 1 , bg = "grey")
    block.grid( row = 1 , column = 1 , stick = E)
    block.insert(INSERT , "Word has not been set.")
    
    setbutton = Button(sideframe , text = "Set Word" , height = 20 , width = 150 , command = set_word)
    setbutton.grid(row = 1 , column = 0 , stick = W  )
    setbutton.config(image = imgsetw)

    guessbutton = Button(sideframe , text = "Guess Word" , height = 20 , width = 150 , command = guess_word)
    guessbutton.grid( row = 2 , column = 0 , stick = W)
    guessbutton.config(image = imgguess)

    letter = Button(sideframe, text = "Letter Request." , height = 20 , width = 150 , command = guess_letter)
    letter.grid(row = 3 , column = 0 , stick = W)
    letter.config( image = imgsetl)

    randombutton = Button(sideframe , text = "Random Word" , height = 20 , width = 150 , command = randomwrd )
    randombutton.grid( row = 3 , column = 1 , stick = E)
    randombutton.config( image = imgrand)

    usedletter = Text(sideframe , width = 40, height = 1 , bg = "grey")
    usedletter.grid(row = 4 , columnspan = 2 , stick = E )
    usedletter.insert(INSERT , "Used letters will appear here...")


    canvas = Canvas(sideframe  ,width = 350 , height = 250 )
    canvas.grid( row = 5 , columnspan = 2)
    
    #the 2 number represent where the center of the image is to be placed in the canvas
    canvas.create_image(175,125, image = img1)

    chat.mainloop()


rt.join()
clientsock.close()
