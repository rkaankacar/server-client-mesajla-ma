import socket
import threading
import tkinter as tk
from tkinter import scrolledtext


HOST = input("Server IP girin: ") 
PORT = int(input("Server port girin: "))  

#  Socket oluştur bağlan 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((HOST, PORT))
except Exception as e:
    print(f"Server'a bağlanılamadı: {e}")
    exit()

# Mesaj alma 
def receive_messages():
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            chat_area.insert(tk.END, f"Server: {data}\n")
            chat_area.see(tk.END)
        except:
            break

#  Mesaj gönder 
def send_message():
    mesaj = entry.get()
    if mesaj:
        client_socket.sendall(mesaj.encode())
        chat_area.insert(tk.END, f"Ben: {mesaj}\n")
        chat_area.see(tk.END)
        entry.delete(0, tk.END)

# UI 
root = tk.Tk()
root.title("Client")

chat_area = scrolledtext.ScrolledText(root, width=50, height=20)
chat_area.pack(padx=10, pady=10)

entry = tk.Entry(root, width=40)
entry.pack(side=tk.LEFT, padx=10, pady=5)

send_btn = tk.Button(root, text="Gönder", command=send_message)
send_btn.pack(side=tk.LEFT)

# Mesaj alma thread
threading.Thread(target=receive_messages, daemon=True).start()

root.mainloop()
