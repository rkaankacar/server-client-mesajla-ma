import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, StringVar
import string
import random

# ------------------ ŞİFRELEME ALGORİTMALARI ------------------

ALPHABET_LOWER = string.ascii_lowercase
ALPHABET_UPPER = string.ascii_uppercase
M = 26

# ---------- Sezar
def caesar_encrypt(text, shift=3):
    res = ""
    for c in text:
        if c.islower():
            res += ALPHABET_LOWER[(ALPHABET_LOWER.index(c)+shift)%M]
        elif c.isupper():
            res += ALPHABET_UPPER[(ALPHABET_UPPER.index(c)+shift)%M]
        else:
            res += c
    return res

def caesar_decrypt(text, shift=3):
    return caesar_encrypt(text, -shift%M)

# ---------- Vigenere
def vigenere_encrypt(text, key="KEY"):
    res, ki = "", 0
    key = ''.join(k for k in key if k.isalpha())
    for c in text:
        if c.isalpha():
            k = key[ki%len(key)]
            shift = ALPHABET_LOWER.index(k.lower())
            if c.islower():
                res += ALPHABET_LOWER[(ALPHABET_LOWER.index(c)+shift)%M]
            else:
                res += ALPHABET_UPPER[(ALPHABET_UPPER.index(c)+shift)%M]
            ki +=1
        else:
            res += c
    return res

def vigenere_decrypt(text, key="KEY"):
    res, ki = "",0
    key = ''.join(k for k in key if k.isalpha())
    for c in text:
        if c.isalpha():
            k = key[ki%len(key)]
            shift = ALPHABET_LOWER.index(k.lower())
            if c.islower():
                res += ALPHABET_LOWER[(ALPHABET_LOWER.index(c)-shift)%M]
            else:
                res += ALPHABET_UPPER[(ALPHABET_UPPER.index(c)-shift)%M]
            ki+=1
        else:
            res += c
    return res

# ---------- Substitution
def generate_substitution_key():
    letters = list(ALPHABET_LOWER)
    shuffled = letters[:]
    random.shuffle(shuffled)
    return {p:c for p,c in zip(letters,shuffled)}

sub_key = generate_substitution_key()

def substitution_encrypt(text):
    res = ""
    for c in text:
        if c.islower():
            res += sub_key.get(c,c)
        elif c.isupper():
            lower = c.lower()
            res += sub_key.get(lower,lower).upper()
        else:
            res += c
    return res

def substitution_decrypt(text):
    inverse = {v:k for k,v in sub_key.items()}
    res = ""
    for c in text:
        if c.islower():
            res += inverse.get(c,c)
        elif c.isupper():
            lower = c.lower()
            res += inverse.get(lower,lower).upper()
        else:
            res += c
    return res

# ---------- Affine
def egcd(a,b):
    if a==0: return (b,0,1)
    g,y,x = egcd(b%a,a)
    return g, x-(b//a)*y, y

def modinv(a,m):
    g,x,_ = egcd(a,m)
    if g!=1: raise ValueError("No modular inverse for given a")
    return x%m

a_affine, b_affine = 5, 8  # a coprime with 26

def affine_encrypt(text):
    res=""
    for c in text:
        if c.islower():
            x = ALPHABET_LOWER.index(c)
            res += ALPHABET_LOWER[(a_affine*x+b_affine)%M]
        elif c.isupper():
            x = ALPHABET_UPPER.index(c)
            res += ALPHABET_UPPER[(a_affine*x+b_affine)%M]
        else:
            res += c
    return res

def affine_decrypt(text):
    a_inv = modinv(a_affine,M)
    res=""
    for c in text:
        if c.islower():
            y = ALPHABET_LOWER.index(c)
            res += ALPHABET_LOWER[(a_inv*(y-b_affine))%M]
        elif c.isupper():
            y = ALPHABET_UPPER.index(c)
            res += ALPHABET_UPPER[(a_inv*(y-b_affine))%M]
        else:
            res += c
    return res

# Şifreleme seçim fonksiyonu
def encrypt_message(text, algo):
    if algo=="Sezar":
        return caesar_encrypt(text)
    elif algo=="Vigenere":
        return vigenere_encrypt(text)
    elif algo=="Substitution":
        return substitution_encrypt(text)
    elif algo=="Affine":
        return affine_encrypt(text)
    return text

def decrypt_message(text, algo):
    if algo=="Sezar":
        return caesar_decrypt(text)
    elif algo=="Vigenere":
        return vigenere_decrypt(text)
    elif algo=="Substitution":
        return substitution_decrypt(text)
    elif algo=="Affine":
        return affine_decrypt(text)
    return text

# ------------------ SERVER & GUI ------------------

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
            decrypted = decrypt_message(data, algo_var.get())
            chat_area.insert(tk.END, f"Client ({addr}): {decrypted}\n")
            chat_area.see(tk.END)
        except:
            break
    conn.close()
    if conn in clients:
        clients.remove(conn)

def start_server():
    chat_area.insert(tk.END, f"Server başlatıldı: {HOST}:{PORT}\n")
    chat_area.see(tk.END)
    while True:
        conn, addr = server_socket.accept()
        clients.append(conn)
        chat_area.insert(tk.END, f"Bağlantı geldi: {addr}\n")
        chat_area.see(tk.END)
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

def send_message():
    mesaj = entry.get()
    if mesaj:
        enc = encrypt_message(mesaj, algo_var.get())
        for c in clients:
            try:
                c.sendall(enc.encode())
            except:
                pass
        chat_area.insert(tk.END, f"Server: {mesaj}\n")
        chat_area.see(tk.END)
        entry.delete(0, tk.END)

# ------------------ TKINTER UI ------------------

root = tk.Tk()
root.title("Server")

chat_area = scrolledtext.ScrolledText(root, width=60, height=20)
chat_area.pack(padx=10, pady=10)

entry = tk.Entry(root, width=40)
entry.pack(side=tk.LEFT, padx=10, pady=5)

send_btn = tk.Button(root, text="Gönder", command=send_message)
send_btn.pack(side=tk.LEFT)

# Algoritma seçim Listbox
algo_var = StringVar(value="Sezar")
algo_box = tk.OptionMenu(root, algo_var, "Sezar", "Vigenere", "Substitution", "Affine")
algo_box.pack(pady=5)

# Server thread
threading.Thread(target=start_server, daemon=True).start()

root.mainloop()
