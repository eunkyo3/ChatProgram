import socket

HOST = ''  # 호스트를 지정하지 않으면 가능한 모든 인터페이스를 의미합니다.
PORT = 1820  # 사용할 포트 번호를 지정합니다.

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # TIME_WAIT 상태에서도 포트를 재사용할 수 있도록 설정합니다.
server_socket.bind((HOST, PORT))  # bind 메서드를 호출하여 소켓을 특정 인터페이스와 포트에 연결합니다.
server_socket.listen()  # 서버를 시작합니다.

print('Server listening on port', PORT)

while True:
    client_socket, client_addr = server_socket.accept()  # 클라이언트의 연결을 기다립니다.
    print('Client connected from', client_addr)

    while True:
        data = client_socket.recv(1024)  # 클라이언트로부터 데이터를 수신합니다.
        if not data:
            break

        print('[Client]:', data.decode())  # 수신한 데이터를 출력합니다.

        message = input('[Server] > ')  # 서버 측에서 메시지를 입력합니다.
        client_socket.send(message.encode())  # 클라이언트로 메시지를 전송합니다.

    client_socket.close()  # 클라이언트 소켓을 닫습니다.
