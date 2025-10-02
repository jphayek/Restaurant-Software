import tkinter as tk
import db

def kitchen_screen(root):
    root.title("Cuisine / Bar - Commandes")
    frame = tk.Frame(root)
    frame.pack()

    def refresh():
        for widget in frame.winfo_children():
            widget.destroy()

        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT orders.id, tables.number, order_items.item, order_items.quantity, order_items.notes 
        FROM orders 
        JOIN tables ON orders.table_id = tables.id
        JOIN order_items ON order_items.order_id = orders.id
        WHERE orders.status='EN COURS'
        """)
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            tk.Label(frame, text=f"Commande {row[0]} | Table {row[1]} | {row[2]} x{row[3]} ({row[4]})").pack()

    tk.Button(root, text="Rafraîchir", command=refresh).pack()
    refresh()
