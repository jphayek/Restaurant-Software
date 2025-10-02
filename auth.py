import tkinter as tk
from tkinter import messagebox
import db

def login_screen(root, on_success):
    root.title("Connexion")
    tk.Label(root, text="Nom d'utilisateur").pack()
    entry_user = tk.Entry(root)
    entry_user.pack()

    tk.Label(root, text="Mot de passe").pack()
    entry_pass = tk.Entry(root, show="*")
    entry_pass.pack()

    def check_login():
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username=? AND password=?", 
                       (entry_user.get(), entry_pass.get()))
        user = cursor.fetchone()
        conn.close()

        if user:
            role = user[0]
            messagebox.showinfo("Connexion", f"Bienvenue {entry_user.get()} ({role})")
            on_success(role)
        else:
            messagebox.showerror("Erreur", "Identifiants incorrects")

    tk.Button(root, text="Se connecter", command=check_login).pack()
