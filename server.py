from socket import *
from _thread import *

# 쓰레드에서 실행되는 코드
# 접속한 클라이언트마다 새로운 쓰레드가 생성되어 통신
def threaded(client_socket, addr):
    print('연결됨 --> ', addr[0], ':', addr[1]) # 연결된 주소 출력

    # 클라이언트가 접속을 끊을 때 까지 반복
    while True:

        try:

            # 데이터가 수신되면 클라이언트에 다시 전송
            data = client_socket.recv(1024)

            # 연결을 종료한 IP주소와 포트 번호를 출력하고 루프 종료
            if not data:
                print('연결 종료 --> ' + addr[0], ':', addr[1])
                break
            
            print(addr[0], ':', addr[1], ' --> ', data.decode())

            # 서버에 접속한 클라이언트들에게 채팅 보내기
            # 메세지를 보낸 본인을 제외한 서버에 접속한 클라이언트에게 메세지 보내기
            for client in client_sockets :
                if client != client_socket : 
                    client.send(data)

        # 에러문 출력
        except ConnectionResetError as e:
            print('연결 종료 --> ' + addr[0], ':', addr[1])
            break
    
    # 연결이 종료되면 해당 클라이언트 소켓을 리스트에서 제거 
    if client_socket in client_sockets :
        client_sockets.remove(client_socket)

    # 소켓을 닫음
    client_socket.close()
    
client_sockets = [] # 서버에 접속한 클라이언트 목록

# 서버 IP 및 열어줄 포트
HOST = '127.0.0.1'
PORT = int(input('서버 포트 : '))

# 서버 소켓 생성
print('서버 생성중..')
server_socket = socket(AF_INET, SOCK_STREAM) # 소켓 객체 생성
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # 이미 사용중인 포트를 재사용
server_socket.bind((HOST, PORT)) # 소켓을 바인딩
server_socket.listen() # 클라이언트 연결 요청을 수신 대기 상태로 만든다
print('생성 완료!')

try:
    while True:
        print('접속 기다리는중..')

        client_socket, addr = server_socket.accept() # 연결 요청 기다림
        client_sockets.append(client_socket) # 연결된 클라이언트 소켓을 리스트에 추가
        start_new_thread(threaded, (client_socket, addr)) # 스레드 시작
        print("참여자 : ", len(client_sockets))

# 에러 출력문        
except Exception as e :
    print ('에러 : ',e)

# 소켓을 닫음
finally:
    server_socket.close()
