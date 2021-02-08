import socket
import random

# Lista de palabras usadas para poner una palabra en el juego, elegida al azar.
# Se pueden agregar mas.
word_list = ['batería', 'jazz', 'rinoceronte', 'servidor', 'mezcla', 'cara', 'vidrio', 'quiosco', 'plata',
             'oso', 'ornitorrinco', 'ortodoncista', 'teclado', 'número', 'espada', 'concha', 'moneda',
             'crucero', 'visión', 'aventurero', 'explorador', 'imposible', 'serpiente', 'revolver',
             'criptografía', 'documentación', 'aleatorio', 'sabana', 'parámeteros', 'caza', 'python', 
             'necronomicón', 'huevo', 'mago', 'lagartija', 'godzilla', 'cabeza', 'avispón', 'pie',
             'muere', 'velocista', 'equipo', 'construir', 'floral', 'oral', 'coral', 'caricatura', 'expedito', 
             'desborde', 'desinformación', 'apagador', 'parpadear', 'pensar', 'aunque', 'toser', 'flotar',
             'garra', 'gruñido', 'parca', 'flotación', 'falla', 'optimista', 'alegre', 'excepción',
             'analizar', 'pañoleta', 'ritmo', 'raro', 'milenio', 'faraón', 'éxtasis', 'pronunciación',
             'ártico', 'recomendar', 'deducible', 'cifrado', 'particionamiento', 'flanquear', 'plancha', 'blanco', 'zoológico',
             'tanque', 'espira', 'transitivo', 'esqueleto', 'paradoja', 'asfixia', 'depresión', 'monótono', 'sofocación']
#-----------------------
# variables globales
global hidden
global actual_word
global word_not_set
global counter
global cur_player

#------------------------
# inicialización de variables globales
counter = 0
word_not_set = True
actual_word = '*'
hidden = ''
cur_player = '' 

#------------------------
# Constantes

servername = '127.0.0.1'
port = 12000
clients = []
players = []

INIT_COUNT = 6
RLET = "RLET "
CNTR = "CNTR "
QUIT = "QUITCOMM"
SETWRD = "SETWRD "
SETWRD2 = "SETWRD2 "
CHECKSET = "CHECKSET "
UPDATEWRD = "UPDATEWRD "


def broadcast( clients , message , sock , addr):

    tokens = message.split()

    for client in clients:

        if (tokens[0] == 'SETWRD'):
            handle_setword( client , message , sock , addr , tokens[0])

        if( message == '!^q!' and str(client) == str(cur_player)):
            sock.sendto("\nGanaste! Felicitaciones!\n".encode() , client)

        elif( message == '!^q!'):
            sock.sendto("\nFuiste AHORCADO! Fin del Juego!\n".encode() , client)

        else:
            if( message != '!^q!' ):
                sock.sendto(f"{message}\n".encode() , client)
            

def handle_setword( client , message , sock , addr , word):
    
    if (client != addr and word == 'SETWRD'):

        sock.sendto(message.encode() , client)
            

    elif (client == addr and word == 'SETWRD'):
        
        print("nada")
           
def hide_word( word ):
    
    global hidden 

    hidden = '*' * len(word)

    return hidden

def checkset(clients , servsocket , addr):

    set = CHECKSET + str(word_not_set)
    broadcast(clients , set , servsocket , addr)

def player_quit(clients , servsocket , addr , player):

    
    left = player + " DEJÓ LA SALA DE CHAT.\n"
    servsocket.sendto(QUIT.encode() , addr)
    broadcast(clients , left , servsocket , addr)
    clients.remove(addr)
    

def setwrd(clients , servsocket , addr , player , word):

    global word_not_set , actual_word , counter , hidden , cur_player

    if(word_not_set == True):

        counter = INIT_COUNT
        cur_player = str(addr)

        print("este es el jugador actual: " + cur_player)

        message = player + " ha puesto una palabra para adivinar.\n"
        print(message)

        message2 = "Intentos restantes: [" + str(counter) + "]\n"
        message3 = CNTR + str(counter)

        actual_word = word
        hidden = hide_word(actual_word)

        update = UPDATEWRD + actual_word + " True"
        broadcast(clients , update , servsocket , addr)

        set = tokens[1] + " " + hidden
        print("Esto esta puesto: " + set)

        broadcast(clients , message , servsocket , addr)
        broadcast(clients , set , servsocket , addr)
        broadcast(clients , message2 , servsocket , addr)
        broadcast(clients , message3 , servsocket , addr)


servsocket = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
servsocket.bind((servername , port))

print("Listo para recibir:")

