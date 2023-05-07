#Implementação do servidor
#Alunos
    # Kevin Alexandre de Castro Lourencini - 102027
    # Maria Victória Fernandes Vaz - 105470

#Bibliotecas necessárias
import socket
import threading

HOST = ''    #Armazenando o enderaço IP do servidor
PORT = 20000 #Armazenando a porta que vamos usar

#Definindo nosso protoclo como UDP para enviar mensagens
UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
#Definindo nosso protocolo como TCP para enviar de arquivos
TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ORIG = (HOST, PORT) #Definindo o host de origem
UDP.bind(ORIG) #Define o endereço do socket do nosso servidor

USER = {} #Lista de suários conectados ao servidor.

while True:

    if len(USER)==0: print("Aguardando conexão...")
    
    message, client = UDP.recvfrom(1024) #Lendo as informações recebidos do cliente
    
    if message.decode().find("USER") != -1: #Caso a mensagem do cliente for um cadastro de usuário
        name = message.decode()[5:len(message):1]    #verifica o nome do cliente
        USER[name]=client   #armazena o nome do cliente e o cliente
        message = "INFO:"+name+" entrou"    #cria a mensgame de alerta de entrada de novo usuário

        for c in USER: #Para cada usuário ativo
            UDP.sendto(message.encode(), USER[c]) #Enviando uma mensagem dizendo que o novo usuário entrou

    elif message.decode().find("LIST") != -1:   
        break
        

UDP.close() #Encerra a conexão
        

        













# #Função para permitir que o servidor receba conexões em paralelo
# def makeConnection(connection, client):
    
#     while True:
#         message = connection.recv(1024).decode()
#         if message == 'BYE':
#             break
    
#     print(client, 'saiu do servidor.')
#     connection.close()