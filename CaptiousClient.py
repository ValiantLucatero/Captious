import socket
import threading
import time , sys
import tkinter as tk
from tkinter import messagebox

global name         #nombre del hilo que esta siendo usado
global quit         #si un jugador decide dejar el juego, esta variable será True
global actualwrd    #palabra puesta actualmente
global word_set     #Checa si una palabra esta puesta o no(True o False)
global used_bar     #Barra donde van las letras usadas (borra las letras cuando es False)
global counter      #Contador de intentos hasta que termine el juego

##--------------------------------------------------------------------------------
# inicialización de variables globales
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
# declaración de funciones
#---------------------------------------------------------------------------------
# Esta función manejará la recepción de los mensajes del servidor.
# Y los imprimirá en la GUI.
# Esta función es un hilo aparte y recibe el nombre de la ventana donde debe imprimir (chat),
# un socket (sock) y un parametro en blanco (name).
# Decodifica los comandos recibidos del servidor y los ejecuta.
#---------------------------------------------------------------------------------
def recieveMsg( name , sock , chat ):
    print("Iniciado")
    global quit, block, word_set, usedletter, actualwrd
    text = tk.Text(chat , width = 50 , height = 20 , yscrollcommand = s.set )
    s.config( command = text.yview)
    text.pack(side = tk.LEFT)
    while quit == False:
        try:
            msg, addr = sock.recvfrom( 1024 )
            message = msg.decode()
            tokens = message.split()
            #print(message + " DEL SERVER") #Para identificar los mensajes del servdidor
        except ConnectionResetError:
            print("Error del hilo")
            message = messagebox.showerror("Error de Conexión!" , "No se logró una conexión...")
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
            #print("MANDE SETWORD") #Para debugging
            block.delete(1.0 , 'end')
            block.insert(tk.INSERT , tokens[1])
        elif  tokens[0] == 'SETWRD2':
            check_set(tokens[2])
            #print("MANDE SETWORD2") #debugging
            block.delete(1.0 , 'end')
            block.insert(tk.INSERT , tokens[1])
        elif tokens[0] == 'UPDATEWRD':
            check_set(tokens[2])
            #print("MANDE UDPATE") #debugging
            actualwrd = tokens[1]
        elif tokens[0] == 'RLET':
            global used_bar
            if(used_bar == 'False'):
                usedletter.delete(1.0 , 'end')
                used_bar = 'True'
            #print("MANDE RLET") #debugging
            letter = tokens[1].upper()
            usedletter.insert(tk.INSERT , letter )
        elif message != "QUITCOMM":
            #Imprimimos lo que quede en el chat
            text.insert(tk.INSERT , message)
            text.see(tk.END)
        else:
            quit = True
    print("Hilo terminado")

#---------------------------------------------------------------------------------
# Esta función se ejecutará cuando des click en el botón 'Enviar' ya que hayas ingresado un nombre
# Conecta al cliente con el servidor.
#---------------------------------------------------------------------------------
def submit():
    global name
    userName = user.get()
    name = userName
    if len(userName) > 0:  
        try:
            clientsock.sendto(userName.encode(), (servername , serverport))
        except ConnectionResetError:
           print("Error de conexión!")
        root.destroy()
        menu_w.destroy()
    else:
        disp_name_error()

#---------------------------------------------------------------------------------
# Esta funcion se ejecutará cuando des 'Enter' (en el teclado) ya que hayas ingresado un nombre de usuario.
# Conecta al cliente con el servidor
#---------------------------------------------------------------------------------
def submitenter(event):
    global name
    userName = user.get()
    name = userName
    if len(userName) > 0:  
        try:
            clientsock.sendto( userName.encode() , (servername , serverport) )
        except ConnectionResetError:
           print("Error de conexión!")
        root.destroy()
        menu_w.destroy()
    else:
        disp_name_error()

#---------------------------------------------------------------------------------
# Esta función enviará los mensajes escritos en la ventana de chat cuando le des
# click al botón 'Enviar'.
# Estos mensajes serán broadcasteados a todos los demás jugadores.
# Los mensajes son enviados con la forma [jugador]: 'mensaje' 
# Si no hay nada en la caja de texto, no se envia nada.
#---------------------------------------------------------------------------------
def chatsend():
    global name 
    message = msg.get()
    if len(message) > 0: 
        line = "[" + name + "]: " + message + "\n"
        clientsock.sendto( line.encode() , (servername , serverport) )
        msg.delete(0 , 'end')

