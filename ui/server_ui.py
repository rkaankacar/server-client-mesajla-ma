<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Server UI - RSA Key Exchange destekli
AES, DES, RSA desteği ile (kütüphane ve manuel modlar)
"""

import tkinter as tk
from tkinter import scrolledtext, StringVar, messagebox, IntVar, ttk
import threading
from core.network.server import ChatServer
from core.encryption.encryption_factory import EncryptionFactory
from core.encryption.aes_library import AESLibraryCipher
from core.encryption.des_library import DESLibraryCipher
import socket


class ServerUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🖥️ Server - Güvenli Dinleme İstasyonu")
        self.root.geometry("800x950")
        self.root.configure(bg="#1a1a2e")

        self._create_widgets()
        
        # Server başlat
        host = socket.gethostbyname(socket.gethostname())
        self.server = ChatServer(host, 0)
        threading.Thread(target=self.start_server, daemon=True).start()

    def _create_widgets(self):
        """Tüm UI bileşenlerini oluşturur."""
        
        # ===== KEY EXCHANGE DURUMU =====
        key_frame = tk.Frame(self.root, bg="#0f0f23")
        key_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(key_frame, text="🔑 RSA Key Exchange:", bg="#0f0f23", fg="#eee", 
                 font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.key_status_label = tk.Label(key_frame, text="⏳ Client bekleniyor...", 
                                          bg="#0f0f23", fg="#ffcc00", font=("Arial", 9))
        self.key_status_label.pack(side=tk.LEFT, padx=10)
        
        # ===== CHAT ALANI =====
        chat_frame = tk.LabelFrame(self.root, text="💬 Gelen Mesajlar (Şifreli)", 
                                    bg="#1a1a2e", fg="#eee", font=("Arial", 10, "bold"))
        chat_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.chat_area = scrolledtext.ScrolledText(chat_frame, width=85, height=18, 
                                                    bg="#16213e", fg="#00ff88", 
                                                    font=("Consolas", 10),
                                                    insertbackground="white")
        self.chat_area.pack(padx=5, pady=5, fill="both", expand=True)

        # ===== MESAJ GÖNDERİMİ =====
        send_frame = tk.Frame(self.root, bg="#1a1a2e")
        send_frame.pack(padx=10, pady=5, fill="x")
        
        self.entry = tk.Entry(send_frame, width=55, font=("Arial", 11), bg="#16213e", fg="white", insertbackground="white")
        self.entry.pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        self.entry.bind("<Return>", lambda e: self.send_message())

        self.send_btn = tk.Button(send_frame, text="🔒 Şifrele ve Gönder", command=self.send_message, 
                                   bg="#e94560", fg="white", font=("Arial", 10, "bold"),
                                   activebackground="#ff6b6b", cursor="hand2")
        self.send_btn.pack(side=tk.LEFT, padx=5)

        # ===== ÇÖZME BUTONU =====
        self.decrypt_btn = tk.Button(self.root, text="🔓 EKRANI TEMİZLE VE TÜM MESAJLARI ÇÖZ", 
                                      command=self.decrypt_all, 
                                      bg="#4ecca3", fg="black", font=("Arial", 11, "bold"),
                                      activebackground="#7fff00", cursor="hand2")
        self.decrypt_btn.pack(pady=8)

        # ===== KRİPTOĞRAFİ AYARLARI =====
        settings_frame = tk.LabelFrame(self.root, text="🔐 Kriptografi Anahtarları", 
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

        # --- Parametreler ---
        params_frame = tk.LabelFrame(settings_frame, text="📝 Parametreler", bg="#1a1a2e", fg="#aaa", font=("Arial", 9))
        params_frame.grid(row=2, column=0, columnspan=4, sticky="ew", pady=5, padx=5)

        # Shift (Caesar)
        tk.Label(params_frame, text="Shift:", bg="#1a1a2e", fg="#eee").grid(row=0, column=0, sticky="e", padx=3)
        self.shift_var = IntVar(value=3)
        tk.Entry(params_frame, textvariable=self.shift_var, width=5, bg="#16213e", fg="white").grid(row=0, column=1, sticky="w", padx=3)

        # Key / Parola
        tk.Label(params_frame, text="Key:", bg="#1a1a2e", fg="#eee").grid(row=0, column=2, sticky="e", padx=3)
        self.key_var = StringVar(value="SecretKey1234567")
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

        # ===== DURUM ÇUBUĞU =====
        status_frame = tk.Frame(self.root, bg="#0f0f23")
        status_frame.pack(fill="x", side=tk.BOTTOM)
        
        self.status_label = tk.Label(status_frame, text="⏳ Server başlatılıyor...", 
                                      bg="#0f0f23", fg="#ffcc00", font=("Arial", 9))
        self.status_label.pack(pady=3)

    def _update_algorithm_list(self):
        """Seçilen moda göre algoritma listesini günceller."""
        mode = self.mode_var.get()
        
        if mode == "library":
            algorithms = ["AES_Library", "DES_Library"]  # RSA kaldırıldı
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

    def start_server(self):
        """Server'ı başlatır ve bağlantıları dinler."""
        def handler(addr, data):
            # Key exchange mesajlarını UI'da gösterme (arka planda işleniyor)
            self.chat_area.insert(tk.END, f"📥 Client ({addr[0]}:{addr[1]}) [ŞİFRELİ]: {data[:60]}{'...' if len(data) > 60 else ''}\n")
            self.chat_area.see(tk.END)
            
            # Key exchange tamamlandığında durumu güncelle
            self._check_key_exchange_status()

        self.chat_area.insert(tk.END, f"🚀 Server başlatıldı!\n")
        self.chat_area.insert(tk.END, f"📡 Adres: {self.server.host}:{self.server.port}\n")
        self.chat_area.insert(tk.END, f"🔐 RSA Key Exchange aktif\n")
        self.chat_area.insert(tk.END, f"{'='*50}\n")
        self.chat_area.see(tk.END)
        
        # Status güncelle
        self.status_label.config(text=f"✅ Aktif: {self.server.host}:{self.server.port}", fg="#00ff88")
        
        self.server.start(handler)

    def _check_key_exchange_status(self):
        """Client'ların key exchange durumunu kontrol eder."""
        for conn, info in self.server.client_info.items():
            if info.get("handshake_done"):
                algo = info.get("symmetric_algo", "?")
                key = info.get("symmetric_key", b"")
                key_hex = key.hex()[:16] if key else "?"
                self.key_status_label.config(
                    text=f"✅ {algo} Key Paylaşıldı | {key_hex}...",
                    fg="#00ff88"
                )
                break

    def send_message(self):
        """Server'dan client'lara şifreli mesaj gönderir."""
