#Implementação do servidor
#Alunos
    # Kevin Alexandre de Castro Lourencini - 102027
    # Maria Victória Fernandes Vaz - 105470

#Bibliotecas necessárias
import socket
import threading
#---------------------------
#Função que possibilitará o paralelismo de requisições 
def multConnections(message, client):

    while True:
        
        if message.decode().find("USER") != -1: #Caso a mensagem do cliente for um cadastro de usuário
            name = message.decode()[5:len(message):1]  #Encontra o nome do cliente
            USER[name]=client   #Armazena o nome do cliente e o cliente
            message = "INFO:"+name+" entrou"  #Cria a mensagem de alerta de entrada de novo usuário
    
            for us in USER: #Para cada usuário ativo
                if us!=name : UDP.sendto(message.encode(), USER[us]) #Enviando uma mensagem dizendo que o novo usuário entrou
            message = ''
            UDP.sendto(message.encode(), USER[name]) #Enviando false para o cliente atual porque ele não precisa exibir a mensagem de que ele mesmo entrou

        elif message.decode()=="LIST":   #Caso o usuário peça a lista de usuários ativos
            message = "INFO:Clientes conectados:\n"
            for us in USER:
                message += (us + ", ") #Montando uma string com o nome dos usuários conectados 
            
            message = message[0:len(message)-2:1] #Retirando a última vírgula e espaço após o último usuário
            UDP.sendto(message.encode(), client) #Enviando a resposta para o cliente

        elif message.decode()=="BYE": #Caso o usuário queira finalizar a conexão
            name = ''
            for us in USER: #busca o nome do usuário que saiu da conecção
                if USER[us] == client:
                    name = us   #Uma vez encontrado o nome, salva para avisar os outros usuários
            message = name+" saiu"  #Monta a mensagem de aviso
            for us in USER: #Para todos os usuários ativos no servidor, avisa que o usuário que saiu, foi desconectado.
                if us!=name : 
                    UDP.sendto(message.encode(), USER[us]) #Informamos para os outros usuários que ele saiu
            UDP.sendto("BYE".encode(), client)
            break #A conexão será encerrada

        elif message.decode().find("MSG") != -1:  #Tratamento de mensagens entre os usuários
            name =''
            for us in USER:
                if USER[us] == client:  #Busca o nome do usuário que mandou a mensagem
                    name = us
            
            message = "MSG:"+name+":"+message.decode()[4:len(message)] #Monta a mensagem a ser enviada
            print(message)
            for us in USER:
                if USER[us]!=client : UDP.sendto(message.encode(), USER[us])    #Manda a mensagem para todos osusuários ativos (exceto o que enviou)
            message = ''    #Envia um sinal ao cliente que mandou a mensagem (evitar que o emissor da mensagem fique travado)
            UDP.sendto(message.encode(), client)

        elif message.decode().find("FILE") != -1:   #tratamento para comando FILE
            connection, clt = TCP.accept()
            message = connection.recv(1025)
            content = message.decode()[message.decode().find("\n")+1:len(message.decode()):1]
            message = message.decode()[5:message.decode().find("\n"):1]
            FILES[message] = content
            message = "INFO:"+ message
            for us in USER:
                if USER[us]!=client : UDP.sendto(message.encode(), USER[us])
            message = ''    #Envia um sinal ao cliente que mandou a mensagem (evitar que o emissor da mensagem fique travado)
            UDP.sendto(message.encode(), client)

        elif message.decode().find("GET") != -1:
            connection, clt = TCP.accept()
            message = connection.recv(1025)
            file = message.decode()[4:len(message.decode()):1]
            message = FILES[file]
            connection.send(message.encode())

        message, client = UDP.recvfrom(1024) #Lendo as informações recebidos do cliente

    UDP.close() #Encerrando a conexão
    
#---------------------------
def reciveClient(UDP):
    while True:
        message, client = UDP.recvfrom(1024) #Lendo as informações recebidas
        # inicia uma nova thread para lidar com a solicitação do cliente
        threading.Thread(target=multConnections, args=(message, client)).start()
#---------------------------

HOST = ''    #Armazenando o enderaço IP do servidor
PORT = 20000 #Armazenando a porta que vamos usar

#Definindo nosso protocolo como TCP para enviar de arquivos
UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
#Definindo nosso protoclo como UDP para enviar mensagens

ORIG = (HOST, PORT) #Definindo o host de origem

#Define o endereço do socket do nosso servidor
UDP.bind(ORIG) 
TCP.bind(ORIG) #Estabelecendo uma conexão TCP
TCP.listen(1)

USER = {} #Lista de suários conectados ao servidor.
FILES = {}  #armazena os arquivos que serão enviados pelos usuários

def conexoes(con, client):
    msg = con.recv(1024)
    msg = msg.decode()
    action, message = msg.split(':', 1)
    if action == "FILE":
        content = message[message.find("\n")+1:len(message):1]
        message = message[5:message.find("\n"):1]
        FILES[message] = content
        message = "INFO:"+ message
        for us in USER:
            if USER[us]!=client : UDP.sendto(message.encode(), USER[us])
        message = ''    #Envia um sinal ao cliente que mandou a mensagem (evitar que o emissor da mensagem fique travado)
        UDP.sendto(message.encode(), client)

def recieve_TCP():
    while True:
        con, client = TCP.recvfrom(1024) #Lendo as informações recebidas
        # inicia uma nova thread para lidar com a solicitação do cliente
        threading.Thread(target=conexoes, args=(con, client)).start()

def run_server():
    
    if len(USER)==0: print("Aguardando conexão...")
    threading.Thread(target=reciveClient, args=(UDP, )).start()
    
run_server()
    
# UDP.close() #Encerra a conexão

# TCP.close() #Encerra a conexão
