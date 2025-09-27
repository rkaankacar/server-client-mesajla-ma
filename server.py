import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

#  Server socket 
HOST = socket.gethostbyname(socket.gethostname())
PORT = 0  
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
PORT = server_socket.getsockname()[1]  
server_socket.listen()

clients = []

# Client handler
def handle_client(conn, addr):
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            chat_area.insert(tk.END, f"Client ({addr}): {data}\n")
            chat_area.see(tk.END)
        except:
            break
    conn.close()
    if conn in clients:
        clients.remove(conn)

#  Server başlat 
def start_server():
    chat_area.insert(tk.END, f"Server başlatıldı: {HOST}:{PORT}\n")
    chat_area.see(tk.END)

    while True:
        conn, addr = server_socket.accept()
        clients.append(conn)
        chat_area.insert(tk.END, f"Bağlantı geldi: {addr}\n")
        chat_area.see(tk.END)
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

# Mesaj gönder 
def send_message():
    mesaj = entry.get()
    if mesaj:
        for c in clients:
            try:
                c.sendall(mesaj.encode())
            except:
                pass
        chat_area.insert(tk.END, f"Server: {mesaj}\n")
        chat_area.see(tk.END)
        entry.delete(0, tk.END)

#  UI 
root = tk.Tk()
root.title("Server")

chat_area = scrolledtext.ScrolledText(root, width=50, height=20)
chat_area.pack(padx=10, pady=10)

entry = tk.Entry(root, width=40)
entry.pack(side=tk.LEFT, padx=10, pady=5)

send_btn = tk.Button(root, text="Gönder", command=send_message)
send_btn.pack(side=tk.LEFT)

# Server thread
threading.Thread(target=start_server, daemon=True).start()

root.mainloop()
