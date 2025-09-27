import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

HOST = "127.0.0.1"
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

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

def send_message():
    mesaj = entry.get()
    if mesaj:
        client_socket.sendall(mesaj.encode())
        chat_area.insert(tk.END, f"Ben: {mesaj}\n")
        chat_area.see(tk.END)
        entry.delete(0, tk.END)

# --- UI kısmı ---
root = tk.Tk()
root.title("Client")

chat_area = scrolledtext.ScrolledText(root, width=50, height=20)
chat_area.pack(padx=10, pady=10)

entry = tk.Entry(root, width=40)
entry.pack(side=tk.LEFT, padx=10, pady=5)

send_btn = tk.Button(root, text="Gönder", command=send_message)
send_btn.pack(side=tk.LEFT)

threading.Thread(target=receive_messages, daemon=True).start()

root.mainloop()
