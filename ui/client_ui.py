import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox, StringVar, IntVar
import threading
from core.network.client import ChatClient

class ClientUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  

        
        self.HOST = simpledialog.askstring("Giriş", "Server IP girin:", initialvalue="127.0.0.1")
        self.PORT = simpledialog.askinteger("Giriş", "Server port girin:", initialvalue=12345)

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
        self.root.title("Client - Güvenli Kripto Chat")
        self.root.geometry("700x750") 

    
        self.chat_area = scrolledtext.ScrolledText(self.root, width=80, height=20)
        self.chat_area.pack(padx=10, pady=10)

    
        settings_frame = tk.LabelFrame(self.root, text="Kriptografi Laboratuvarı", padx=10, pady=10)
        settings_frame.pack(padx=10, pady=5, fill="x")

        
        tk.Label(settings_frame, text="Algoritma Seç:").grid(row=0, column=0, sticky="e", padx=5)
        self.algo_var = StringVar(value="Sezar")
        
        algorithm_list = [
            "Sezar", "Vigenere", "Substitution", "Affine", "RailFence",
            "Playfair", "ROT13", "Columnar", "Polybius", "Pigpen",
            "Route", "Hill", "RSA", "DES", "DSA"
        ]
        
        self.algo_menu = tk.OptionMenu(settings_frame, self.algo_var, *algorithm_list)
        self.algo_menu.grid(row=0, column=1, columnspan=3, sticky="w", padx=5)

        
        # 1. Satır: Shift ve Key
        tk.Label(settings_frame, text="Shift (Sezar):").grid(row=1, column=0, sticky="e")
        self.shift_var = IntVar(value=3)
        tk.Entry(settings_frame, textvariable=self.shift_var, width=5).grid(row=1, column=1, sticky="w")

        # Key sadece Vigenere için değil; DES, Hill, Playfair, Columnar için de kullanılır.
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
        
        
        send_frame = tk.Frame(self.root)
        send_frame.pack(padx=10, pady=10)

        self.entry = tk.Entry(send_frame, width=55)
        self.entry.pack(side=tk.LEFT, padx=5)

        self.send_btn = tk.Button(send_frame, text="🔒 Şifrele ve Gönder", command=self.send_message, bg="#ffcccb", font=("Arial", 10, "bold"))
        self.send_btn.pack(side=tk.LEFT, padx=5)

        
        self.client.start_receiving(self.handle_received)

    def handle_received(self, message):
    
        self.chat_area.insert(tk.END, f"Gelen: {message}\n")
        self.chat_area.see(tk.END)

    def send_message(self):
        mesaj = self.entry.get()
        if not mesaj:
            return


        algo = self.algo_var.get()
        
        params = {
            "shift": self.shift_var.get(),
            "key": self.key_var.get(),
            "a": self.a_var.get(),
            "b": self.b_var.get(),
            "rails": self.rails_var.get()
        }

        
        self.client.send_encrypted(mesaj, algo, **params)
        
        # Ekrana bilgi ver
        self.chat_area.insert(tk.END, f"Ben ({algo}): {mesaj} -> [ŞİFRELİ GÖNDERİLDİ]\n")
        self.chat_area.see(tk.END)
        self.entry.delete(0, tk.END)

    def run(self):
        self.root.mainloop()