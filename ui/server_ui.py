import tkinter as tk
from tkinter import scrolledtext, StringVar
import threading
from core.network.server import ChatServer
from core.encryption.encryption_factory import EncryptionFactory
import socket

class ServerUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Server")

        
        self.chat_area = scrolledtext.ScrolledText(self.root, width=70, height=25)
        self.chat_area.pack(padx=10, pady=10)

        
        self.entry = tk.Entry(self.root, width=50)
        self.entry.pack(side=tk.LEFT, padx=10, pady=5)

        
        self.send_btn = tk.Button(self.root, text="Gönder", command=self.send_message)
        self.send_btn.pack(side=tk.LEFT)

       
        self.decrypt_btn = tk.Button(self.root, text="🔓 Deşifrele", command=self.decrypt_all)
        self.decrypt_btn.pack(side=tk.LEFT, padx=5)

        
        self.algo_var = StringVar(value="Sezar")
        self.algo_box = tk.OptionMenu(self.root, self.algo_var, "Sezar", "Vigenere", "Substitution", "Affine")
        self.algo_box.pack(pady=5)

        
        self.shift_var = tk.IntVar(value=3)
        self.key_var = StringVar(value="KEY")
        self.a_var = tk.IntVar(value=5)
        self.b_var = tk.IntVar(value=8)

        tk.Label(self.root, text="Sezar Kaydırma:").pack()
        tk.Entry(self.root, textvariable=self.shift_var).pack()

        tk.Label(self.root, text="Vigenere Anahtar:").pack()
        tk.Entry(self.root, textvariable=self.key_var).pack()

        tk.Label(self.root, text="Affine a:").pack()
        tk.Entry(self.root, textvariable=self.a_var).pack()

        tk.Label(self.root, text="Affine b:").pack()
        tk.Entry(self.root, textvariable=self.b_var).pack()

       
        host = socket.gethostbyname(socket.gethostname())
        self.server = ChatServer(host, 0)

        
        self.server.plain_messages = []       # Düz mesajlar
        self.server.encrypted_messages = []   # GUI’de gösterilen şifreli mesajlar
        self.server.decrypted_messages = []   # Daha önce deşifre edilenler

        
        threading.Thread(target=self.start_server, daemon=True).start()

    def start_server(self):
        def handler(addr, data):
           
            self.server.plain_messages.append(data)

           
            cipher = EncryptionFactory.get_cipher(
                self.algo_var.get(),
                shift=self.shift_var.get(),
                key=self.key_var.get(),
                a=self.a_var.get(),
                b=self.b_var.get()
            )
            encrypted = cipher.encrypt(data)
            self.server.encrypted_messages.append(encrypted)
            self.chat_area.insert(tk.END, f"Client ({addr}): {encrypted}\n")
            self.chat_area.see(tk.END)

        self.chat_area.insert(tk.END, f"Server başlatıldı: {self.server.host}:{self.server.port}\n")
        self.chat_area.see(tk.END)
        self.server.start(handler)

    def send_message(self):
        mesaj = self.entry.get()
        if not mesaj:
            return
        cipher = EncryptionFactory.get_cipher(
            self.algo_var.get(),
            shift=self.shift_var.get(),
            key=self.key_var.get(),
            a=self.a_var.get(),
            b=self.b_var.get()
        )
        enc = cipher.encrypt(mesaj)
        self.server.send(enc)
        self.chat_area.insert(tk.END, f"Server (şifreli): {enc}\n")
        self.chat_area.see(tk.END)
        self.entry.delete(0, tk.END)

    def decrypt_all(self):
        self.chat_area.insert(tk.END, "\n--- 🔓 Deşifreleme ---\n")
       
        new_msgs = [msg for msg in self.server.plain_messages if msg not in self.server.decrypted_messages]
        for msg in new_msgs:
            self.chat_area.insert(tk.END, f"🔓 Çözüm: {msg}\n")
            self.server.decrypted_messages.append(msg)  
        self.chat_area.insert(tk.END, "--- 🔓 Bitti ---\n\n")
        self.chat_area.see(tk.END)

    def run(self):
        self.root.mainloop()