while True:

    try:

        message , addr = servsocket.recvfrom(1024)

        print(str(addr) + " dijo " + message.decode() )#identificador para los mensajes recibidos de los clientes
        
        modmsg = message.decode()
        tokens = modmsg.split()

        if addr not in clients:

            #Añade el nombre de usuario a la lista de direcciones conectadas
            #-----------------------
            clients.append(addr)
            welcome = str( message.decode() ) + " se ha unido al chat\n"
            broadcast(clients , welcome , servsocket , addr)
            #-----------------------

        else:
            #Decodificamos cualquier comando enviado por un cliente
            if tokens[1] == '^q':

                player = tokens[0]
                player_quit(clients , servsocket , addr , player )


            elif tokens[1] == 'CHECKSET':

                checkset(clients , servsocket , addr)

            elif tokens[1] == 'SETWRD':

                player = tokens[0]
                word = tokens[2].lower()

                setwrd(clients , servsocket , addr , player , word)

            elif tokens[1] == 'RLET':

                index  = 0
                player = tokens[0]
                letter = tokens[2]
                count = len(actual_word)
                temp = ''
                hit = '0' #indicador de que una letra fue adivinada (0-false , 1-true)

                while index < count:

                    if ( actual_word[index] == letter ):

                        print( str( actual_word[index] ) + " Este es el índice" )#identificador para la letra encontrada en la palabra
                        temp = temp + letter

                        hit = '1'

                    else:

                        temp = temp + hidden[index]

                    index = index + 1

                if hit == '1':

                    message = player + " adivinó una letra\n"
                    broadcast(clients , message , servsocket , addr)

                if hit == '0':

                    counter = counter - 1
                    message = player + " NO adivinó una letra\n"
                    message2 = "Intentos restantes: [" + str(counter) + "]\n"
                    usedletter = RLET + letter
                    message3 = CNTR + str(counter)

                    broadcast(clients , usedletter , servsocket , addr)
                    broadcast(clients , message , servsocket , addr)
                    broadcast(clients , message2 , servsocket , addr)
                    broadcast(clients , message3 , servsocket , addr)


                if counter == 0:

                    print("FIN DEL JUEGO " + str(counter) )

                    #Enviamos el mensaje al jugador que perdió o ganó
                    won = "!^q!"
                    broadcast(clients , won , servsocket , cur_player)
                    message = "La palabra ha sido mostrada.\n"
                    broadcast(clients , message , servsocket , addr)
                    #--------------------------------------------------

                    set = SETWRD2 + actual_word + " False"
                    broadcast(clients , set , servsocket , addr)

                    cur_player = '' #reinicia al jugador actual

                hidden = temp
                    
                if (hidden == actual_word):

                    win_image = CNTR + " W" 
                    winmsg = tokens[0] + " adivinó la palabra!!\n" 
                    broadcast(clients , win_image , servsocket , addr)
                    broadcast(clients , winmsg , servsocket , addr)
                    set = SETWRD2 + hidden + " False"

                else:
                    if counter != 0:
                        set = SETWRD2 + hidden + " True"

                broadcast(clients , set , servsocket , addr) # Actualizamos a los jugadores del estatus de la palabra

            elif tokens[1] == 'GUESSWRD':

                player = tokens[0]
                guessword = tokens[2]

                if (actual_word == guessword):

                    message = player + " adivinó la palabra!\n"
                    set = SETWRD2 + actual_word + " False"
                    win_image = CNTR + " W" 

                    broadcast(clients , set , servsocket , addr) # Mostramos a todos los jugadores la palabra
                    broadcast(clients , message , servsocket , addr) # Mensaje a todos los jugadores de que alguien ya adivinó la palabra
                    broadcast(clients , win_image , servsocket , addr) 
                    
                else:
                    counter = counter - 2

                    if counter < 0 :
                        counter = 0

                    message2 = "Intentos restantes: [" + str(counter) + "]\n"
                    message = player + " trató de adivinar la palabra! Pero falló.\n"
                    message3 = CNTR + str(counter)

                    broadcast(clients , message , servsocket , addr) # Mensaje a todos los jugadores de que alguien no le atinó
                    broadcast(clients , message2 , servsocket , addr)
                    broadcast(clients , message3 , servsocket , addr) # actualiza a cada jugador del contador

                    if counter == 0:

                        print("FIN DEL JUEGO " + str(counter) )

                    #Enviamos el mensaje correcto al usuario que ganó o perdió
                        won = "!^q!"
                        broadcast(clients , won , servsocket , cur_player)
                        message = "La palabra ha sido mostrada.\n"
                        broadcast(clients , message , servsocket , addr)
                    #----------------------------------------------------------

                        set = SETWRD2 + actual_word + " False"
                        broadcast(clients , set , servsocket , addr)

                        cur_player = '' #reinicia al jugador actual

            elif tokens[1] == 'RANDOMWRD':

                actual_word = random.choice(word_list)
                counter = INIT_COUNT   
                hidden = hide_word(actual_word)     
                                        
                update = UPDATEWRD + actual_word + " True"

                print("Palabra aleatoria: " + actual_word )#Identificadoor

                message = tokens[0] + " ha puesto una palabra aleatoria.\n"
                print(message)#Identificador

                message2 = "Intentos restantes: [" + str(counter) + "]\n"
                message3 = CNTR + str(counter)

                set = SETWRD2 + hidden + ' True'
                print("Esto está puesto: " + set)#Identificador

                broadcast(clients , update , servsocket , addr)
                broadcast(clients , message , servsocket , addr)
                broadcast(clients , set , servsocket , addr)
                broadcast(clients , message2 , servsocket , addr)
                broadcast(clients , message3 , servsocket , addr)


            else:
                broadcast( clients , modmsg , servsocket , addr)
    except:
        pass
servsocket.close()