#---------------------------------------------------------------------------------
# Esta función enviará los mensajes escritos en la ventana de chat cuando presiones
# 'enter'.
# Estos mensajes serán broadcasteados a todos los demás jugadores.
# Los mensajes son enviados con la forma [jugador]: 'mensaje' 
# Si no hay nada en la caja de texto, no se envia nada.
#---------------------------------------------------------------------------------
def enter(event):
    global name
    message = msg.get()
    if len(message) > 0: 
        line = "[" + name + "]: " + message + "\n"
        clientsock.sendto( line.encode() , (servername , serverport) )
        msg.delete(0 , 'end')

#---------------------------------------------------------------------------------
# Error catching por si el usuario no pone un nombre de usuario
#---------------------------------------------------------------------------------
def disp_name_error():
    messagebox.showerror("Sin nombre!" , "Por favor, ingresa tu nombre\n")

#---------------------------------------------------------------------------------
# Si un jugador decide salir del juego envia un comando al server con la forma
# '[jugador]: ^q'
# El comando '^q' es cachado y ejecutado por el server 
#---------------------------------------------------------------------------------
def quitchat():
    line = "[" + name + "]: ^q \n"
    clientsock.sendto( line.encode() , (servername , serverport) )
    chat.destroy()

#---------------------------------------------------------------------------------
# Esta función es el pop up para que el usuario ingrese una palabra para adivinar
#---------------------------------------------------------------------------------
def set_word():
    global wordwindow 
    global input
    wordwindow = tk.Tk()
    wordwindow.title("Escoge una palabra difícil (Pero bien escrita!)")
    wordwindow.minsize(width = 200, height =50)
    wordlabel = tk.Label( wordwindow, text = "Ingresa tu palabra: ")
    wordlabel.pack(side = tk.LEFT)
    input = tk.Entry( wordwindow )
    input.pack(side = tk.LEFT)
    button = tk.Button( wordwindow , text = "Poner", width = 20 , command = wordsend )
    button.pack(side = tk.LEFT)
    wordwindow.mainloop()

#---------------------------------------------------------------------------------
# Esta función se ejecuta al darle click en 'Poner' en la 'wordwindow' (pop up arriba)
# Envía el comando al server con la forma '[player]: SETWRD palabra'
# Aquí modificamos 'word_set' Si es falso no hay palabra colocada y puedes ponerla
# Si es verdadero muestra que no es tu turno para ponerla y que ya hay una.
#---------------------------------------------------------------------------------
def wordsend():
    global block , word_set
    word = input.get()
    tokens = word.split()
    if (len(tokens[0]) > 0):
        if word_set == 'False':  
            print("Boton picado")
            block.delete(1.0 , 'end')
            block.insert(tk.INSERT , tokens[0])
            command = "[" + name + "]: SETWRD " + tokens[0] 
            clientsock.sendto( command.encode() , (servername , serverport))
        else:
            messagebox.showerror("Palabra ya puesta!!" , "No es tu turno de poner una palabra, espera tu turno!")
        wordwindow.destroy()

#---------------------------------------------------------------------------------
# Esta función es el pop up para que el jugador adivine la palabra completa
#---------------------------------------------------------------------------------

def guess_word():
    global guess 
    global guessinput
    guess = tk.Tk()
    guess.title("¿Te la sabes?")
    tk.Label(guess , text = "Intento: " ).pack(side = tk.LEFT)
    guessinput = tk.Entry( guess )
    guessinput.pack( side = tk.LEFT)
    tk.Button(guess , text = "Será?..." , command = send_guess).pack(side = tk.LEFT)
    guess.mainloop()

#---------------------------------------------------------------------------------
# Esta función es ejecutada cuando le das click al botón 'Será?...' del pop up para
# adivinar de arriba
# Envia el comando al server con la forma '[jugador]: GUESSWRD palabra'
#---------------------------------------------------------------------------------
def send_guess():
    gword = guessinput.get()
    tokens = gword.split()
    if( len(tokens[0]) > 0 ):
        command = "[" + name + "]: GUESSWRD " + tokens[0] 
        clientsock.sendto( command.encode() , (servername , serverport) )
        guess.destroy()

