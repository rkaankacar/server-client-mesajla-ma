import tkinter as tk
from tkinter import scrolledtext, StringVar, messagebox, IntVar
import threading
from core.network.server import ChatServer
from core.encryption.encryption_factory import EncryptionFactory
import socket

class ServerUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Server - Güvenli Dinleme İstasyonu")
        self.root.geometry("700x800")

        
        self.chat_area = scrolledtext.ScrolledText(self.root, width=80, height=25)
        self.chat_area.pack(padx=10, pady=10)

        
        send_frame = tk.Frame(self.root)
        send_frame.pack(pady=5)
        
        self.entry = tk.Entry(send_frame, width=55)
        self.entry.pack(side=tk.LEFT, padx=10)

        self.send_btn = tk.Button(send_frame, text="🔒 Şifrele ve Gönder", command=self.send_message, bg="#ffcccb", font=("Arial", 10, "bold"))
        self.send_btn.pack(side=tk.LEFT)

        
        self.decrypt_btn = tk.Button(self.root, text="🔓 EKRANI TEMİZLE VE HEPSİNİ ÇÖZ", command=self.decrypt_all, bg="#ccffcc", font=("Arial", 10, "bold"))
        self.decrypt_btn.pack(pady=5)

        
        settings_frame = tk.LabelFrame(self.root, text="Kriptografi Anahtarları", padx=10, pady=10)
        settings_frame.pack(padx=10, pady=5, fill="x")

    
        tk.Label(settings_frame, text="Algoritma Seç:").grid(row=0, column=0, sticky="e", padx=5)
        self.algo_var = StringVar(value="Sezar")
        
        algorithm_list = [
            "Sezar", "Vigenere", "Substitution", "Affine", "RailFence",
            "Playfair", "ROT13", "Columnar", "Polybius", "Pigpen",
            "Route", "Hill", "RSA", "DES", "DSA"
        ]
        
        self.algo_box = tk.OptionMenu(settings_frame, self.algo_var, *algorithm_list)
        self.algo_box.grid(row=0, column=1, columnspan=3, sticky="w", padx=5)

    
        
    
        tk.Label(settings_frame, text="Shift (Sezar):").grid(row=1, column=0, sticky="e")
        self.shift_var = IntVar(value=3)
        tk.Entry(settings_frame, textvariable=self.shift_var, width=5).grid(row=1, column=1, sticky="w")

        tk.Label(settings_frame, text="Key / Parola:").grid(row=1, column=2, sticky="e")
        self.key_var = StringVar(value="KEY")
        tk.Entry(settings_frame, textvariable=self.key_var, width=15).grid(row=1, column=3, sticky="w")

        
        tk.Label(settings_frame, text="Affine A:").grid(row=2, column=0, sticky="e")
        self.a_var = IntVar(value=5)
        tk.Entry(settings_frame, textvariable=self.a_var, width=5).grid(row=2, column=1, sticky="w")

        tk.Label(settings_frame, text="Affine B:").grid(row=2, column=2, sticky="e")
        self.b_var = IntVar(value=8)
        tk.Entry(settings_frame, textvariable=self.b_var, width=5).grid(row=2, column=3, sticky="w")

    
        tk.Label(settings_frame, text="Rail / Sütun:").grid(row=3, column=0, sticky="e")
        self.rails_var = IntVar(value=3)
        tk.Entry(settings_frame, textvariable=self.rails_var, width=5).grid(row=3, column=1, sticky="w")
        
    
        host = socket.gethostbyname(socket.gethostname())
        self.server = ChatServer(host, 0)
        
        
        
        threading.Thread(target=self.start_server, daemon=True).start()

    def start_server(self):
        def handler(addr, data):
            
            self.chat_area.insert(tk.END, f"Client ({addr}) [GİZLİ]: {data}\n")
            self.chat_area.see(tk.END)

        self.chat_area.insert(tk.END, f"Server başlatıldı: {self.server.host}:{self.server.port}\n")
        self.chat_area.see(tk.END)
        self.server.start(handler)

    def send_message(self):
        """Server da cevap yazarken şifreleyip yollar."""
        mesaj = self.entry.get()
        if not mesaj:
            return
            
        try:
            
            cipher = EncryptionFactory.get_cipher(
                self.algo_var.get(),
                shift=self.shift_var.get(),
                key=self.key_var.get(),
                a=self.a_var.get(),
                b=self.b_var.get(),
                rails=self.rails_var.get() 
            )
            enc = cipher.encrypt(mesaj)
            
            
            self.server.send(enc)
            
           
            self.server.encrypted_messages.append(enc)
            
            self.chat_area.insert(tk.END, f"Server (Ben) -> [ŞİFRELİ GİTTİ]: {enc}\n")
            self.chat_area.see(tk.END)
            self.entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Hata", f"Gönderirken hata oluştu: {e}")

    def decrypt_all(self):
        """Listede biriken şifreli mesajları, ŞU ANKİ ayarlarla çözmeye çalışır."""
        
    
        self.chat_area.delete('1.0', tk.END)
        self.chat_area.insert(tk.END, "--- 🔓 TÜM GEÇMİŞ ÇÖZÜLÜYOR ---\n\n")
        
        try:
            current_cipher = EncryptionFactory.get_cipher(
                self.algo_var.get(),
                shift=self.shift_var.get(),
                key=self.key_var.get(),
                a=self.a_var.get(),
                b=self.b_var.get(),
                rails=self.rails_var.get()
            )
        except Exception as e:
            self.chat_area.insert(tk.END, f"❌ Anahtar Hatası: {e}\n")
            return

        if not self.server.encrypted_messages:
            self.chat_area.insert(tk.END, "Hiç şifreli mesaj yok.\n")

        for idx, enc_msg in enumerate(self.server.encrypted_messages):
            try:
                plain_text = current_cipher.decrypt(enc_msg)
                self.chat_area.insert(tk.END, f"Mesaj #{idx+1} ({enc_msg}) -> 🔓: {plain_text}\n")
            except Exception as e:
                self.chat_area.insert(tk.END, f"Mesaj #{idx+1} çözülemedi: {e}\n")

        self.chat_area.insert(tk.END, "\n--- LİSTE SONU ---\n")
        self.chat_area.see(tk.END)

    def run(self):
        self.root.mainloop()