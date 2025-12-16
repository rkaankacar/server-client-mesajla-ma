<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Client UI - RSA Key Exchange destekli
AES, DES, RSA desteği ile (kütüphane ve manuel modlar)
"""

import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox, StringVar, IntVar, ttk
import threading
from core.network.client import ChatClient
from core.encryption.encryption_factory import EncryptionFactory

=======
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox, StringVar, IntVar
import threading
from core.network.client import ChatClient
>>>>>>> 6fbfecac606b02cc84d206202e00760216dde9fa

class ClientUI:
    def __init__(self):
        self.root = tk.Tk()
<<<<<<< HEAD
        self.root.withdraw()

        # Simetrik algoritma seçimi (Key Exchange için)
        self.symmetric_algo_choice = simpledialog.askstring(
            "Simetrik Algoritma", 
            "Key Exchange için algoritma seçin (AES veya DES):",
            initialvalue="AES"
        )
        if self.symmetric_algo_choice not in ["AES", "DES"]:
            self.symmetric_algo_choice = "AES"

        # Server bağlantı bilgileri
=======
        self.root.withdraw()  

        
>>>>>>> 6fbfecac606b02cc84d206202e00760216dde9fa
        self.HOST = simpledialog.askstring("Giriş", "Server IP girin:", initialvalue="127.0.0.1")
        self.PORT = simpledialog.askinteger("Giriş", "Server port girin:", initialvalue=12345)

        if not self.HOST or not self.PORT:
            messagebox.showerror("Hata", "IP ve port girilmedi!")
            exit()

        self.client = ChatClient(self.HOST, self.PORT)
<<<<<<< HEAD
        self.client.set_preferred_algo(self.symmetric_algo_choice)
        self.client.on_key_exchange_complete = self._on_key_exchange_complete
        
=======
>>>>>>> 6fbfecac606b02cc84d206202e00760216dde9fa
        try:
            self.client.connect()
        except Exception as e:
            messagebox.showerror("Hata", f"Server'a bağlanılamadı: {e}")
            exit()

        self.root.deiconify()
<<<<<<< HEAD
        self.root.title("🔐 Client - Güvenli Kripto Chat")
        self.root.geometry("800x900")
        self.root.configure(bg="#1a1a2e")

        self._create_widgets()
        
        # Mesaj alma thread'i
        self.client.start_receiving(self.handle_received)

    def _on_key_exchange_complete(self, algo, key):
        """Key Exchange tamamlandığında çağrılır."""
        self.root.after(0, lambda: self._update_key_exchange_status(algo, key))

    def _update_key_exchange_status(self, algo, key):
        """UI'da key exchange durumunu günceller."""
        self.key_status_label.config(
            text=f"✅ Key Exchange OK | {algo} | Key: {key.hex()[:16]}...",
            fg="#00ff88"
        )
        self.chat_area.insert(tk.END, f"🔐 Key Exchange tamamlandı!\n")
        self.chat_area.insert(tk.END, f"   Algoritma: {algo}\n")
        self.chat_area.insert(tk.END, f"   Paylaşılan Anahtar: {key.hex()}\n")
        self.chat_area.insert(tk.END, f"{'='*50}\n")
        self.chat_area.see(tk.END)

    def _create_widgets(self):
        """Tüm UI bileşenlerini oluşturur."""
        
        # ===== KEY EXCHANGE DURUMU =====
        key_frame = tk.Frame(self.root, bg="#0f0f23")
        key_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(key_frame, text="🔑 RSA Key Exchange:", bg="#0f0f23", fg="#eee", 
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.key_status_label = tk.Label(key_frame, text="⏳ Bekleniyor...", 
                                          bg="#0f0f23", fg="#ffcc00", font=("Arial", 9))
        self.key_status_label.pack(side=tk.LEFT, padx=10)
        
        # ===== CHAT ALANI =====
        chat_frame = tk.LabelFrame(self.root, text="💬 Mesajlar", bg="#1a1a2e", fg="#eee", font=("Arial", 10, "bold"))
        chat_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.chat_area = scrolledtext.ScrolledText(chat_frame, width=85, height=15, 
                                                    bg="#16213e", fg="#00ff88", 
                                                    font=("Consolas", 10),
                                                    insertbackground="white")
        self.chat_area.pack(padx=5, pady=5, fill="both", expand=True)

        # ===== KRİPTOĞRAFİ AYARLARI =====
        settings_frame = tk.LabelFrame(self.root, text="⚙️ Kriptografi Laboratuvarı", 
                                        padx=10, pady=10, bg="#1a1a2e", fg="#eee", 
                                        font=("Arial", 10, "bold"))
        settings_frame.pack(padx=10, pady=5, fill="x")

        # --- Mod Seçimi ---
        mode_frame = tk.Frame(settings_frame, bg="#1a1a2e")
        mode_frame.grid(row=0, column=0, columnspan=4, sticky="w", pady=5)
        
        tk.Label(mode_frame, text="🔧 Mod:", bg="#1a1a2e", fg="#eee").pack(side=tk.LEFT, padx=5)
        self.mode_var = StringVar(value="library")
        
        ttk.Radiobutton(mode_frame, text="📚 Kütüphane", variable=self.mode_var, 
                        value="library", command=self._update_algorithm_list).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(mode_frame, text="✍️ Manuel", variable=self.mode_var, 
                        value="manual", command=self._update_algorithm_list).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(mode_frame, text="📜 Klasik", variable=self.mode_var, 
                        value="classic", command=self._update_algorithm_list).pack(side=tk.LEFT, padx=5)

        # --- Algoritma Seçimi ---
        tk.Label(settings_frame, text="🔐 Algoritma:", bg="#1a1a2e", fg="#eee").grid(row=1, column=0, sticky="e", padx=5)
        self.algo_var = StringVar(value="AES_Library")
        
        self.algo_menu = ttk.Combobox(settings_frame, textvariable=self.algo_var, width=20, state="readonly")
        self.algo_menu.grid(row=1, column=1, columnspan=2, sticky="w", padx=5, pady=2)

        # --- Anahtar Bilgileri Göstergesi (algoritma listesinden önce oluşturulmalı) ---
        self.key_info_label = tk.Label(settings_frame, text="", bg="#1a1a2e", fg="#00ff88", font=("Arial", 9))
        self.key_info_label.grid(row=1, column=3, sticky="w", padx=10)
        self.algo_var.trace_add("write", self._update_key_info)
        
        self._update_algorithm_list()

        # --- Klasik Şifre Parametreleri ---
        params_frame = tk.LabelFrame(settings_frame, text="📝 Parametreler", bg="#1a1a2e", fg="#aaa", font=("Arial", 9))
        params_frame.grid(row=2, column=0, columnspan=4, sticky="ew", pady=5, padx=5)

        # Shift (Caesar)
        tk.Label(params_frame, text="Shift:", bg="#1a1a2e", fg="#eee").grid(row=0, column=0, sticky="e", padx=3)
        self.shift_var = IntVar(value=3)
        tk.Entry(params_frame, textvariable=self.shift_var, width=5, bg="#16213e", fg="white").grid(row=0, column=1, sticky="w", padx=3)

        # Key / Parola
        tk.Label(params_frame, text="Key:", bg="#1a1a2e", fg="#eee").grid(row=0, column=2, sticky="e", padx=3)
        self.key_var = StringVar(value="SecretKey1234567")  # 16 karakter AES için
        tk.Entry(params_frame, textvariable=self.key_var, width=20, bg="#16213e", fg="white").grid(row=0, column=3, sticky="w", padx=3)

        # Affine A, B
        tk.Label(params_frame, text="Affine A:", bg="#1a1a2e", fg="#eee").grid(row=1, column=0, sticky="e", padx=3)
        self.a_var = IntVar(value=5)
        tk.Entry(params_frame, textvariable=self.a_var, width=5, bg="#16213e", fg="white").grid(row=1, column=1, sticky="w", padx=3)

        tk.Label(params_frame, text="Affine B:", bg="#1a1a2e", fg="#eee").grid(row=1, column=2, sticky="e", padx=3)
        self.b_var = IntVar(value=8)
        tk.Entry(params_frame, textvariable=self.b_var, width=5, bg="#16213e", fg="white").grid(row=1, column=3, sticky="w", padx=3)

        # Rails
        tk.Label(params_frame, text="Rails:", bg="#1a1a2e", fg="#eee").grid(row=2, column=0, sticky="e", padx=3)
        self.rails_var = IntVar(value=3)
        tk.Entry(params_frame, textvariable=self.rails_var, width=5, bg="#16213e", fg="white").grid(row=2, column=1, sticky="w", padx=3)

        # ===== MESAJ GÖNDERİMİ =====
        send_frame = tk.Frame(self.root, bg="#1a1a2e")
        send_frame.pack(padx=10, pady=10, fill="x")

        self.entry = tk.Entry(send_frame, width=60, font=("Arial", 11), bg="#16213e", fg="white", insertbackground="white")
        self.entry.pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        self.entry.bind("<Return>", lambda e: self.send_message())

        self.send_btn = tk.Button(send_frame, text="🔒 Şifrele ve Gönder", command=self.send_message, 
                                   bg="#e94560", fg="white", font=("Arial", 10, "bold"),
                                   activebackground="#ff6b6b", cursor="hand2")
        self.send_btn.pack(side=tk.LEFT, padx=5)

        # ===== DURUM ÇUBUĞU =====
        status_frame = tk.Frame(self.root, bg="#0f0f23")
        status_frame.pack(fill="x", side=tk.BOTTOM)
        
        self.status_label = tk.Label(status_frame, text=f"✅ Bağlı: {self.HOST}:{self.PORT}", 
                                      bg="#0f0f23", fg="#00ff88", font=("Arial", 9))
        self.status_label.pack(pady=3)

    def _update_algorithm_list(self):
        """Seçilen moda göre algoritma listesini günceller."""
        mode = self.mode_var.get()
        
        if mode == "library":
            algorithms = ["AES_Library", "DES_Library"]  # RSA kaldırıldı (key exchange için)
        elif mode == "manual":
            algorithms = ["AES_Manual", "DES"]  # RSA kaldırıldı
        else:  # classic
            algorithms = EncryptionFactory.CLASSIC_ALGORITHMS
        
        self.algo_menu['values'] = algorithms
        if algorithms:
            self.algo_var.set(algorithms[0])
        self._update_key_info()

    def _update_key_info(self, *args):
        """Seçilen algoritmanın anahtar bilgisini gösterir."""
        if not hasattr(self, 'key_info_label'):
            return
            
        algo = self.algo_var.get()
        info = EncryptionFactory.get_algorithm_info(algo)
        
        if info:
            if info.get("key_size"):
                self.key_info_label.config(text=f"🔑 {info['key_size']} byte anahtar | {info['description']}")
            else:
                self.key_info_label.config(text=f"📜 {info['description']}")
        else:
            self.key_info_label.config(text="")

    def handle_received(self, message):
        """Server'dan gelen mesajları gösterir."""
        self.chat_area.insert(tk.END, f"📥 Gelen: {message}\n")
        self.chat_area.see(tk.END)

    def send_message(self):
        """Mesajı şifreler ve gönderir."""
=======
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
>>>>>>> 6fbfecac606b02cc84d206202e00760216dde9fa
        mesaj = self.entry.get()
        if not mesaj:
            return

<<<<<<< HEAD
=======

>>>>>>> 6fbfecac606b02cc84d206202e00760216dde9fa
        algo = self.algo_var.get()
        
        params = {
            "shift": self.shift_var.get(),
            "key": self.key_var.get(),
            "a": self.a_var.get(),
            "b": self.b_var.get(),
            "rails": self.rails_var.get()
        }

<<<<<<< HEAD
        try:
            # Key exchange tamamlandıysa bilgi göster
            if self.client.is_handshake_done():
                shared_algo = self.client.get_symmetric_algo()
                self.chat_area.insert(tk.END, f"📤 Ben [Paylaşılan {shared_algo}]: {mesaj} → [ŞİFRELİ]\n")
            else:
                mode_text = self.mode_var.get().upper()
                self.chat_area.insert(tk.END, f"📤 Ben [{mode_text}/{algo}]: {mesaj} → [ŞİFRELİ]\n")
            
            # Şifrele ve gönder
            self.client.send_encrypted(mesaj, algo, **params)
            self.chat_area.see(tk.END)
            self.entry.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Şifreleme Hatası", str(e))

    def run(self):
        """Ana döngüyü başlatır."""
        self.root.mainloop()


if __name__ == "__main__":
    ClientUI().run()
=======
        
        self.client.send_encrypted(mesaj, algo, **params)
        
        # Ekrana bilgi ver
        self.chat_area.insert(tk.END, f"Ben ({algo}): {mesaj} -> [ŞİFRELİ GÖNDERİLDİ]\n")
        self.chat_area.see(tk.END)
        self.entry.delete(0, tk.END)

    def run(self):
        self.root.mainloop()
>>>>>>> 6fbfecac606b02cc84d206202e00760216dde9fa