#---------------------------------------------------------------------------------
# Esta función es para que el jugador adivine una letra (abre un pop up)
#---------------------------------------------------------------------------------
def guess_letter():
    global letter 
    global letterinput
    letter = tk.Tk()
    letter.title("Adivina por letra")
    tk.Label(letter , text = "letra: " ).pack(side = tk.LEFT)
    letterinput = tk.Entry( letter , width = 20 )
    letterinput.pack( side = tk.LEFT)
    tk.Button(letter , text = "¿Estará?..." , command = send_letter).pack(side = tk.LEFT)
    letter.mainloop()

#---------------------------------------------------------------------------------
# Esta función es ejecutada cuando le das en el botón '¿Estará?...' del pop up de
# arriba. Envia el comando al server con la forma '[jugador]: RLET letra'
# Antes de enviar el comando checa si solo metió un caracter para evitar errores.
# No checa si es una letra, solo si es un solo caracter. (Por las ñ y acentos)
#---------------------------------------------------------------------------------
def send_letter():
    gletter = letterinput.get()
    tokens = gletter.split()
    if( len(tokens[0]) == 1 ):
        command = "[" + name + "]: RLET " + tokens[0] 
        clientsock.sendto( command.encode() , (servername , serverport) )
        letterinput.delete(0 , 'end')

#---------------------------------------------------------------------------------
# Esta función checa y coloca el indicador de que una palabra fue puesta y si la
# barra de letras usadas debe ser limpiada
#---------------------------------------------------------------------------------
def check_set( word ):
    global used_bar, word_set
    word_set =  word
    if (word == 'False'):
        used_bar = 'False'

def randomwrd():
    if word_set == 'False':  
        command = "[" + name + "]: RANDOMWRD" 
        clientsock.sendto(command.encode() , (servername , serverport))
    else:
        messagebox.showerror("Palabra ya puesta!!" , "No es tu turno de poner una palabra, espera tu turno!")

def connect():
    #Para la primera ventana. Pide un nombre de usuario
    global root , user
    root = tk.Tk()
    root.title("Bienvenido!")
    welcomelabel = tk.Label(root , text = "Bienvenido a la sala de chat!!")
    welcomelabel.grid(row = 1 , columnspan = 3)
    userlabel = tk.Label(root , text = "Nombre:")
    userlabel.grid(row = 3, column = 0)
    user = tk.Entry(root)
    user.bind("<Return>" , submitenter)
    user.grid(row = 3 , column = 1)
    submit_button = tk.Button(root, text = "Enviar", command = submit)
    submit_button.grid(row = 3 , column = 2)
    root.mainloop()

def menu():
    global menu_w
    menu_w = tk.Tk()
    menu_w.title("Bienvenido a Captious")
    menu_w.maxsize(width = 305 , height = 230)
    menu_w.geometry("305x230+%d+%d" % ((500) , (250)) )
    img = tk.PhotoImage( file = "images/welcome.png")
    welcome_canvas = tk.Canvas(menu_w , bg = 'blue' , width = 300 , height = 200 )
    welcome_canvas.pack(side = tk.TOP)
    welcome_canvas.create_image( 152 , 102 , image = img)
    play = tk.Button(menu_w , command = connect)
    play.pack(side = tk.LEFT)
    play.config(text = "Jugar", width = 8)
    help = tk.Button(menu_w , command =  disp_help )
    help.pack(side = tk.LEFT)
    help.config(text = "Reglas", width = 8)
    esc = tk.Button(menu_w  , command = quit_game)
    esc.pack(side = tk.LEFT)
    esc.config(text = "Salir", width = 8)
    menu_w.mainloop()

def disp_help():
    messagebox.showinfo("Ayuda" , "Reglas del juego:\n\n" +
                                  "-El punto del juego es adivinar la palabra puesta por un jugador" +
                                  " antes de que te quedes sin intentos.\n\n" +
                                  "-Un jugador tendrá la opción de poner una palabra propia " +
                                  "o de escoger una palabra aleatoria de la base de datos.\n\n" +
                                  "-Si es tu turno de adivinar, puedes dar click en 'Adivinar Letra' para intentar con una letra especifica" + 
                                  " o puedes dar click en 'Adivinar Palabra' si crees saber la" +
                                  " palabra completa.\n\n" +
                                  "-Si adivinas la palabra, ganarás la ronda y una nueva palabra puede ser puesta.\n\n" +
                                  "-Si te quedas sin intentos quedarás AHORCADO y el juego termina.\n\n" +
                                  "-CASTIGOS:\n-1 por una letra mal adivinada.\n-2 por una palabra mal adivinada.\n\n")

