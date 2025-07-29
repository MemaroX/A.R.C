
import socket
import pyautogui

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)
    print("Server listening on port 12345")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Got connection from {addr}")

        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(f"Received command: {data}")

            if data == 'left_click':
                pyautogui.click()
            elif data == 'right_click':
                pyautogui.click(button='right')
            elif data.startswith('move'):
                _, x, y = data.split(',')
                pyautogui.move(int(x), int(y))

        client_socket.close()

if __name__ == '__main__':
    main()
