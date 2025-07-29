
import socket
import tkinter as tk

def send_command(command):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345)) # Replace with your server's IP if not running on the same machine
    client_socket.send(command.encode())
    client_socket.close()

def main():
    root = tk.Tk()
    root.title("Python Remote")

    left_click_button = tk.Button(root, text="Left Click", command=lambda: send_command('left_click'))
    left_click_button.pack()

    right_click_button = tk.Button(root, text="Right Click", command=lambda: send_command('right_click'))
    right_click_button.pack()

    # Example of how to send a move command
    # You can create a more sophisticated UI for this
    move_button = tk.Button(root, text="Move Mouse (10, 10)", command=lambda: send_command('move,10,10'))
    move_button.pack()

    root.mainloop()

if __name__ == '__main__':
    main()