=======
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
>>>>>>> 6fbfecac606b02cc84d206202e00760216dde9fa
        mesaj = self.entry.get()
        if not mesaj:
            return
            
        try:
<<<<<<< HEAD
            # Key exchange tamamlanmış client varsa, paylaşılan anahtarı kullan
            shared_key = None
            shared_algo = None
            
            for conn, info in self.server.client_info.items():
                if info.get("handshake_done"):
                    shared_key = info.get("symmetric_key")
                    shared_algo = info.get("symmetric_algo")
                    break
            
            if shared_key and shared_algo:
                # Paylaşılan anahtarla şifrele
                if shared_algo == "AES":
                    cipher = AESLibraryCipher()
                    cipher.key = shared_key
                elif shared_algo == "DES":
                    cipher = DESLibraryCipher()
                    cipher.key = shared_key
                else:
                    cipher = EncryptionFactory.get_cipher(
                        self.algo_var.get(),
                        shift=self.shift_var.get(),
                        key=self.key_var.get(),
                        a=self.a_var.get(),
                        b=self.b_var.get(),
                        rails=self.rails_var.get()
                    )
                enc = cipher.encrypt(mesaj)
                self.chat_area.insert(tk.END, f"📤 Server [Paylaşılan {shared_algo}] → {enc[:50]}...\n")
            else:
                cipher = EncryptionFactory.get_cipher(
                    self.algo_var.get(),
                    shift=self.shift_var.get(),
                    key=self.key_var.get(),
                    a=self.a_var.get(),
                    b=self.b_var.get(),
                    rails=self.rails_var.get()
                )
                enc = cipher.encrypt(mesaj)
                self.chat_area.insert(tk.END, f"📤 Server [{self.algo_var.get()}] → {enc[:50]}...\n")
            
            # Client'lara gönder
            self.server.send(enc)
            
            # Şifreli mesajı kaydet
            self.server.encrypted_messages.append(enc)
            
            self.chat_area.see(tk.END)
            self.entry.delete(0, tk.END)
            
