import tkinter as tk
from tkinter import messagebox, simpledialog
import db
import utils

def orders_screen(root):
    root.title("Prise de commande")

    # Champs du formulaire
    tk.Label(root, text="Table").pack()
    entry_table = tk.Entry(root)
    entry_table.pack()

    tk.Label(root, text="Plat / Boisson").pack()
    entry_item = tk.Entry(root)
    entry_item.pack()

    tk.Label(root, text="Quantité").pack()
    entry_qty = tk.Entry(root)
    entry_qty.pack()

    tk.Label(root, text="Notes (ex: viande saignante)").pack()
    entry_notes = tk.Entry(root)
    entry_notes.pack()

    def add_order():
        conn = db.get_connection()
        cursor = conn.cursor()

        # Insérer la commande
        cursor.execute("INSERT INTO orders (table_id, status) VALUES (?, ?)", 
                       (entry_table.get(), "EN COURS"))
        order_id = cursor.lastrowid

        # Ajouter les détails
        cursor.execute("INSERT INTO order_items (order_id, item, quantity, notes) VALUES (?, ?, ?, ?)",
                       (order_id, entry_item.get(), entry_qty.get(), entry_notes.get()))

        conn.commit()
        conn.close()
        messagebox.showinfo("Succès", "Commande envoyée en cuisine ✅")

        # Choix du mode d’impression
        mode = simpledialog.askstring("Impression", "Voulez-vous imprimer en 'pdf' ou 'thermal' ?")

        if mode == "pdf":
            filename = utils.print_bill_pdf(order_id)
            messagebox.showinfo("Facture", f"Facture générée : {filename}")
        elif mode == "thermal":
            try:
                utils.print_bill_thermal(order_id)
                messagebox.showinfo("Facture", "Facture imprimée sur ticket thermique 🧾")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d’imprimer : {e}")
        else:
            messagebox.showinfo("Info", "Aucun ticket généré.")

    # Bouton d’envoi
    tk.Button(root, text="Envoyer commande et imprimer", command=add_order).pack()