def quit_game():
        sys.exit(0)

#---------------------------------------------------------------------
clientsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsock.bind((servername , port))
menu()
userlength = len(name)
if userlength > 0:
    global msg, canvas, img1 , img2 , img3 , img4 , img5 , img6 , img7
    chat = tk.Tk()
    img1 = tk.PhotoImage(file = 'images/hng1.png') 
    img2 = tk.PhotoImage(file = 'images/hng2.png') 
    img3 = tk.PhotoImage(file = 'images/hng3.png') 
    img4 = tk.PhotoImage(file = 'images/hng4.png') 
    img5 = tk.PhotoImage(file = 'images/hng5.png')
    img6 = tk.PhotoImage(file = 'images/hng6.png')      
    img7 = tk.PhotoImage(file = 'images/hng7.png') 
    img8 = tk.PhotoImage(file = 'images/hng8.png')

    chat.title("Captious Chat")
    chat.minsize( width = 735 , height = 330 )
    chat.geometry("740x450+%d+%d" % ((300) , (250)) )

    hangman = tk.Label(chat , text = "Bienvenido a Captious, " + name + "!!\n" , font = ("Arial" , 15) )
    hangman.pack(side = tk.TOP)

    topframe = tk.Frame(chat , bg = "green")
    topframe.pack( side = tk.TOP)

    bottomframe = tk.Frame(chat , height = 30)
    bottomframe.pack( side = tk.BOTTOM )

    sideframe = tk.Frame(topframe , bg = "green" , bd = 6 , width = 80 , height = 40)
    sideframe.pack(side = tk.RIGHT)

    s = tk.Scrollbar(topframe)
    s.pack(side = tk.RIGHT , fill = tk.Y)

    chatlabel = tk.Label(bottomframe , text = "Tu: ")
    chatlabel.pack( side = tk.LEFT)

    msg = tk.Entry(bottomframe , width = 50)
    msg.bind("<Return>" , enter)
    msg.pack(side = tk.LEFT)

    chatbutton = tk.Button(bottomframe, text = "Enviar"  ,  command = chatsend , height = 20 , width = 20)
    chatbutton.pack(side = tk.LEFT)

    quitbutton = tk.Button(bottomframe, text = "Salir" , command = quitchat , height = 20 , width = 10)
    quitbutton.pack(side = tk.BOTTOM)

    rt = threading.Thread(target = recieveMsg , args = ("Thread" , clientsock , topframe))
    rt.start()

    block = tk.Text( sideframe , width = 24 , height = 1 , bg = "grey")
    block.grid( row = 1 , column = 1 , stick = tk.E)
    block.insert(tk.INSERT , "Sin palabra")

    setbutton = tk.Button(sideframe , text = "Poner Palabra", command = set_word)
    setbutton.grid(row = 1 , column = 0 , stick = tk.W)

    guessbutton = tk.Button(sideframe , text = "Adivinar Palabra", command = guess_word)
    guessbutton.grid( row = 2 , column = 0 , stick = tk.W)

    letter = tk.Button(sideframe, text = "Adivinar Letra", command = guess_letter)
    letter.grid(row = 3 , column = 0 , stick = tk.W)

    randombutton = tk.Button(sideframe , text = "Palabra Aleatoria" , command = randomwrd )
    randombutton.grid( row = 3 , column = 1 , stick = tk.E)

    usedletter = tk.Text(sideframe , width = 40, height = 1 , bg = "grey")
    usedletter.grid(row = 4 , columnspan = 2 , stick = tk.E)
    usedletter.insert(tk.INSERT , "Las letras usadas aparecerán aquí...")

    canvas = tk.Canvas(sideframe  ,width = 350 , height = 250 )
    canvas.grid( row = 5 , columnspan = 2)
    
    #El número 2 representa donde está el centro de la imagen para colocarlo en el canvas
    canvas.create_image(175,125, image = img1)
    chat.mainloop()

rt.join()
clientsock.close()
