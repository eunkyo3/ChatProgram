from socket import *
from _thread import *

HOST = '127.0.0.1'
PORT = int(input('연결 포트 : '))

client_socket = socket(AF_INET, SOCK_STREAM) # 소켓 객체 생성
client_socket.connect((HOST, PORT)) # 연결

print ('서버 접속!')
print('/quit <-- 입력시 접속을 종료합니다.')
print('--------------------------------------------------------')

# 서버로부터 메세지를 받는 메소드
# 스레드로 구동 시켜, 메세지를 보내는 코드와 별개로 작동
def recv_data(client_socket) :
    while True :
        data = client_socket.recv(1024)

        print("받음 : ",repr(data.decode())) # 수신한 데이터를 출력

start_new_thread(recv_data, (client_socket,)) # 스레드 시작

while True:
    message = input('')
    
    if message == '/quit': # /quit 를 입력시 종료
        break

    client_socket.send(message.encode()) # 메세지를 보냄

# 소켓을 닫음
client_socket.close()
