import tkinter as tk
import db
import auth, orders, kitchen, admin

def main():
    db.init_db()

    root = tk.Tk()

    def after_login(role):
        for widget in root.winfo_children():
            widget.destroy()
        if role == "serveur":
            orders.orders_screen(root)
        elif role in ["cuisinier", "barman"]:
            kitchen.kitchen_screen(root)
        elif role == "admin":
            admin.admin_screen(root)

    auth.login_screen(root, after_login)
    root.mainloop()

if __name__ == "__main__":
    main()
