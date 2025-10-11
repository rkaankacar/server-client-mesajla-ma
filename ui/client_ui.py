import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
import threading
from core.network.client import ChatClient


class ClientUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # önce gizle

        self.HOST = simpledialog.askstring("Giriş", "Server IP girin:")
        self.PORT = simpledialog.askinteger("Giriş", "Server port girin:")

        if not self.HOST or not self.PORT:
            messagebox.showerror("Hata", "IP ve port girilmedi!")
            exit()

        self.client = ChatClient(self.HOST, self.PORT)
        try:
            self.client.connect()
        except Exception as e:
            messagebox.showerror("Hata", f"Server'a bağlanılamadı: {e}")
            exit()

        self.root.deiconify()
        self.root.title("Client")

        # Chat ekranı
        self.chat_area = scrolledtext.ScrolledText(self.root, width=50, height=20)
        self.chat_area.pack(padx=10, pady=10)

        # Mesaj giriş alanı
        self.entry = tk.Entry(self.root, width=40)
        self.entry.pack(side=tk.LEFT, padx=10, pady=5)

        self.send_btn = tk.Button(self.root, text="Gönder", command=self.send_message)
        self.send_btn.pack(side=tk.LEFT)

        # Mesajları al
        self.client.start_receiving(self.handle_received)

    def handle_received(self, message):
        # Server zaten mesajı şifreli olarak gönderiyor
        self.chat_area.insert(tk.END, f"Server: {message}\n")
        self.chat_area.see(tk.END)

    def send_message(self):
        mesaj = self.entry.get()
        if not mesaj:
            return
        # Client her zaman düz mesaj gönderir, şifrelemeyi server yapacak
        self.client.send(mesaj)
        self.chat_area.insert(tk.END, f"Ben: {mesaj}\n")
        self.chat_area.see(tk.END)
        self.entry.delete(0, tk.END)

    def run(self):
        self.root.mainloop()
