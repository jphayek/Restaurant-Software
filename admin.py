import tkinter as tk
import db

def admin_screen(root):
    root.title("Statistiques")
    frame = tk.Frame(root)
    frame.pack()

    conn = db.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*), SUM(total) FROM payments")
    total_cmds, total_money = cursor.fetchone()

    tk.Label(frame, text=f"Nombre de commandes : {total_cmds}").pack()
    tk.Label(frame, text=f"Chiffre d'affaires : {total_money if total_money else 0} €").pack()

    conn.close()