=======
            
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
>>>>>>> 6fbfecac606b02cc84d206202e00760216dde9fa
        except Exception as e:
            messagebox.showerror("Hata", f"Gönderirken hata oluştu: {e}")

    def decrypt_all(self):
<<<<<<< HEAD
        """Biriken şifreli mesajları çözer (paylaşılan anahtar veya manuel)."""
        self.chat_area.delete('1.0', tk.END)
        self.chat_area.insert(tk.END, "═══════════════════════════════════════════════════\n")
        self.chat_area.insert(tk.END, "🔓 TÜM GEÇMİŞ MESAJLAR ÇÖZÜLÜYOR...\n")
        
        # Paylaşılan anahtar var mı kontrol et
        shared_key = None
        shared_algo = None
        
        for conn, info in self.server.client_info.items():
            if info.get("handshake_done"):
                shared_key = info.get("symmetric_key")
                shared_algo = info.get("symmetric_algo")
                break
        
        if shared_key:
            self.chat_area.insert(tk.END, f"🔑 Paylaşılan {shared_algo} Anahtarı Kullanılıyor: {shared_key.hex()}\n")
            
            if shared_algo == "AES":
                current_cipher = AESLibraryCipher()
                current_cipher.key = shared_key
            elif shared_algo == "DES":
                current_cipher = DESLibraryCipher()
                current_cipher.key = shared_key
        else:
            self.chat_area.insert(tk.END, f"📋 Manuel Algoritma: {self.algo_var.get()}\n")
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
                self.chat_area.insert(tk.END, f"❌ Cipher Hatası: {e}\n")
                return
        
        self.chat_area.insert(tk.END, "═══════════════════════════════════════════════════\n\n")

        if not self.server.encrypted_messages:
            self.chat_area.insert(tk.END, "📭 Hiç şifreli mesaj yok.\n")
            return

        success_count = 0
        for idx, enc_msg in enumerate(self.server.encrypted_messages):
            try:
                plain_text = current_cipher.decrypt(enc_msg)
                self.chat_area.insert(tk.END, f"✅ Mesaj #{idx+1}:\n")
                self.chat_area.insert(tk.END, f"   Şifreli: {enc_msg[:40]}{'...' if len(enc_msg) > 40 else ''}\n")
                self.chat_area.insert(tk.END, f"   🔓 Çözüm: {plain_text}\n\n")
                success_count += 1
            except Exception as e:
                self.chat_area.insert(tk.END, f"❌ Mesaj #{idx+1} çözülemedi: {e}\n\n")

        self.chat_area.insert(tk.END, "═══════════════════════════════════════════════════\n")
        self.chat_area.insert(tk.END, f"📊 Toplam: {len(self.server.encrypted_messages)} | Başarılı: {success_count}\n")
        self.chat_area.insert(tk.END, "═══════════════════════════════════════════════════\n")
        self.chat_area.see(tk.END)

    def run(self):
        """Ana döngüyü başlatır."""
        self.root.mainloop()


if __name__ == "__main__":
    ServerUI().run()
=======
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
>>>>>>> 6fbfecac606b02cc84d206202e00760216dde9fa
