#Implementação do cliente
#Alunos
    # Kevin Alexandre de Castro Lourencini - 102027
    # Maria Victória Fernandes Vaz - 105470

#Bibliotecas necessárias
import socket

HOST = '127.0.1.1'  #Endereço IP do cliente
PORT = 20000    #Porta em que o servidor está (destino)

#Definindo nosso protoclo como UDP para enviar mensagens
UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
#Definindo nosso protocolo como TCP para enviar de arquivos
TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

destiny = (HOST, PORT) #Definindo o host de origem

message = '' #Declarando a mensagem que será enviada
actualUser = False #Varável que vai dizer se o usuário está conectado

while True:     #Definindo e estabelecendo comunicação com o servidor
    
    if actualUser==False:  #Caso seja a primeira iteração do usuário, pede para se declarar
        print("Nome de Usuário: ")
        actualUser = input() #Lemos o nome do usuário
        message = "USER:"+actualUser #Montamos a mensagem que será enviada para o servidor
        UDP.sendto(message.encode(), destiny) #Enviando a mensagem 
    else:
        message = input()
        
        #Verificamos qual foi amensagem lida e fazemos a operação correspondente
        if message=="/bye":     #Se o usuário digitar '/bye', envia bye ao servidor e termina a conexão
            message = "BYE"
            UDP.sendto(message.encode(), destiny) #Enviando a mensagem 
            break
        
        elif  message=="/list": #Se o comando foi '/list', manda o comando LIST ao servidor
            message = "LIST"
            UDP.sendto(message.encode(), destiny) #Enviando a mensagem 
            
        elif  message.find("/file")!=-1:    #Verifica se a mensagem digitada foi um 'file' e se sim, envia os dados
            UDP.sendto("FILE".encode(), destiny)
            message = "FILE:"+message[6:len(message):1]+"\n"
            TCP.connect(destiny)
            TCP.send(message.encode()) #Enviando a mensagem (com TCP pois há troca de arquivos)
            TCP.close()
        
        elif  message.find("/get")!=-1: #Verifica se o comando foi um '/get' e se sim, pede os dados do arquivo solicitado
            UDP.sendto("GET".encode(), destiny)
            message = "GET:"+message[6:len(message):1+"\n"]
            TCP.connect(destiny)
            TCP.send(message.encode()) #Enviando a mensagem (com TCP pois há troca de arquivos)
            TCP.close()
        
        else: 
            message = "MSG:"+message #Envia no formato adequado uma mensagem qualquer que o usuário digitar
            UDP.sendto(message.encode(), destiny) #Enviando a mensagem 


    #Tratamento das mensagens recebidas do servidor
    message, server = UDP.recvfrom(1024) #Para receber algo do servidor
    
    #Tratamento de respostas do servidor do tipo INFO
    if message.decode().find("INFO") != -1:
        message = message.decode()[5:len(message):1]

    #Tratamento de respostas do servidor do tipo MSG
    elif message.decode().find("MSG") != -1:
        #Formatando a resposta do servidor para ficar na maneira mostrada na especificação do trabalho
        message = message.decode()
        message = message[4:len(message):1]
        name = message[0:message.find(':'):1]
        message = name + " disse: " + message[message.find(':')+1:len(message):1]
        #A mensagem é mostrada e nada abaixo dela preisa ser executado nessa iteração
        print(message)
        continue

    if message.decode() != '' : print(message.decode()) #Imprimindo resposta do servidor


UDP.close() #Encerra a conexão